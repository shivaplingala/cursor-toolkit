# AgentCore handoff (from aws-diagnose-read)

When the symptom is Amazon Bedrock **AgentCore** (runtime, gateway, memory,
traces, `agentcore` CLI, `agentcore/agentcore.json`), stay in diagnose only long
enough to classify. Then **load the matching sibling skill** in this plugin.

Diagnose remains **read-only** (`aws_read.py`). Do **not** run mutating
`agentcore add|deploy|update|delete` steps while the diagnose skill is active.
After the report, tell the user which skill to invoke for the fix.

## Classify → skill

| Symptom / intent | Load skill | Notes |
| ---------------- | ---------- | ----- |
| Wrong answers, tool failures, timeouts, missing logs/traces, CLI/env broken | `agents-debug` | Prefer `agentcore traces` / `agentcore logs`; use WRAP for raw CW/IAM reads |
| Add memory, VPC, multi-agent, browser, code interpreter, app integrate, teardown | `agents-build` | Handoff after diagnose; do not apply while diagnosing |
| Evals, online monitoring, CloudWatch/X-Ray dashboards, cost | `agents-optimize` | Observability setup after root cause is known |
| Production IAM/auth/secrets, cold start, session/`maxVms`, quotas | `agents-harden` | Checklist + limits; suggest, don't apply in diagnose mode |

## Sibling paths (this plugin)

```
skills/agents-debug/SKILL.md
skills/agents-build/SKILL.md
skills/agents-optimize/SKILL.md
skills/agents-harden/SKILL.md
```

## Intake extras (AgentCore path)

Ask once if missing (in addition to generic AWS fields when relevant):

```
AGENT_NAME / RUNTIME:           from agentcore/agentcore.json or user
APPROX_TIME_UTC:                (R)
AWS_REGION:                     (R)
SYMPTOM_CLASS:                  error | wrong-answer | tool | memory | timeout | traces | cli-doctor
```

## Read-only vs agents CLI

| Action | While diagnosing | After handoff |
| ------ | ---------------- | ------------- |
| `aws_read.py` / WRAP | ✅ | ✅ |
| `agentcore traces|logs|status` | ✅ (read) | ✅ |
| `agentcore add|deploy|update|delete` | ❌ suggest only | ✅ under build/optimize/harden |
| Mutating AWS CLI/SDK | ❌ | ❌ unless user leaves diagnose and explicitly asks |

## Report closeout

In **Suggested fix**, name the handoff skill explicitly, e.g.:

> Next: load `agents-debug` and run `agentcore traces get …`  
> Then: load `agents-harden` for `maxVms` / session lifecycle checklist.
