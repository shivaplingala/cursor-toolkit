# Read-Only Operation Catalog

Useful read-only operations per service, with the parameters that matter for
diagnosis. All are invoked through the wrapper:

```bash
python scripts/aws_read.py <service> <operation> --param Key=Value ... --region <region>
```

To see every operation the wrapper allows for a service: `--list-ops`.

**Token budget:** orchestrator uses `aws-ops-compact.md` (one row per domain).
Sub-agents get pre-filled commands via `subagent-evidence-lite.md` — do not paste
this file or `subagents-aws-index.md` into Task prompts. L2 dispatch map:
`../subagents-aws-index.md`.

## Table of contents
- CloudWatch Logs (`logs`)
- CloudWatch Metrics & Alarms (`cloudwatch`)
- S3 (`s3`)
- Lambda (`lambda`)
- EC2 (`ec2`)
- ECS (`ecs`)
- RDS (`rds`)
- API Gateway (`apigateway`, `apigatewayv2`)
- ELB / ALB (`elbv2`)
- DynamoDB (`dynamodb`)
- IAM (`iam`)
- CloudTrail (`cloudtrail`)
- SNS / SQS (`sns`, `sqs`)
- Step Functions (`stepfunctions`)
- Cost Explorer (`ce`)
- Health / Trusted Advisor (`health`, `support`)

---

## CloudWatch Logs (`logs`)
The first stop for "my app is erroring".

- `describe_log_groups` — find log groups. Params: `logGroupNamePrefix`, `limit`.
- `describe_log_streams` — streams within a group. Params: `logGroupName`,
  `orderBy=LastEventTime`, `descending=true`, `limit`.
- `filter_log_events` — search across streams by pattern + time. Params:
  `logGroupName`, `startTime`/`endTime` (epoch **ms**), `filterPattern`
  (e.g. `?ERROR ?Exception ?Timeout`, or `"{ $.level = \"error\" }"` for JSON
  logs), `limit`.
- `get_log_events` — raw events from one stream. Params: `logGroupName`,
  `logStreamName`, `startFromHead`.
- `start_query` / `get_query_results` — CloudWatch Logs Insights. NOTE:
  `start_query` begins with `start` and is blocked by the wrapper as a mutating
  verb. Prefer `filter_log_events` for read-only investigation.

## CloudWatch Metrics & Alarms (`cloudwatch`)
Quantify the symptom (error rate, latency, CPU, throttles).

- `get_metric_data` — the workhorse. Pass `MetricDataQueries` (JSON),
  `StartTime`, `EndTime`. Lets you pull multiple metrics/stats at once.
- `get_metric_statistics` — simpler single-metric pull. Params: `Namespace`,
  `MetricName`, `Dimensions`, `StartTime`, `EndTime`, `Period`, `Statistics`.
- `list_metrics` — discover what metrics/dimensions exist. Params: `Namespace`,
  `MetricName`.
- `describe_alarms` — current alarm states (which are in ALARM right now).
- `describe_alarm_history` — when alarms fired. Great for correlating to an
  incident time.

Common namespaces: `AWS/Lambda`, `AWS/ApiGateway`, `AWS/ApplicationELB`,
`AWS/RDS`, `AWS/ECS`, `AWS/SQS`, `AWS/DynamoDB`, `AWS/EC2`.

## S3 (`s3`)
- `list_buckets` — all buckets in the account.
- `list_objects_v2` — objects in a bucket. Params: `Bucket`, `Prefix`,
  `MaxKeys`, `ContinuationToken`.
- `head_object` — object metadata without downloading (size, content-type,
  storage class, encryption, last-modified). Params: `Bucket`, `Key`.
- `get_object` — object contents (wrapper caps body at 256 KB; good for config
  files and small logs, not large data). Params: `Bucket`, `Key`, `Range`.
- `get_bucket_policy` — the resource policy (key for "access denied" debugging).
- `get_bucket_acl`, `get_bucket_encryption`, `get_bucket_versioning`,
  `get_bucket_location`, `get_public_access_block`, `get_bucket_cors`,
  `get_bucket_lifecycle_configuration` — bucket configuration.
- `get_object_acl` — per-object permissions.

## Lambda (`lambda`)
- `get_function` / `get_function_configuration` — runtime, memory, timeout,
  env var keys, role, layers, last-modified. Params: `FunctionName`.
- `list_functions` — enumerate. 
- `get_policy` — resource policy (who can invoke it).
- `list_event_source_mappings` — triggers (SQS/Kinesis/DynamoDB) and their
  state (e.g. disabled, lag). Params: `FunctionName`.
- `get_account_settings` — concurrency limits (relevant for throttling).
- Pair with `logs filter_log_events` on `/aws/lambda/<FunctionName>` and
  `cloudwatch` `Errors`/`Throttles`/`Duration` metrics.

## EC2 (`ec2`)
- `describe_instances` — state, type, AZ, IPs, security groups, IAM profile.
  Params: `InstanceIds`, `Filters`.
- `describe_instance_status` — health checks, scheduled events.
- `describe_security_groups` — ingress/egress rules (connectivity debugging).
- `describe_network_interfaces`, `describe_subnets`, `describe_route_tables`,
  `describe_vpcs`, `describe_nat_gateways`, `describe_internet_gateways` —
  network path debugging.
- `describe_volumes`, `describe_snapshots` — storage.
- `get_console_output` — instance console (boot/crash diagnostics). Params:
  `InstanceId`.

