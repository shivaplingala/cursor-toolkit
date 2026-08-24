# Protocol: plan review → fix loop (main agent)

**Owner:** main / coordinator agent (not the reviewers). Reviewers are read-only; **you** edit the plan.

## Goal

After research, grill, and a complete plan — **before** asking for human plan approval — loop until **both** coding and impact reviews of the **plan** return `STATUS: PASS` with `FINDING_COUNT: 0`.

That means **0** issues, bugs, edge cases, and **0** other unwaived findings.

Fixes go into the **plan** (files to touch, callers, tasks, guards, tests, risks). Do not start Phase 4 product code in this loop.

## When

End of Phase 3, after all of:

1. Phase 1 research done (Approved report when research-agent was used)
2. **grill-me** then **grill-with-docs** complete (`## Grill-Q&A` recorded)
3. Complete plan exists (`docs/plans/YYYY-MM-DD-<slug>.md`) with tasks and file lists

Do **not** request human plan approval until this loop exits clean. Same gate for `/full-cycle-delivery` and `/fcd-v2`.

## Inputs you must extract from the plan

- Every Create / Modify / Delete path
- Named symbols, contracts, event shapes, SST bindings
- Acceptance criteria and verify commands

If the plan has no file list, that is a finding — add the list, then re-review. Do not PASS an empty blast radius.

## Loop

```text
round = 1
while true:
  1. Dispatch prompts/coding-reviewer.md MODE=PLAN
     (plan text + current code at planned paths; correctness, security, maintainability, performance, tests)
  2. Dispatch prompts/impact-reviewer.md MODE=PLAN
     (planned files + where they are used: callers/callees via graphify then GitNexus)
  3. Merge findings (dedupe by path / symbol)
  4. If both PASS and FINDING_COUNT==0 → write last round sidecar; update plan ## Plan review; ask for human approval; stop
  5. Else edit the **plan** only. Re-open only Grill-Q&A answers the findings invalidate; prefix `(impact)`. Do not re-run full grill.
  6. round += 1; if round > 10 → escalate to human with open findings; do not ask approval
```

## Finding policy

Same as `review-fix-loop.md`:

| Severity    | Action                                      |
| ----------- | ------------------------------------------- |
| blocker     | Must fix in the plan before next round      |
| should-fix  | Must fix in the plan before next round      |
| edge-case   | Must fix in the plan before next round      |
| nit         | Fix in the plan or `## WAIVED` with reason  |

`FINDING_COUNT: 0` / `PASS` only when nothing unwaived remains (issues, bugs, edge cases, other).

Blockers / should-fix / edge-case cannot be waived without a **new** explicit human waiver.

## GitNexus

Required when planned symbols live in a GitNexus-indexed repo. Work type `host-tooling` with no serverless/indexed symbols: pass `GITNEXUS: n/a` to the impact reviewer; graphify/grep of planned plugin paths still required.

## Report / sidecar

Write `docs/plans/YYYY-MM-DD-<slug>.plan-review.round-<n>.md` next to the plan. Also keep `## Plan review` on the plan (last STATUS / counts).

```text
PLAN_REVIEW_ROUND: <n>
CODING: PASS|FAIL (count)
IMPACT: PASS|FAIL (count) blast=<level>
OPEN:
- ...
FIXED_THIS_ROUND:
- ...
WAIVED:
- ...
```

## Forbidden

- Asking for plan approval with open findings
- Asking reviewers to edit the plan or code
- Starting Phase 4 implement during this loop
- Skipping impact because "it is only a plan"
- PASS with an empty planned-file list
