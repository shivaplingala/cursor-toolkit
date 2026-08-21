---
name: fcd-v2
description: >-
  FCD-V2: gated delivery like full-cycle-delivery, plus optional Ruflo Phase-4
  swarm (escalate-only) with thin shared memory board, sidecars, append-only
  plan deltas, claim-before-edit, and Headroom on large sidecar reads. Use when
  the user invokes /fcd-v2 or asks for FCD-V2 / FCD Ruflo orchestration. Does
  not replace /full-cycle-delivery — user chooses. Keep FCD iron laws (grill,
  plan approval, coding+impact to 0, no autonomous prod merge).
---

# FCD-V2

Standalone alternative to classic **full-cycle-delivery** (FCD v1).  
**Do not edit or “upgrade” the FCD v1 plugin from this skill.** User picks `/full-cycle-delivery` or `/fcd-v2`.

## Path resolution

`$SKILL_ROOT` = this skill directory (first existing wins):

1. `~/.cursor/plugins/local/fcd-v2/skills/fcd-v2`
2. `~/.cursor/skills/fcd-v2`
3. `~/.claude/skills/fcd-v2`
4. `~/.agents/skills/fcd-v2` (Agents hub / **Zed** global skills)
5. `~/.gemini/config/skills/fcd-v2`
6. `~/.gemini/antigravity/skills/fcd-v2`

`$FCD_ROOT` = classic FCD skill (read-only dependency for gates/playbooks/prompts):

1. `~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery`
2. `~/.cursor/skills/full-cycle-delivery`
3. `~/.claude/skills/full-cycle-delivery`
4. `~/.gemini/config/skills/full-cycle-delivery`
5. `~/.gemini/antigravity/skills/full-cycle-delivery`

If `$FCD_ROOT` is missing, say so and stop (or fall back only if user allows documenting gates inline).

## Iron laws (same as FCD — non-negotiable)

1. No completion claims without fresh verify output.
2. Human plan approval before Phase 4 implement.
3. No autonomous prod deploy or PR merge.
4. Phases 2–3: **grill-me** then **grill-with-docs** before plan approval.
5. After approval, stay on this skill for Phases 4–7 (do not freestyle).
6. Phase 5 / ship: coding + impact review-fix until both `FINDING_COUNT: 0`.
7. **Progress ledger:** create/update `progress.md` (see `$FCD_ROOT/templates/progress.md`). New chat → resume from progress; do not re-intake. Swarm `memory.md` stays thin (pointers to sidecars only). Code edits → **ponytail** only.
8. **Grow knowledge every usage:** Read `$FCD_ROOT/knowledge/` before Phase 4; run `$FCD_ROOT/prompts/knowledge-capture.md` on Phase 7 / meaningful stop (same corpus as classic FCD).

## Phase map

| Phase | Behavior |
| ----- | -------- |
| 0–3 | Follow `$FCD_ROOT/SKILL.md` (intake, research, design, plan, grill, approval) |
| **4** | **Implement** — escalate → classic **or** swarm; same per-task gates as FCD (below) |
| 5–7 | Whole-branch review-fix, integrate (incl. **qa-fix-loop**), ship — never autonomous prod |

Announce: `Using FCD-V2` and whether Phase 4 is `classic` or `swarm`.

## Phase 4 — Implement (mandatory)

### 4a. Mode decision

**Compatibility pin (before escalate):** Resolve `$FCD_ROOT`. Require these files or **stop**:

- `$FCD_ROOT/SKILL.md`
- `$FCD_ROOT/playbooks/` (at least one playbook)
- `$FCD_ROOT/prompts/implementer.md`
- `$FCD_ROOT/prompts/coding-reviewer.md`
- `$FCD_ROOT/prompts/impact-reviewer.md`
- `$FCD_ROOT/prompts/review-fix-loop.md`
- `$FCD_ROOT/prompts/qa.md` + `qa-fix-loop.md` when UI/QA in plan
- `$FCD_ROOT/prompts/backend.md` when serverless/host-tooling in plan

Optional: `scripts/fcd-doctor.sh`.

Read `$SKILL_ROOT/escalate.md`. Score the approved plan.

| Score | Mode | How to run Phase 4 |
| ----- | ---- | ------------------ |
| **&lt; 2** | **classic** | Per-task loop below (no Ruflo). Cursor Task OK for parallel reads. |
| **≥ 2** | **swarm** | `$SKILL_ROOT/protocol.md` end to end — same per-task gates, plus board/claims/sidecars |

**Before first task:** skim `$FCD_ROOT/knowledge/` (build/debug/fix/performance/qa/swarm as relevant).

