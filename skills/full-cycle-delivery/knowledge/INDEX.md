# FCD knowledge corpus (shared)

**Canonical path:** `$FCD_ROOT/knowledge/`  
Both `/full-cycle-delivery` and `/fcd-v2` **read on start** and **write on closeout** (and mid-delivery when a lesson is sharp).

## Files

| File | Topic |
| ---- | ----- |
| `build.md` | How to build / implement / wire host tooling |
| `debug.md` | How to diagnose failures |
| `fix.md` | How to fix defects (patterns that worked) |
| `performance.md` | Perf / cost / token / runtime wins |
| `qa.md` | Localhost QA, Playwright, gates, FAIL_LIST loops |
| `swarm.md` | FCD-V2 Ruflo / board / escalate lessons |
| `log.md` | Append-only dated raw entries (source of truth for new lessons) |

## Rules

1. **Read** relevant topic files (+ recent `log.md` tail) before Phase 4 when resuming or starting implement.
2. **Capture** after each delivery closeout (Phase 7 or human stop with meaningful work) via `prompts/knowledge-capture.md`.
3. Prefer **one durable bullet** over diary. Deduplicate. No secrets, no PII, no raw credentials.
4. Topic files: keep each ≤ **40** bullets; when over, distill (merge/drop stale) then add.
5. `log.md` entries: dated, one lesson per bullet under a day heading.
6. Workspace DOX / `AGENTS.md` still own product contracts — this corpus owns **delivery craft** (how FCD builds/debugs/fixes).

## Invoke

```text
Load $FCD_ROOT/knowledge/INDEX.md
Follow prompts/knowledge-capture.md
```
