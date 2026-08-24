# Performance — delivery craft

## Code review (CPU / memory)

- Hot path: unbounded loop, full-table scan, sync I/O in async handler → flag `should-fix`+
- Memory: entire collection in RAM, unbounded cache, large JSON parse per request
- Serverless: Lambda memory vs duration; payload size; concurrent fan-out
- N+1 DB/API calls; missing pagination on list endpoints
- Justified high usage (batch job, one-time migration) → note in review, not a finding

## FCD orchestration

- FCD-V2 swarm Phase 4 ≈ **1.3–2.5×** classic token cost — stay classic unless escalate ≥ 2.
- Keep swarm `memory.md` ≤ 80 lines / 8 KiB; fat → sidecars; Headroom only on large **reads**.
- Prefer Chromium-only Playwright until P0 green; avoid multi-browser local smoke.
- Append-only brief deltas beat rewriting whole agent briefs.
- Escalate score &lt; 2 → classic (TodoWrite + Task often enough); don’t open Ruflo for one-file renames.
