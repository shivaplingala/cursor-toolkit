# Merge template — evidence → timeline → report

Orchestrator-only. Use after L1/L2 sub-agents return JSON.

## Per-conversation timeline table

| Step (UTC) | Component | Event | Source domain |
| ---------- | --------- | ----- | ------------- |
| | websocket | Processing WebSocket message | logs-websocket |
| | websocket | Completed Bedrock agent invocation | logs-websocket |
| | outbound | Published channelOutboundReply | logs-websocket |
| | outbound | INIT_START / Init Duration | logs-outbound |
| | outbound | Reply sent via Graph API | logs-outbound |

Add user-local TZ column if `APPROX_TIME_UTC` implies one.

## Derived metrics (compute in parent)

| Metric | Formula |
| ------ | ------- |
| LLM / turn duration | finalize − turn start |
| Publish → Graph | Graph send − channelOutboundReply publish |
| Cold start | `Init Duration` from REPORT line |
| User-reported gap | inbox time − Graph send (note clock source) |

## Cross-conversation comparison (optional)

When `COMPARATIVE_REPORT=yes` or user asked "why A vs B":

| Metric | Conversation A | Conversation B |
| ------ | -------------- | -------------- |
| Web → Graph send | | |
| Outbound cold start | | |
| Same assistant messageId (web/email) | yes/no | yes/no |
| Dominant bottleneck | | |

## Map JSON → report sections

| Report section | Source |
| -------------- | ------ |
| Summary | Parent synthesis from timelines + metrics |
| Evidence | Bullets from `findings` + `timeline`; cite `commands_run` |
| Root cause | Parent; confidence confirmed/likely/possible |
| Suggested fix | Parent; user applies |
| How to verify | Parent |
| Open questions | Union of sub-agent `gaps` |

Full report skeleton: `report-template.md`.

## Conflict resolution

If two sub-agents disagree on timestamps, prefer CloudWatch `REPORT` / structured
log fields over inferred ordering. Note ambiguity in Open questions.
