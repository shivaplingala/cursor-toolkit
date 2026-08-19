# Playbook: integration-channel

**Work type:** `integration-channel`  
**Research type:** `integration-channel`

**Examples:** ChatGPT, Claude, MS Copilot, phonecall

## Do NOT

- Add to `ASYNC_PUSH_CHANNELS`
- Plan `channelOutboundReply` / outbound consumer unless product adds callback

## Checklist

- [ ] Session / conversation identity model
- [ ] Auth and rate limiting for external surface
- [ ] Prompt: `agentic-workflow/<channel>.md` + Prompt Engineer eval
- [ ] Multi-Agent: tool permissions, injection from external content
- [ ] Optional mirror to email/web — product decision in Phase 0
- [ ] Update channel matrix

## Personas

Software Architect, Multi-Agent, Prompt Engineer.
