# Playbook: conversation-service-feature

**Work type:** `conversation-service-feature`

## Always read

Root `AGENTS.md` learned facts (error JSON shape, email validation, workflow channel rules).

## Touch points

- `apps/conversation-service/src/services/messages/`
- `apps/conversation-service/src/functions/`
- `apps/conversation-service/src/prompts/`
- `apps/conversation-service/src/utils/mongodb/`
- `protocols/shared/channel-routing.ts`, `channel-reply-dispatch.ts`

## Checklist

- [ ] GitNexus impact before shared handlers
- [ ] Primary error in JSON `error` field
- [ ] Workflow: SFN `channel` for prompt; async push uses `session.channel`
- [ ] Tests in `apps/conversation-service/tests/unit/`
- [ ] `./scripts/verify-scope.sh apps/conversation-service`
