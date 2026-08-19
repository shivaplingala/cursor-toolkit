---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Grill-Q&A → plan

When a decision is **locked** (user answered), append it to the **active implementation plan** (usually `docs/plans/YYYY-MM-DD-*.md`):

1. Ensure a `## Grill-Q&A` section exists (create at end of plan if missing).
2. Append one bullet: `- Q: <question summary> A: <locked answer>`

Do this as you go — do not batch only at the end. If no plan file exists yet, create/update the draft plan first, then append.
