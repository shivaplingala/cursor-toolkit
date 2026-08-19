# Diagnostic Playbooks

Each playbook maps a symptom to its likely causes and the exact read-only
evidence that confirms or rules each out. Use them to decide *what to read*
instead of dumping everything. All commands go through
`python scripts/aws_read.py ...`.

---

## Lambda function erroring or failing

**Likely causes:** unhandled exception in code · timeout · out-of-memory ·
permission (role can't reach a resource) · throttling (concurrency limit) ·
bad/missing env var · downstream dependency failing · event source backlog.

**Evidence to pull:**
1. Errors in the logs:
   `logs filter_log_events --param logGroupName=/aws/lambda/<fn> --param filterPattern="?ERROR ?Exception ?Task timed out ?errorMessage" --param startTime=<ms> --param endTime=<ms>`
2. Error/throttle/duration shape over time:
   `cloudwatch get_metric_data` on `AWS/Lambda` `Errors`, `Throttles`,
   `Duration`, `ConcurrentExecutions` for the function.
3. Config sanity: `lambda get_function_configuration --param FunctionName=<fn>`
   — check `Timeout`, `MemorySize`, `Runtime`, env var **keys**, `Role`.
4. If permission suspected: `iam simulate_principal_policy` for the function's
   role against the action it's failing on (e.g. `s3:GetObject` on the ARN).
5. If event-driven and lagging:
   `lambda list_event_source_mappings --param FunctionName=<fn>` (State,
   LastProcessingResult) and the source's backlog (e.g. SQS attributes).

**Tells:** `Task timed out after N seconds` → timeout too low or downstream
slow. `Runtime exited ... signal` / memory near limit in `REPORT` line → OOM.
`AccessDenied`/`is not authorized to perform` → IAM. `Rate exceeded` / nonzero
`Throttles` → concurrency.

---

## API Gateway / ALB returning 5xx

**Likely causes:** backend (Lambda/target) erroring · backend timeout · no
healthy targets · integration misconfig · throttling.

**Evidence:**
1. Split client vs server: `cloudwatch` `5XXError` vs `4XXError`
   (`AWS/ApiGateway`) or `HTTPCode_Target_5XX_Count` vs `HTTPCode_ELB_5XX_Count`
   (`AWS/ApplicationELB`). ELB 5xx with healthy targets → ELB/timeout; Target
   5xx → the app.
2. ALB target health: `elbv2 describe_target_health --param TargetGroupArn=<arn>`
   — read `TargetHealth.Reason` and `Description`.
3. Latency: `TargetResponseTime` / `Latency` — climbing latency + 5xx often
   means backend timeout.
4. Backend logs: the Lambda or ECS/EC2 app logs for the same window.
5. API GW execution/access logs in CloudWatch Logs (if enabled) for the failing
   route.

---

## S3 "Access Denied"

**Likely causes:** IAM policy on the caller lacks the action · bucket policy
denies · Block Public Access · object owned by another account (ACL) · KMS key
policy (object is SSE-KMS and caller can't use the key) · wrong region/endpoint
· object/prefix doesn't exist (sometimes surfaces as 403).

**Evidence:**
1. Who is calling: `sts get_caller_identity`.
2. Can they, in theory: `iam simulate_principal_policy` for the principal vs
   `s3:GetObject` (or `ListBucket`) on the bucket/object ARN.
3. Bucket policy: `s3 get_bucket_policy --param Bucket=<b>` — look for explicit
   `Deny`, account/principal conditions, `aws:SourceVpce`, etc.
4. Public access block: `s3 get_public_access_block --param Bucket=<b>`.
5. Object exists & ownership: `s3 head_object --param Bucket=<b> --param Key=<k>`
   (404 vs 403 distinction), `s3 get_object_acl`.
6. Encryption: `s3 get_bucket_encryption` — if SSE-KMS, the caller also needs
   `kms:Decrypt` on the key (check the key, but note the wrapper won't run
   decrypt itself).

**Tell:** `ListBucket` denied but `GetObject` allowed often shows up as 403 on a
missing key — confirm with `head_object`.

---

## ECS task won't start / keeps stopping

**Likely causes:** image pull failure · OOM/exit code · failing health check ·
insufficient capacity (CPU/mem/ENIs) · task role/exec role permission · bad
secret/env reference.

**Evidence:**
1. `ecs describe_services --param cluster=<c> --param services=[<svc>]` — read
   the `events` array; it usually states the reason verbatim ("unable to place
   tasks", "CannotPullContainerError", etc.).
2. `ecs describe_tasks --param cluster=<c> --param tasks=[<id>]` — `stoppedReason`
   and each container's `exitCode`/`reason`.
3. `ecs describe_task_definition` — image URI, CPU/mem, log config, secrets.
4. App logs in the configured CloudWatch log group.
5. If exec/task role suspected: `iam simulate_principal_policy`.

**Tells:** `CannotPullContainerError` → ECR perms or wrong image tag. exit code
137 → OOM-killed. Health check failures → app not listening on the expected
port / slow start.

---

## RDS connectivity or performance

**Likely causes:** security group blocks the client · DB at connection limit ·
CPU/memory/storage exhaustion · failover/maintenance event · credentials/auth ·
in a private subnet the client can't reach.

**Evidence:**
1. `rds describe_db_instances --param DBInstanceIdentifier=<id>` — `DBInstanceStatus`,
   endpoint, `VpcSecurityGroups`, `PubliclyAccessible`, `MultiAZ`.
2. `rds describe_events --param SourceIdentifier=<id>` — recent failovers,
   reboots, storage events.
3. `cloudwatch` `AWS/RDS`: `DatabaseConnections` (vs max), `CPUUtilization`,
   `FreeableMemory`, `FreeStorageSpace`, `ReadLatency`/`WriteLatency`.
4. Network: `ec2 describe_security_groups` for the DB's SGs — does ingress allow
   the client's SG/CIDR on the DB port?

---

## IAM "not authorized to perform"

The fastest read-only confirmation in all of AWS:

1. `iam simulate_principal_policy --param PolicySourceArn=<principal-arn> --param ActionNames=[<action>] --param ResourceArns=[<resource-arn>]`
   — returns `allowed`/`explicitDeny`/`implicitDeny` per action, and which
   statement caused it.
2. If denied: inspect the attached/inline policies
   (`list_attached_role_policies`, `get_policy`+`get_policy_version`,
   `get_role_policy`) and any resource policy on the target (bucket policy, KMS
   key policy, etc.) for the missing allow or an explicit deny.
3. Watch for permission *boundaries* and SCPs (org-level) — `simulate` accounts
   for boundaries but not always SCPs; note this as a possibility if simulate
   says allowed yet the call still fails.

---

## Throttling / rate limiting

**Evidence:** look for `ThrottlingException` / `Rate exceeded` /
`ProvisionedThroughputExceeded` in logs, and the service's throttle metric:
Lambda `Throttles`, DynamoDB `ThrottledRequests` + `ConsumedReadCapacityUnits`
vs provisioned, API GW `Count` vs configured throttle, SQS/Kinesis iterator age.
Check service quotas/limits via the relevant `get_account_settings` /
`describe_*limits` read where available.

---

## Cost spike

1. `ce get_cost_and_usage --param Granularity=DAILY --param Metrics=[UnblendedCost] --param 'GroupBy=[{"Type":"DIMENSION","Key":"SERVICE"}]' --param 'TimePeriod={"Start":"YYYY-MM-DD","End":"YYYY-MM-DD"}'`
   — find which service jumped.
2. `ce get_anomalies` — AWS's own anomaly detection.
3. Drill into the culprit service (e.g. spike in S3 → request/data-transfer
   metrics; spike in Lambda → invocation/duration; spike in NAT → bytes).
4. `cloudtrail lookup_events` around the spike start to see what was created
   (note: creation can't be undone here — report it for the user to act on).

---

## "What changed?" (general regression)

When something worked yesterday and not today, go to CloudTrail first:

`cloudtrail lookup_events --param StartTime=<iso> --param EndTime=<iso>` filtered
by the resource or by mutating `EventName`s (e.g. `UpdateFunctionConfiguration`,
`ModifyDBInstance`, `PutBucketPolicy`, `AuthorizeSecurityGroupIngress`). Match a
change event's timestamp to when the symptom began.