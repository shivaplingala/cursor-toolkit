# AWS L2 domains — token budget dispatch

**Orchestrator:** run **phase 0.9** (`orchestrator.md` / `dispatch-decision.md`) before
choosing inline vs lite. Do not skip the `DISPATCH:` line.

## Token rules

| Reads needed | Mode | What loads |
| ------------ | ---- | ---------- |
| ≤2 commands (phase 0.9) | **Inline** — parent runs WRAP | 1–2 rows from `aws-ops-compact.md` |
| 3+ independent commands | **L2 lite** parallel | `subagent-evidence-lite.md` + `COMMAND_LIST` only |
| 2+ conversations | **L1** parallel | investigator + pre-filled commands |

**Never** attach `subagent-aws-*.md` or full `services.md` to sub-agents.
**Never** paste `aws-ops-compact.md` whole table into a Task prompt.

## Domain → service map

| domain | svc |
| ------ | --- |
| aws-sts | sts |
| aws-logs | logs |
| aws-cloudwatch | cloudwatch |
| aws-s3 | s3 |
| aws-lambda | lambda |
| aws-ec2 | ec2 |
| aws-ecs | ecs |
| aws-rds | rds |
| aws-apigateway | apigateway |
| aws-apigatewayv2 | apigatewayv2 |
| aws-elbv2 | elbv2 |
| aws-dynamodb | dynamodb |
| aws-iam | iam |
| aws-cloudtrail | cloudtrail |
| aws-sns | sns |
| aws-sqs | sqs |
| aws-stepfunctions | stepfunctions |
| aws-ce | ce |
| aws-health | health |
| aws-support | support |

Ops + capture hints: `references/aws-ops-compact.md` (orchestrator reads selected rows).
Detailed catalog (rare): `references/services.md`.

## Example lite dispatch

```text
Task(readonly=true, subagent_type=shell, fast):
  subagent-evidence-lite.md — DOMAIN=aws-logs, COMMAND_LIST=[filter_log_events line…]
Task(readonly=true, subagent_type=shell, fast):
  subagent-evidence-lite.md — DOMAIN=aws-lambda, COMMAND_LIST=[get_function_configuration…]
```

Max 6–8 concurrent L2. `logs-*` / `api-*` domains use same lite shell.
