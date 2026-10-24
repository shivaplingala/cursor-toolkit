# Fix — delivery craft

- Coding + impact review-fix until both `FINDING_COUNT: 0` (max 10 rounds → human).
- QA fix loop: FAIL_LIST → owner agent → impact → targeted QA → **full** QA → until `QA_ISSUE_COUNT: 0` (`prompts/qa-fix-loop.md`).
- Plan `## WAIVED` covers nits only; blockers/should-fix/edge-case need a new human waiver.
- Name collision: agency **Backend Architect** = design; skill **backend** / **backend-implementer** = implement.
- LoopBack ReportDefinition parameters live on `__data`; `_.has` misses `defaultValue`. Getter + rethrow `olderThanNDays` invalid defaults (do not swallow 400).
- Dual-path dates: OOB parameters skip `buildConditionNode` — emit `lessThan` from ParameterResolver; nested `olderThanNDays` is a dedicated filter-builder branch, never `DYNAMIC_DATE_OPERATORS`.

