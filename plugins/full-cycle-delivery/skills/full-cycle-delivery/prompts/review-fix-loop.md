# Protocol: review → fix loop (main agent)

**Owner:** main / coordinator agent (not the reviewers). Reviewers are read-only; **you** apply fixes.

## Goal

Loop until **both** coding and impact reviews return `STATUS: PASS` with `FINDING_COUNT: 0`.

## When

After each Phase 4 task: implementer + **work-type verify** green + `spec-reviewer` PASS.

- Serverless: `./scripts/verify-scope.sh <workspace>`
- `host-tooling`: `fcd-doctor.sh` / `install-*.sh --check` / `test-host-matrix.sh` as the playbook requires

Also before Phase 7 ship (whole-branch diff), after all tasks complete.

## Loop

```text
round = 1
while true:
  1. Dispatch prompts/coding-reviewer.md  (fresh diff)
  2. Dispatch prompts/impact-reviewer.md (fresh symbols + GitNexus/graphify)
  3. Merge findings (dedupe by path:line / symbol)
  4. If both PASS and FINDING_COUNT==0 → done
  5. Else dispatch prompts/implementer.md (or fix inline) with the merged FAIL list only
  6. Re-run work-type verify (verify-scope **or** host-tooling doctor/matrix) (exit 0 required)
  7. round += 1; if round > 10 → escalate to human with open findings; stop
```

## Finding policy

| Severity     | Action                                      |
| ------------ | ------------------------------------------- |
| blocker      | Must fix before next review round           |
| should-fix  | Must fix before next review round           |
| edge-case    | Must fix before next review round           |
| nit          | Fix or waive with one-line reason in report |

**Plan `## WAIVED`:** Nits listed there with a human reason are pre-waived for this branch — record them under `WAIVED:` in the round report; do not count toward FAIL. Blockers / should-fix / edge-case still require a fix or a **new** explicit human waiver in chat/plan.

Do not advance to the next plan task or ship while any unwaived finding remains.

## Report shape (each round, main agent)

```text
REVIEW_ROUND: <n>
CODING: PASS|FAIL (count)
IMPACT: PASS|FAIL (count) blast=<level>
OPEN:
- ...
FIXED_THIS_ROUND:
- ...
WAIVED:
- ...
VERIFY: verify-scope **or** host-tooling doctor/matrix exit code + snippet
```

Also append the same summary to `sidecars/T<id>.round-<n>.md` and update **progress.md** Tasks columns (`coding`, `impact`, `history`).
## Forbidden

- Claiming done with open findings
- Asking reviewers to edit code
- Skipping impact review when shared symbols or cross-file contracts changed
- Infinite loop without the round-10 human escalate
