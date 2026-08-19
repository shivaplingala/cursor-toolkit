# AWS ops compact (orchestrator only)

**Do not paste this file into sub-agents.** Parent reads **only the row(s)** for
domains it dispatches, builds `COMMAND_LIST`, sends `subagent-evidence-lite.md`.

`WRAP="python $SKILL_ROOT/scripts/aws_read.py"`

| domain | svc | ops | capture (max 5 findings × 200 chars) |
| ------ | --- | --- | -------------------------------------- |
| aws-sts | sts | get_caller_identity | Account, Arn |
| aws-logs | logs | describe_log_groups, filter_log_events, get_log_events | errors, REPORT, cold start; **no** start_query |
| aws-cloudwatch | cloudwatch | get_metric_statistics, describe_alarms, describe_alarm_history | error/throttle/latency values, alarms in ALARM |
| aws-s3 | s3 | head_object, get_bucket_policy, list_objects_v2, get_public_access_block | 403/404, Deny in policy, prefix listing |
| aws-lambda | lambda | get_function_configuration, list_event_source_mappings, get_account_settings | timeout, memory, role, ESM state; **no** invoke |
| aws-ec2 | ec2 | describe_instances, describe_security_groups, get_console_output | state, SG rules, console snippet |
| aws-ecs | ecs | describe_services, describe_tasks, describe_task_definition | events[], stop reason, exit code |
| aws-rds | rds | describe_db_instances, describe_events | status, endpoint, recent events |
| aws-apigateway | apigateway | get_rest_apis, get_stage, get_resources | stage logging, integration URI |
| aws-apigatewayv2 | apigatewayv2 | get_apis, get_stage, get_routes | routes, integrations |
| aws-elbv2 | elbv2 | describe_target_health, describe_rules | TargetHealth.Reason (key for 5xx) |
| aws-dynamodb | dynamodb | describe_table, get_item, query | status, throttles hint; scan sparingly |
| aws-iam | iam | get_role, simulate_principal_policy | EvalDecision; redact secret values |
| aws-cloudtrail | cloudtrail | lookup_events, describe_trails | EventName, userIdentity, time (ISO not ms) |
| aws-sns | sns | get_topic_attributes, list_subscriptions_by_topic | DLQ on subs |
| aws-sqs | sqs | get_queue_url, get_queue_attributes | backlog, oldest message age, redrive |
| aws-stepfunctions | stepfunctions | list_executions, get_execution_history | failed state, error/cause |
| aws-ce | ce | get_cost_and_usage, get_anomalies | top services by cost |
| aws-health | health | describe_events | open AWS events in region |
| aws-support | support | describe_trusted_advisor_check_result | check status; needs support plan |

Epoch ms: logs only. Metrics/CloudTrail/CE: ISO/datetime. `--list-ops` for full allowlist.
