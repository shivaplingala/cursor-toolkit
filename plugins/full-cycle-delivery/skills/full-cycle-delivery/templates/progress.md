# Progress ledger template

Copy next to an approved plan as `docs/plans/YYYY-MM-DD-<slug>.progress.md`  
(or `.fcd-v2/<slug>/progress.md` when swarming).

```markdown
# Progress — <slug>
Plan: docs/plans/YYYY-MM-DD-<slug>.md
Updated: <iso>

## Phase checklist (FCD)
- [ ] 0 Intake
- [ ] 1 Research
- [ ] 2 Design
- [ ] 3 Plan + grill + approval
- [ ] 4 Implement
- [ ] 5 Cross-cutting review
- [ ] 6 Integration
- [ ] 7 Ship

Use `[~]` for partial phases.

## Tasks
| id | title | status | agent | coding | impact | verify | history |
|----|-------|--------|-------|--------|--------|--------|---------|
| T1 | … | todo | — | — | — | — | — |

Status: `todo` | `in_progress` | `partial` | `done` | `blocked` | `deferred`

## Active locks
- path | agent | since

## Sidecar index
- briefs/T1.md
- sidecars/T1.round-1.md

## Resume instructions (for next chat)
1. Read this file end-to-end
2. Read plan AC + tasks with status ≠ done
3. Skim `$FCD_ROOT/knowledge/` (or FCD skill `knowledge/`) for prior craft lessons
4. Continue from last history line; do not re-grill locked Grill-Q&A

## QA (when in scope)
- Agent: `qa-engineer` · skills: `qa`, `playwright-qa`
- Gate: PASS | FAIL | PARTIAL | N/A
- Sign-off: ready | blocked — …
- Last run sidecar: sidecars/qa-run-….md

## Knowledge
- Last capture: none | YYYY-MM-DD (topics: …)
```
