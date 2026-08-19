# QA (FCD prompt)

Dispatch agent **`qa-engineer`** (plugin `agents/qa-engineer.md`). Skills: **qa**, **playwright-qa** (E2E), **ponytail** only if editing test code.

## When to run

| Moment | QA work |
| ------ | ------- |
| Phase 3 plan | Add QA tasks when user-facing / UI / Playwright / resume board is in scope (catalog, gate, smoke, sign-off) |
| Phase 4 early (recommended) | Catalog + id-map + gate before Frontend builds harness |
| Phase 6 | Execute smoke / gate; record progress + sidecar |
| Phase 7 | Sign-off required when plan listed QA tasks or UI E2E was in scope |

## Parent must pass

- Plan + progress paths
- Suites in scope
- `PLAYWRIGHT_BASE_URL` / auth state note (no secrets in progress)

## Exit

Follow **`prompts/qa-fix-loop.md`**: FAIL_LIST → orchestrator assigns fixes → targeted QA → full QA → impact → until `QA_ISSUE_COUNT: 0`.  
Local **BASE_URL** must be `http://127.0.0.1:8080`. Do not mark Phase 6 complete until gate PASS or human `## WAIVED`.
