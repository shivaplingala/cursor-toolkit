# conversation-service — read-only debug playbook

Extended reference for `SKILL.md` appendix. AWS via `scripts/aws_read.py`; HTTP GET
via `curl` + `$DIAG_TOKEN`.

## User intake template

See SKILL.md appendix for the copy-paste block.

## API discovery

- Routes: `apps/conversation-service/sst/stacks/api-stack-routes.ts`
- Handlers: `apps/conversation-service/src/functions/apis/**`
- Base URL: `https://{stage}.api.example.com` from `.env.example`

## S3 trace key

`traces/{tenantId}/{sessionId}/{messageId}/{traceId}.json.gz`

## Step Functions (read-only)

```bash
python scripts/aws_read.py stepfunctions describe_execution \
  --param executionArn="<arn>" --region "$AWS_DEFAULT_REGION"

python scripts/aws_read.py stepfunctions get_execution_history \
  --param executionArn="<arn>" --param maxResults=50 --region "$AWS_DEFAULT_REGION"
```

## Lambda → source file

After identifying the Lambda from logs, resolve the handler:

```bash
python scripts/aws_read.py lambda get_function_configuration \
  --param FunctionName=<name-from-log-group> --region "$AWS_DEFAULT_REGION"
```

Grep the returned `Handler` path or SST construct name in `apps/*/sst/` to get the
repo file and entry function for the **Code location** table in reports.

## Traces bucket

Resolve via SSM read (wrapper): `/<stage>/conversation-service/` or
TracesStack outputs in conversation-service SST.
