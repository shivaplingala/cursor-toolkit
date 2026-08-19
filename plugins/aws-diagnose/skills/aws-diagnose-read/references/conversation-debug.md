# conversation-service — read-only debug playbook

Extended reference for `SKILL.md`. AWS via
`$SKILL_ROOT/scripts/aws_read.py`; HTTP GET via `curl` +
`$DIAG_TOKEN`.

## Parallel dispatch

| Scope | Doc |
| ----- | --- |
| Orchestrator phases | `../orchestrator.md` |
| L1 per conversation (A, B, …) | `../subagent-conversation-investigator.md` |
| L2 logs | `../subagent-logs.md` |
| L2 API | `../subagent-api.md` |
| L2 S3 traces | `../subagent-s3.md` |
| Merge + compare | `../merge-template.md` |
| Report | `../report-template.md` |
| **Infra map (SSM, Lambdas, routes)** | `references/sst-infra-scan.md` |

## User intake

**Required-field gate:** `references/intake-required.md` — orchestrator asks user
before investigation if stage, conversation id, tenant id, region, time, or
`DIAG_TOKEN` are missing.

Single- and multi-conversation templates: `SKILL.md`.

## API discovery

- Routes: `apps/conversation-service/sst/stacks/api-stack-routes.ts`
- Handlers: `apps/conversation-service/src/functions/apis/**`
- Base URL: `https://{stage}.api.example.com` from `.env.example`

## S3 trace key

`traces/{tenantId}/{sessionId}/{messageId}/{traceId}.json.gz`

## Step Functions (read-only)

```bash
SKILL="$SKILL_ROOT/scripts/aws_read.py"

python $SKILL stepfunctions describe_execution \
  --param executionArn="<arn>" --region "$AWS_DEFAULT_REGION"

python $SKILL stepfunctions get_execution_history \
  --param executionArn="<arn>" --param maxResults=50 --region "$AWS_DEFAULT_REGION"
```

## Traces bucket

Resolve via `scan_sst.py` (`--topic ssm --search trace`) or SSM read (wrapper).
Traces stack: `apps/conversation-service/sst/stacks/traces-stack.ts`.

## Log groups

Stage-suffixed Lambda names — discover via `logs describe_log_groups` then filter.
See `../subagent-logs.md`.