### 4b. Per-task loop (classic **and** swarm)

Same gates as `$FCD_ROOT` Phase 4. In swarm mode, orchestrator assigns via briefs/`memory.md`; workers still must hit verify + review-fix.

1. Prefer **QA first** when plan has catalog/gate tasks: **`qa-engineer`** (`$FCD_ROOT/prompts/qa.md`) before Frontend harness depends on case IDs.
2. Dispatch implementer (**ponytail** for all code):
   - Serverless / packages / host-tooling / progress protocol → **`backend-implementer`** + skill **backend** (`$FCD_ROOT/prompts/backend.md`)
   - UI / `ui-vue3-app` → **`frontend-implementer`** + skill **frontend** (+ **playwright-qa** for E2E)
   - QA catalog / gate / smoke / sign-off → **`qa-engineer`** + **qa** / **playwright-qa**
   - Else → `$FCD_ROOT/prompts/implementer.md`
3. Verify (exit 0):
   - serverless → `./scripts/verify-scope.sh <workspace>`
   - `host-tooling` → doctor / `--check` / host-matrix per playbook
   - QA smoke → `npm run test:e2e` on **localhost** only
4. Update **progress.md** (and swarm `memory.md` pointers); create `briefs/T<id>.md` on spawn
5. `$FCD_ROOT/prompts/spec-reviewer.md` → fix until plan matches
6. **Zero-finding review loop** — `$FCD_ROOT/prompts/review-fix-loop.md`:
   - coding-reviewer + impact-reviewer (read-only)
   - Write `sidecars/T<id>.round-<n>.md`; update Tasks `coding` / `impact` / `history`
   - Fix via implementer agents → re-verify → until both `PASS` / `FINDING_COUNT: 0`
7. Mark task `done` only when coding PASS 0, impact PASS 0, verify green (unless human `deferred`). QA non-code tasks: catalog/gate reviewed; no review-fix unless product code changed.
8. Check off plan tasks only after the loop exits clean.

**Limits:** verify 5×/task; review-fix max **10** rounds → escalate to human. Do not advance with open blocker / should-fix / edge-case.

**Swarm extras** (score ≥ 2 only): follow `protocol.md` — dense briefs, thin board, claim-before-edit, MISSING deltas, optional Ruflo glue. Do **not** skip 4b gates.

### 4c. Agents (plugin)

Prefer FCD plugin agents (also copied under `fcd-v2/agents/`):

| Agent | Role |
| ----- | ---- |
| `backend-implementer` | Serverless / host-tooling code |
| `frontend-implementer` | Vue UI / harness |
| `qa-engineer` | Catalog, gate, FAIL_LIST, sign-off |
| `coding-reviewer` / `impact-reviewer` / `review-fix-loop` | Dual review to 0 (impact = **graphify + GitNexus**) |

Phase 2 design personas stay on workspace `agency-engineering` — not these implement agents.

**Impact tooling:** `$FCD_ROOT/prompts/impact-reviewer.md` requires **both** graphify and GitNexus. Do not PASS shared-symbol edits on graphify alone.

## After Phase 4 (Phases 5–7)

1. Whole-branch coding + impact via `$FCD_ROOT/prompts/review-fix-loop.md` until both `FINDING_COUNT: 0`.
2. Integration / quality as FCD requires.
3. **QA gate:** `$FCD_ROOT/prompts/qa-fix-loop.md` — localhost `http://127.0.0.1:8080` only; FAIL_LIST → fix → targeted QA → full QA until `QA_ISSUE_COUNT: 0`.
4. **Knowledge capture (mandatory):** `$FCD_ROOT/prompts/knowledge-capture.md` → append to `$FCD_ROOT/knowledge/` (shared with classic FCD). Record in progress history.
5. Open PR if asked; never merge/prod deploy autonomously.

## Token posture

- Expect swarm Phase 4 ≈ **1.3–2.5×** classic Phase 4 when escalate fires; keep board thin or cost balloons.
- Headroom = lens on large sidecar **reads**, not the canonical store.
- Prefer append-only deltas over rewriting agent briefs.

## Related files

- `$SKILL_ROOT/escalate.md` — when Ruflo is needed
- `$SKILL_ROOT/protocol.md` — board, sidecars, deltas, claims, Headroom, completeness
- `$FCD_ROOT/playbooks/*` — work-type checklists
- `$FCD_ROOT/prompts/*` — implementer / reviewers / review-fix-loop / knowledge-capture
- `$FCD_ROOT/knowledge/` — growing delivery craft (shared with `/full-cycle-delivery`)
