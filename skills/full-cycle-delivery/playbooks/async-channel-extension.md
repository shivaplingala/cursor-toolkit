# Playbook: async-channel-extension

**Work type:** `async-channel-extension`  
**When:** Channel app exists (Slack, Teams) but outbound async push is incomplete or missing.

**Greenfield channels** (WhatsApp, SMS): use `async-channel-greenfield.md` + research-agent `new-async-channel`.

## Prerequisites

- [ ] Channel already in `ALLOWED_CHANNELS` and `ASYNC_PUSH_CHANNELS` (or add in same PR)
- [ ] Channel matrix row exists: `docs/architecture/channel-capability-matrix.md`
- [ ] Internal research or approved report if provider outbound API is new to the team

## Focus (vs greenfield)

Skip inbound/webhook/SQS ingest if already implemented. This playbook is **outbound push completion**:

1. **`channelRouting.<channel>`** keys persisted on inbound (verify existing handlers)
2. **Outbound consumer:** EventBridge rule `detail.channel = ['<channel>']` + `outbound-reply-processor` Lambda
3. **`deliver()`** only — reuse `apps/channels/shared/utils/outbound` and `services/outbound`
4. **Content adaptation:** markdown → Slack blocks / Teams adaptive cards (channel-specific)
5. **Dedup:** shared `ChannelOutboundDedup` DynamoDB pattern (`apps/channels/outlook/AGENTS.md`)
6. **Tests:** outbound consumer, dedup/idempotency, provider client mocks
7. **Smoke:** trigger workflow reply on channel; confirm async delivery

## Reference implementations

| Channel | App path | Outbound status |
| ------- | -------- | --------------- |
| email | `apps/channels/outlook/` | Complete (reference) |
| slack | `apps/channels/slack/` | See channel matrix |
| teams | `apps/channels/teams/` | See channel matrix |

## Docs

- `docs/analysis/async-channel-push-extensibility-review.md`
- `apps/channels/outlook/AGENTS.md`

## Personas

Backend Architect (consumer wiring), Multi-Agent (partial failure / retries).

## Verify

```bash
./scripts/verify-scope.sh apps/channels/<channel>
./scripts/verify-scope.sh apps/conversation-service  # if routing touched
```
