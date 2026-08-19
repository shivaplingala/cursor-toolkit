# Dispatch decision (orchestrator — phase 0.9)

Parent-only. Run after hypotheses + SST scan, **before** phase 1 evidence.

## Quick flow

1. Draft numbered `COMMAND_LIST` from hypotheses.
2. Merge domains that hit the same resource.
3. Score domains (+ rules in `orchestrator.md` step 8).
4. Apply overrides (`DISPATCH_PREFERENCE`, `TOKEN_SENSITIVE`).
5. Emit `DISPATCH:` line, then execute.

## Examples

| Symptom | Draft commands | Decision |
| ------- | -------------- | -------- |
| Lambda timeout | 1× filter_log_events + 1× get_function_configuration | **INLINE** (2 commands) |
| Lambda + SQS + IAM | 3 independent WRAP calls | **L2 LITE** ×3 parallel |
| Playbook lists 4 reads, same log group | Merge → 1 filter | **INLINE** |
| Conv A + Conv B | 2× L1 investigators | **L1**; each may inline if ≤2 commands |
| Need log group name first | wave 1 describe inline → re-score | Often stays **INLINE** |

## Output template

```text
DISPATCH: inline
REASON: 2 commands after merge; TOKEN_SENSITIVE=yes
DOMAINS: aws-logs, aws-lambda
COMMANDS: 2
```

```text
DISPATCH: l2-lite
REASON: 4 independent domains; parallel faster than serial
DOMAINS: aws-logs, aws-lambda, aws-sqs, aws-iam
COMMANDS: 4
```
