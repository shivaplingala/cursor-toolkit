---
name: playwright-qa
description: >-
  Playwright E2E / browser QA for serverless projects UI. Local FCD QA uses localhost only
  (127.0.0.1:8080). Use when writing or running Playwright smoke, mapping QA
  cases, CI e2e gates, or the QA fix-until-zero loop. Coding: ponytail.
---

# Playwright QA

## Local iron rule

- **baseURL:** `http://127.0.0.1:8080` only for local FCD QA
- Do **not** use `Playwright-Automation` remote hosts (example / example-learn / etc.)
- Patterns OK to borrow from `Playwright-Automation/docs/` (locators, traces) — see `FCD_LOCALHOST_POLICY.md`
- Config enforces loopback unless `CI=1` or `ALLOW_REMOTE_E2E=1`

## When

- `ui-vue3-app` `@playwright/test`
- Suite C in `docs/fcd-progress-playwright-qa/qa/test-cases.md`
- FCD Phase 6 + **`prompts/qa-fix-loop.md`** (FAIL_LIST → fix → re-QA → full QA → 0 issues)

## Do not

- Replace unit/verify-scope with E2E
- Commit secrets or OTP
- Invent journeys not in the QA catalog
- Run local QA against remote Playwright-Automation envs
- Use a coding style other than **ponytail** when editing test/harness code

## Workflow

1. Read `progress.md` + `qa/test-cases.md` + `qa/gate.md`
2. Unset `PLAYWRIGHT_BASE_URL` (or set loopback only)
3. **ponytail** before any code
4. Chromium-first; role/label locators; `storageState` via `E2E_STORAGE_STATE`
5. Run → emit FAIL_LIST for orchestrator (`qa-fix-loop`)
6. After fixes: targeted QA → full QA → impact if code changed → repeat until `QA_ISSUE_COUNT: 0`

## Commands

```bash
cd ui-vue3-app
unset PLAYWRIGHT_BASE_URL
npm run test:e2e
```

## Related

- Agent **qa-engineer**; FCD `prompts/qa.md` + `prompts/qa-fix-loop.md`
- Skills: **frontend**, **backend**, **qa**
