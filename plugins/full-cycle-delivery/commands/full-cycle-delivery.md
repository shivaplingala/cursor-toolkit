---
name: full-cycle-delivery
description: >-
  Start the gated serverless-monorepo delivery pipeline (intake → research →
  grill → plan approval → implement → dual code review with fix-until-zero →
  verify → ship). Prefer this over ad-hoc feature implementation whenever the
  user wants a plan gate or full delivery.
---

# /full-cycle-delivery — gated delivery pipeline (intake → ship)

Resolve `$SKILL_ROOT` in order (first existing `SKILL.md` wins):

1. Plugin (Cursor): `~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery`
2. Cursor skills: `~/.cursor/skills/full-cycle-delivery`
3. Claude Code / GLM Coding Plan: `~/.claude/skills/full-cycle-delivery`
4. Agents hub / **Zed**: `~/.agents/skills/full-cycle-delivery`
5. Codex: `~/.codex/skills/full-cycle-delivery`
6. Antigravity / Gemini: `~/.gemini/config/skills/full-cycle-delivery`
7. Antigravity alt root: `~/.gemini/antigravity/skills/full-cycle-delivery`
8. OpenCode: `~/.config/opencode/skills/full-cycle-delivery`
9. Kilo Code: `~/.kilo/skills/full-cycle-delivery`
10. Kimi Code: `~/.kimi-code/skills/full-cycle-delivery`
11. Workspace: `<repo>/.claude/skills/full-cycle-delivery`

Read and follow `$SKILL_ROOT/SKILL.md` end to end. Full spec (when in serverless-monorepo): `skills-agents-autos-plans/FULL-CYCLE-DELIVERY-PLAN.md`.

Task: $ARGUMENTS

(If the line above shows the literal text "$ARGUMENTS", the placeholder was not
substituted — take the task from the rest of the user's message instead. If no task
was given at all, ask the user for one and stop.)

Rules:

1. **Phase 0 intake:** classify the work type (see classifier table in SKILL.md) and read the matching playbook under `$SKILL_ROOT/playbooks/`. If fewer than 2 of {trigger, outcome, scope, deploy env} are known, ask once and stop.
2. **Phase 1 research:** if external docs/provider config are needed, run the research-agent skill first and require an **Approved** report before continuing.
3. **Phase 2 design:** load personas from `.claude/skills/agency-engineering/INDEX.md`; produce ADR drafts from `docs/adrs/TEMPLATE.md` for structural decisions.
4. **Phase 3 plan:** write `docs/plans/YYYY-MM-DD-<slug>.md` from `docs/plans/TEMPLATE.md`. **Stop for explicit human plan approval before implementing.**
5. **Phase 4 implement:** skim `$SKILL_ROOT/knowledge/`; per task — QA-first when needed → **backend-** / **frontend-implementer** / **qa-engineer** (or `prompts/implementer.md`) → work-type verify exit 0 → spec-reviewer → `review-fix-loop` until coding+impact `FINDING_COUNT: 0` (max 10 rounds → escalate).
6. **Phases 5–7:** whole-branch coding+impact to 0; quality/smoke; **qa-fix-loop** (localhost) to `QA_ISSUE_COUNT: 0`; PR; **`prompts/knowledge-capture.md`** (grow shared knowledge) — **never** merge/prod autonomously.
