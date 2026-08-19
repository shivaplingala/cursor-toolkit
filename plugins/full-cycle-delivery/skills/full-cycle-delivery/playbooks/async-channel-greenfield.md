# Playbook: async-channel-greenfield

**Work types:** `async-channel-greenfield`, `async-channel-extension`  
**Research type:** `new-async-channel` (use research-agent first for greenfield)

**Reference:** `apps/channels/outlook/` — inbound processor + `outbound-reply-processor.ts`

## Prerequisites

- [ ] Approved research report at `docs/research/YYYY-MM-DD-<slug>-report.md` (greenfield)
- [ ] Channel matrix updated: `docs/architecture/channel-capability-matrix.md`

## Architecture contract

1. Add channel to `ASYNC_PUSH_CHANNELS` in `apps/conversation-service/src/services/messages/protocols/shared/channel-routing.ts`
2. Define routing keys in channel-reply-dispatch / `REQUIRED_ROUTING_KEYS`
3. Inbound: persist `channelRouting.<channel>` + session interaction channel
4. Outbound: new `outbound-reply-processor` Lambda + EventBridge rule `detail.channel = ['<channel>']`
5. Implement only `deliver()` via `apps/channels/shared/utils/outbound` — do not copy Outlook wholesale
6. Dedup: shared `ChannelOutboundDedup` DynamoDB pattern (`apps/channels/outlook/AGENTS.md`)
7. Workflow prompt: `apps/conversation-service/src/prompts/agentic-workflow/<channel>.md`
8. i18n: `packages/conversation-ui`, `packages/case-i18n`
9. SST: follow `outlook/sst/stacks/` pattern
10. Tests: routing, inbound metadata, outbound consumer, dedup/idempotency, provider mocks

## Personas

Software Architect (ADR), Backend Architect (infra), Multi-Agent (failure modes), DevOps (SST).

## Smoke

Webhook/fixture replay; provider sandbox; `aws-diagnose-read` for queue/logs if needed.

## Docs

- `docs/analysis/async-channel-push-extensibility-review.md`
- `docs/analysis/async-channel-push-routing-plan.md`
