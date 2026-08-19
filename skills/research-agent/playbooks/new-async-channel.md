# Playbook: new-async-channel

Research type: `new-async-channel`

WhatsApp, SMS, or similar — **inbound webhook + outbound async push** via `channelOutboundReply`.

## Checklist

- [ ] Provider API choice (direct vs aggregator) with trade-offs table
- [ ] Webhook verification and signature validation (official doc links)
- [ ] Inbound message format → conversation-service session/message mapping
- [ ] Outbound async push: plug-in surface from `docs/analysis/async-channel-push-extensibility-review.md`
- [ ] Add to `ASYNC_PUSH_CHANNELS` in channel routing (`channel-routing.ts`)
- [ ] `channelRouting.<channel>` key schema in zone
- [ ] Reuse `apps/channels/shared/utils/outbound` — Outlook as reference impl only
- [ ] EventBridge rule + dedup DynamoDB pattern (compare Outlook)
- [ ] SQS: shared queue from tenant-management messaging stack
- [ ] Workflow prompt: `apps/conversation-service/src/prompts/agentic-workflow/<channel>.md`
- [ ] i18n labels in `conversation-ui` / `case-i18n`
- [ ] Template / opt-in / policy requirements (WhatsApp especially)
- [ ] `ALLOWED_CHANNELS` update in input-validation
- [ ] Full AWS + provider configuration inventory
- [ ] Rate limits, cost model, sandbox vs prod numbers

## Do not assume

- Integration-channel model (no async push) — confirm type with intake
- New queue per channel unless research proves shared queue insufficient

## Report emphasis

- End-to-end diagram: webhook → queue → processor → conversation-service → outbound
- Explicit comparison to `apps/channels/outlook/` with file-level mapping
- Security: webhook auth, PII in logs, attachment handling

## Sub-agent focus

| Sub-agent | Extra focus |
| --------- | ----------- |
| external-docs | Provider webhook + messaging API + template policies |
| github-samples | Official SDK samples; Outlook/Slack patterns in repo |
| aws-config-catalog | IAM, SQS, API Gateway routes, DynamoDB locks |
| codebase | ASYNC_PUSH_CHANNELS, outbound shared utils, SFN channel |
