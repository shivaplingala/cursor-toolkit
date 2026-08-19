---
name: fcd-v2
description: >-
  Start FCD-V2: classic FCD gates plus optional Ruflo Phase-4 swarm when
  escalate criteria fire. Does not replace /full-cycle-delivery — user chooses.
---

# /fcd-v2 — FCD-V2 (gated delivery + optional Ruflo Phase 4)

Resolve `$SKILL_ROOT` (first existing `SKILL.md` wins):

1. Plugin: `~/.cursor/plugins/local/fcd-v2/skills/fcd-v2`
2. Cursor: `~/.cursor/skills/fcd-v2`
3. Claude: `~/.claude/skills/fcd-v2`
4. Agents hub / **Zed**: `~/.agents/skills/fcd-v2`
5. Antigravity / Gemini: `~/.gemini/config/skills/fcd-v2`
6. Antigravity alt root: `~/.gemini/antigravity/skills/fcd-v2`

Resolve `$FCD_ROOT` for classic gates/playbooks/prompts (read-only):

1. `~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery`
2. `~/.cursor/skills/full-cycle-delivery`
3. `~/.claude/skills/full-cycle-delivery`
4. `~/.gemini/config/skills/full-cycle-delivery`
5. `~/.gemini/antigravity/skills/full-cycle-delivery`

Read and follow `$SKILL_ROOT/SKILL.md`. Do **not** modify the FCD v1 plugin.

Task: $ARGUMENTS

(If the line above shows the literal text "$ARGUMENTS", take the task from the
rest of the user's message. If no task was given, ask once and stop.)

Rules:

1. **Choose explicitly:** `/fcd-v2` = this skill. `/full-cycle-delivery` = classic FCD. Do not auto-switch the user's choice.
2. **Phases 0–3:** Follow `$FCD_ROOT` (intake, research, design, grill-me → grill-with-docs, plan, **human approval**). Stop if not approved. Create/update **progress.md**.
3. **Phase 4 — Implement (mandatory):**
   - Run `$SKILL_ROOT/escalate.md`. Score &lt; 2 → **classic**; score ≥ 2 → `$SKILL_ROOT/protocol.md` (**swarm**). Announce mode.
   - Compatibility pin: require `$FCD_ROOT` playbooks + implementer/coding/impact/review-fix-loop prompts (and qa/backend prompts when in plan).
   - Per task (classic **and** swarm): QA catalog first when needed → dispatch **backend-implementer** / **frontend-implementer** / **qa-engineer** (ponytail for code) → work-type verify exit 0 → spec-reviewer → `$FCD_ROOT/prompts/review-fix-loop.md` until coding+impact `FINDING_COUNT: 0` → update progress (swarm: board + briefs + claims).
   - Limits: verify 5×/task; review-fix max 10 rounds then escalate to human.
4. **Completeness (swarm):** Orchestrator checks AC + verify; append MISSING deltas with line numbers; agents read only new ranges.
5. **Phases 5–7:** Whole-branch coding + impact to `FINDING_COUNT: 0`; quality/smoke; **qa-fix-loop** (localhost only) to `QA_ISSUE_COUNT: 0`; **`$FCD_ROOT/prompts/knowledge-capture.md`** (grow `$FCD_ROOT/knowledge/`); PR — **never** autonomous prod merge.
6. **Headroom:** large sidecar reads only. **Ruflo:** escalate-only; never `ruflo init` in repo unless asked.
7. **Knowledge:** skim `$FCD_ROOT/knowledge/` before Phase 4; capture on closeout every usage.
