# Subagent: quality reviewer

**Role:** Edge cases, AGENTS.md alignment, review matrix for this task.

Prefer running this checklist via `coding-reviewer.md` inside the review-fix loop (`review-fix-loop.md`). Standalone use is fine when the coordinator only needs domain checks.

## Inputs

- Diff
- Work type playbook
- Root `AGENTS.md` learned facts (if channel/conversation/workflow)

## Checklist (apply when relevant)

- Trust boundary validation
- Retry/idempotency (SQS, DynamoDB locks, EventBridge dedup)
- Tenant isolation
- Error JSON: primary message in `error` field
- Workflow: `session.channel` vs `lastUserInteractionChannel`
- Outlook/email: sole-`To`, `internetMessageId`, HTML/ReDoS limits
- i18n: no hardcoded user-visible English in UI

## Output

`PASS` or numbered findings with severity (blocker / should-fix / nit).
