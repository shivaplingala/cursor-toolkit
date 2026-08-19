# Playbook: integration-channel

Research type: `integration-channel`

ChatGPT, Claude, Microsoft Copilot, etc. — platform bot / API integration **without** async push unless product explicitly requires callback.

## Checklist

- [ ] **Do not** plan `channelOutboundReply` / `ASYNC_PUSH_CHANNELS` unless intake confirms outbound callback
- [ ] Session and conversation identity model (user id, tenant, thread id on platform)
- [ ] Platform bot registration, manifest, or plugin setup
- [ ] Auth: OAuth, API keys, JWT — store shapes only in report
- [ ] Inbound message path to conversation-service (sync vs webhook)
- [ ] Existing prompt file review: `apps/conversation-service/src/prompts/agentic-workflow/<channel>.md`
- [ ] Prompt Engineer eval needs (injection, tool permissions)
- [ ] Multi-Agent checklist: tool surface, HITL, trace design
- [ ] Optional mirror to email/web for notifications — **product decision**, list as open question
- [ ] `ALLOWED_CHANNELS` if new channel id
- [ ] Full provider portal configuration inventory
- [ ] AWS touchpoints (if any): API Gateway, Lambda, secrets — often lighter than async channels

## Report/warning

Integration channels differ from Outlook/Slack async delivery. Cite
`docs/analysis/channel-async-delivery-architecture.md` for when web/email mirror applies.

## Report emphasis

- Clear statement: persist-only vs callback-required
- Platform-specific auth and webhook (if any) with official links
- Open questions for product (notification strategy, session continuity)

## Sub-agent focus

| Sub-agent | Extra focus |
| --------- | ----------- |
| external-docs | Platform developer docs (OpenAI, Anthropic, Microsoft Copilot extensibility) |
| github-samples | Official platform samples; avoid generic chatbot tutorials |
| aws-config-catalog | Only if Lambda/API in path; else mark AWS N/A |
| codebase | Prompts, ALLOWED_CHANNELS, session model — not outbound utils |
