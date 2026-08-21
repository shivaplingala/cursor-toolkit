---
name: review-fix-loop
description: >-
  Coordinator for full-cycle-delivery Phase 4/5: dispatch coding + impact
  reviewers, merge findings, fix via implementer, re-verify, and loop until
  both reviews return 0 findings (max 10 rounds then escalate).
---

# Review-fix loop coordinator

Follow the protocol (resolve relative to the plugin skill):

`~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery/prompts/review-fix-loop.md`

(also via `~/.cursor/skills/full-cycle-delivery/prompts/review-fix-loop.md`)

## Loop (summary)

1. Dispatch **coding-reviewer** (read-only)
2. Dispatch **impact-reviewer** (read-only, GitNexus + graphify)
3. If both `PASS` and `FINDING_COUNT: 0` → done
4. Else fix all blocker / should-fix / edge-case (and nits or waive)
5. Work-type verify exit 0 (`verify-scope` **or** host-tooling doctor/matrix)
6. Repeat from step 1 (max 10 rounds, then escalate to human)

You own the fixes. Reviewers never edit. Do not advance tasks or ship with open findings.
