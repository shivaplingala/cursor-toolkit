# Playbook: frontend-package

**Work type:** `frontend-package`

Packages: `conversation-ui`, `outlook-admin-ui`, `workflow-ui`, etc.

## Bind to

- `packages/outlook-admin-ui/AGENTS.md` — WCAG 2.1 AA, combobox ARIA, `t()` for labels
- Vue 3 + Vuetify + Vitest — not React agency patterns

## Verify

```bash
./scripts/verify-scope.sh packages/<name>
```

## QA (when UI / Playwright in scope)

- Plan QA tasks; prefer catalog before harness
- Agent **qa-engineer** + **playwright-qa**; Phase 6 gate + Phase 7 sign-off
