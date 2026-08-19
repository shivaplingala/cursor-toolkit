# Fix — delivery craft

- Coding + impact review-fix until both `FINDING_COUNT: 0` (max 10 rounds → human).
- QA fix loop: FAIL_LIST → owner agent → impact → targeted QA → **full** QA → until `QA_ISSUE_COUNT: 0` (`prompts/qa-fix-loop.md`).
- Plan `## WAIVED` covers nits only; blockers/should-fix/edge-case need a new human waiver.
- Name collision: agency **Backend Architect** = design; skill **backend** / **backend-implementer** = implement.
- Skipped P0 auth cases are not FAIL_LIST items — either provide storageState or explicit waive before ship.
