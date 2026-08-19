# Playbook: workflow-feature

**Work type:** `workflow-feature`

## Touch points

- `apps/workflow/src/functions/wf-actions/`
- SFN definitions, prompts

## Checklist

- [ ] Workflow steps use SFN `channel` for LLM prompt
- [ ] Async delivery uses `session.channel` — not `lastUserInteractionChannel`
- [ ] Tests: workflow unit + `tools/vitest/workflow-coverage.config.ts` where applicable
- [ ] `./scripts/verify-scope.sh apps/workflow`
