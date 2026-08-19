# Read-Only AWS Command Catalog

All commands below are non-mutating. Replace `<...>` placeholders. Add `--region <region>` when the default is ambiguous. Prefer narrow time windows and `--query` to limit output.

## Identity / Account

```bash
aws sts get-caller-identity
aws iam list-account-aliases
```

## Lambda

```bash
aws lambda get-function --function-name <name>
aws lambda get-function-configuration --function-name <name> \
  --query '{Timeout:Timeout,Memory:MemorySize,Runtime:Runtime,Env:Environment.Variables,LastUpdate:LastUpdateStatus}'
aws lambda list-event-source-mappings --function-name <name>
aws lambda get-function-concurrency --function-name <name>
aws lambda list-versions-by-function --function-name <name>
```

## CloudWatch Logs

```bash
# Tail live (read-only stream)
aws logs tail "/aws/lambda/<name>" --follow --since 15m

# Errors in a window (epoch ms)
aws logs filter-log-events \
  --log-group-name "/aws/lambda/<name>" \
  --start-time $(( ($(date +%s) - 3600) * 1000 )) \
  --filter-pattern '?ERROR ?Exception ?"Task timed out" ?Runtime.ExitError'

# Find a specific request/correlation id
aws logs filter-log-events --log-group-name "/aws/lambda/<name>" \
  --filter-pattern '"<requestId-or-internetMessageId>"' \
  --start-time $(( ($(date +%s) - 86400) * 1000 ))

# Insights query
aws logs start-query --log-group-name "/aws/lambda/<name>" \
  --start-time $(( $(date +%s) - 3600 )) --end-time $(date +%s) \
  --query-string 'fields @timestamp,@message | filter @message like /ERROR/ | sort @timestamp desc | limit 50'
aws logs get-query-results --query-id <id>
```

## CloudWatch Metrics

```bash
# Generic template
aws cloudwatch get-metric-statistics \
  --namespace <AWS/Lambda|AWS/SQS|AWS/DynamoDB|AWS/ApiGateway> \
  --metric-name <Errors|Throttles|Duration|ApproximateAgeOfOldestMessage|ConsumedReadCapacityUnits|5XXError> \
  --dimensions Name=<Dim>,Value=<Val> \
  --start-time $(date -u -d '3 hours ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 --statistics Sum Average Maximum

aws cloudwatch describe-alarms --state-value ALARM
```

## API Gateway (HTTP API v2)

```bash
aws apigatewayv2 get-apis
aws apigatewayv2 get-routes --api-id <id>
aws apigatewayv2 get-integrations --api-id <id>
aws apigatewayv2 get-stages --api-id <id>
# 5xx metric: namespace AWS/ApiGateway, dimension Name=ApiId,Value=<id>
```

## SQS

```bash
aws sqs list-queues --queue-name-prefix "<app>-<stage>"
aws sqs get-queue-attributes --queue-url <url> --attribute-names All
# Depth, in-flight, DLQ redrive policy
aws sqs get-queue-attributes --queue-url <url> \
  --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible RedrivePolicy
```

> Do NOT use `receive-message` / `purge-queue` — both alter visibility/state. Use metrics and attributes only.

## DynamoDB

```bash
aws dynamodb describe-table --table-name <table>
aws dynamodb describe-time-to-live --table-name <table>
# Scoped read of one item (read-only)
aws dynamodb get-item --table-name <table> --key '{"pk":{"S":"<v>"},"sk":{"S":"<v>"}}'
# Targeted query (avoid full scans on prod)
aws dynamodb query --table-name <table> \
  --key-condition-expression "pk = :p" \
  --expression-attribute-values '{":p":{"S":"<v>"}}' --limit 25
```

## SSM Parameter Store

```bash
aws ssm describe-parameters --parameter-filters "Key=Name,Option=BeginsWith,Values=/<app>/<stage>"
aws ssm get-parameter --name "<name>"                 # metadata + value for String
aws ssm get-parameters-by-path --path "/<app>/<stage>" --recursive
# SecureString: only decrypt when essential; do not echo full value
aws ssm get-parameter --name "<name>" --with-decryption --query 'Parameter.{Name:Name,Type:Type}'
```

## Secrets Manager

```bash
aws secretsmanager list-secrets --filters Key=name,Values=<app>-<stage>
aws secretsmanager describe-secret --secret-id <id>   # metadata, rotation, deletion window
# Note: a secret in the scheduled-deletion recovery window throws InvalidRequestException, not ResourceNotFound.
```

## EventBridge

```bash
aws events list-event-buses
aws events list-rules --event-bus-name TenantEventsBus
aws events list-targets-by-rule --rule <rule> --event-bus-name TenantEventsBus
aws events describe-rule --name <rule> --event-bus-name TenantEventsBus
```

## KMS

```bash
aws kms list-keys
aws kms describe-key --key-id <id>
aws kms get-key-policy --key-id <id> --policy-name default
```

## S3

```bash
aws s3api head-bucket --bucket <bucket>
aws s3api get-bucket-policy --bucket <bucket>
aws s3 ls s3://<bucket>/<prefix>/ --recursive --summarize
aws s3api head-object --bucket <bucket> --key <key>
```

## IAM (permission diagnosis)

```bash
aws iam get-role --role-name <role>
aws iam list-attached-role-policies --role-name <role>
aws iam list-role-policies --role-name <role>
aws iam get-role-policy --role-name <role> --policy-name <inline>
# Verify whether a role can perform an action without doing it
aws iam simulate-principal-policy --policy-source-arn <role-arn> \
  --action-names events:PutEvents dynamodb:PutItem
```

## CloudTrail (who/what happened)

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=<name> \
  --start-time $(date -u -d '6 hours ago' +%Y-%m-%dT%H:%M:%S)
```
