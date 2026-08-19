# Protocol: QA → fix loop (main / orchestrator)

**Owner:** main / FCD orchestrator. **qa-engineer** runs suites and returns FAIL lists; implementers fix; orchestrator re-dispatches.

## Goal

Loop until **QA_ISSUE_COUNT: 0** (no failed P0 cases; waived only via plan `## WAIVED` or explicit human note).

## Local baseURL iron rule

- **Local QA always uses localhost:** `http://127.0.0.1:8080` (Vite in `ui-vue3-app`).
- Do **not** use Playwright-Automation remote hosts (`*.example.com`, `*.example-learn.com`, `*.example-hcm.com`, etc.) for this loop.
- Unset `PLAYWRIGHT_BASE_URL` locally (config defaults to loopback). Remote only if `CI=1` or human sets `ALLOW_REMOTE_E2E=1`.

Patterns borrowed from `Playwright-Automation/` (POM habits, traces, screenshots) — **not** its default `baseURL`.

## When

- FCD Phase 6 (and after any FE/BE fix that touches user-facing or progress-board acceptance)
- After receiving a FAIL list from **qa-engineer**

## Loop

```text
round = 1
while true:
  1. Dispatch qa-engineer (prompts/qa.md) — FULL suite in scope (localhost)
  2. Write sidecars/qa-round-<n>.md with GATE + FAIL_LIST (case ids)
  3. If QA_ISSUE_COUNT == 0 and GATE PASS → done (update progress.md)
  4. Hand FAIL_LIST to orchestrator → assign owners:
       BE-TC-*  → backend-implementer
       FE-TC-* / harness → frontend-implementer
       PW-TC-*  → frontend-implementer (app/locators) and/or qa-engineer (spec-only)
       XA-TC-*  → orchestrator / backend as listed
  5. Fix only the failed cases (ponytail)
  6. Impact: GitNexus/graphify on touched symbols (impact-reviewer if product code)
  7. Dispatch qa-engineer — TARGETED re-run of fixed case ids only
  8. If targeted still FAIL → stay on those ids (goto 4); else continue
  9. Dispatch qa-engineer — FULL suite again + impact check if code changed
 10. round += 1; if round > 10 → escalate to human with open FAIL_LIST; stop
```

## FAIL_LIST shape (orchestrator handoff)

```text
QA_ROUND: <n>
BASE_URL: http://127.0.0.1:8080
GATE: PASS|FAIL|PARTIAL
QA_ISSUE_COUNT: <n>
FAIL_LIST:
- <CASE-ID> | <playwright title or manual> | owner=backend|frontend|qa | note=…
SKIPPED:
- <CASE-ID> | reason=…   # not counted as issues unless P0 and unwaived
PASS:
- …
VERIFY: npm run test:e2e (exit code + snippet)
```

## Forbidden

- Claiming Phase 6/7 done with open unwaived FAIL_LIST items
- Running local QA against remote Playwright-Automation envs
- Skipping full QA after a targeted pass (always full before exit)
- Skipping impact when product code changed in the fix round