## ECS (`ecs`)
- `list_clusters`, `list_services`, `list_tasks` — enumerate.
- `describe_services` — desired vs running count, deployment status, events
  (the `events` field often states exactly why tasks won't start). Params:
  `cluster`, `services`.
- `describe_tasks` — task stop reason, container exit codes. Params: `cluster`,
  `tasks`.
- `describe_task_definition` — image, CPU/memory, env keys, log config.
- Pair with the task's CloudWatch log group.

## RDS (`rds`)
- `describe_db_instances` — status, engine/version, endpoint, storage,
  multi-AZ, security groups, parameter group. Params: `DBInstanceIdentifier`.
- `describe_db_clusters` — Aurora clusters.
- `describe_events` — recent RDS events (failovers, restarts, storage).
- `describe_db_parameters` / `describe_db_parameter_groups` — config.
- `describe_db_snapshots` — backups.
- Pair with `cloudwatch` `CPUUtilization`, `FreeableMemory`,
  `DatabaseConnections`, `FreeStorageSpace`.

## API Gateway (`apigateway` REST / `apigatewayv2` HTTP)
- `get_rest_apis` / `get_apis` — enumerate.
- `get_stages` / `get_stage` — stage config, throttling, logging settings.
- `get_resources`, `get_method` — route/integration wiring.
- Pair with `cloudwatch` `5XXError`/`4XXError`/`Latency`/`Count` in
  `AWS/ApiGateway`, and the access/execution logs in CloudWatch Logs.

## ELB / ALB (`elbv2`)
- `describe_load_balancers`, `describe_listeners`, `describe_rules` — wiring.
- `describe_target_groups`, `describe_target_health` — **which targets are
  unhealthy and why** (the `TargetHealth.Reason`/`Description` is gold for 5xx).
- Pair with `AWS/ApplicationELB` metrics: `HTTPCode_Target_5XX_Count`,
  `HTTPCode_ELB_5XX_Count`, `TargetResponseTime`, `UnHealthyHostCount`.

## DynamoDB (`dynamodb`)
- `describe_table` — schema, capacity mode, indexes, status.
- `query` / `scan` — read items (read-only). Use sparingly; `scan` reads the
  whole table. Params: `TableName`, `KeyConditionExpression`, `Limit`.
- `get_item` — single item. Params: `TableName`, `Key`.
- `describe_continuous_backups`, `describe_time_to_live`.
- Pair with `AWS/DynamoDB` `ThrottledRequests`, `ConsumedReadCapacityUnits`.

## IAM (`iam`)
Permission failures are one of the most common AWS bugs.

- `get_role` / `get_user` — the principal.
- `list_attached_role_policies` / `list_role_policies` — what's attached.
- `get_policy` + `get_policy_version` — managed policy document.
- `get_role_policy` — inline policy document.
- `simulate_principal_policy` — **test whether a principal can perform an
  action** without changing anything. Params: `PolicySourceArn`,
  `ActionNames`, `ResourceArns`. The cleanest way to confirm an AccessDenied.
- `get_account_authorization_details` — full export (large; filter).

## CloudTrail (`cloudtrail`)
Answers "what changed and who did it".

- `lookup_events` — recent management events. Params: `LookupAttributes`
  (e.g. `[{"AttributeKey":"EventName","AttributeValue":"DeleteBucket"}]`),
  `StartTime`, `EndTime`. Correlate a config change to an incident time.
- `get_trail_status`, `describe_trails` — is logging even on.

## SNS / SQS (`sns`, `sqs`)
- SQS `get_queue_attributes` — `ApproximateNumberOfMessages`,
  `...NotVisible`, redrive policy / DLQ (backlog & poison-message debugging).
  Params: `QueueUrl`, `AttributeNames=['All']`.
- SQS `list_queues`, `get_queue_url`.
- SNS `get_topic_attributes`, `list_subscriptions_by_topic`,
  `get_subscription_attributes` — delivery config, DLQ.

## Step Functions (`stepfunctions`)
- `list_executions` — recent runs and status. Params: `stateMachineArn`,
  `statusFilter=FAILED`.
- `describe_execution` — one run's status, error, cause.
- `get_execution_history` — step-by-step, including the failing state and error.

## Cost Explorer (`ce`)
For "why did my bill spike".
- `get_cost_and_usage` — cost by service/time. Params: `TimePeriod`,
  `Granularity`, `Metrics`, `GroupBy`.
- `get_anomalies` — detected cost anomalies.

## Health / Support (`health`, `support`)
- `health describe_events` — AWS-side issues affecting your account/region.
- `support describe_trusted_advisor_checks` / `...check_result` — Trusted
  Advisor findings (requires Business/Enterprise support).

---

## Notes on parameters
- Times: CloudWatch **Logs** use epoch **milliseconds**; CloudWatch **Metrics**,
  CloudTrail, and Cost Explorer use ISO-8601 / `datetime`. Pass JSON values via
  `--param` (the wrapper parses Key=Value where Value can be JSON), e.g.
  `--param 'MetricDataQueries=[{"Id":"e","MetricStat":{...},"Period":300,"Stat":"Sum"}]'`.
- For anything you can't express on one line, it's fine to write a tiny throwaway
  Python script that imports the wrapper's `is_operation_safe` check, or just
  builds the param JSON and shells out to `aws_read.py`.