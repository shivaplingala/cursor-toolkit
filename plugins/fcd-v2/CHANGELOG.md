# Changelog

## 1.5.0 — 2026-08-24

- Host install uses shared catalog (Qwen, DeepSeek, ZCode + prior hosts)

## 1.4.0 — 2026-08-24

- Phase 2: inherit FCD **`staff-engineering`** router + domain skills; **`backend-architect`** for APIs/Lambda/data/IAM
- Compat pin: `$FCD_ROOT/prompts/backend-architect.md` when backend design in plan
- Install copies coding-reviewer / impact-reviewer / review-fix-loop / backend-architect agents

## 1.3.0 — 2026-08-24

- Phases 0–3 inherit FCD `plan-review-fix-loop`: after grill + complete plan, coding+impact of planned files/callers until 0 before asking approval
- Compat pin requires `$FCD_ROOT/prompts/plan-review-fix-loop.md`

## 1.2.0 — 2026-08-12

- Escalate annotated examples; FCD compat pin; memory.md ≤80 lines / 8KiB
- Install `--check`; shared host-discovery lib; Zed via agents hub


## 1.1.0 — 2026-08-07

- Antigravity host discovery install: skill copies (both Gemini roots), command, dual-shape rules
- Path resolution lists include `~/.gemini/config/skills` and `~/.gemini/antigravity/skills`
- Document copy freshness (re-run installer after plugin updates)

## 1.0.0 — 2026-08-07

- Initial FCD-V2 plugin (standalone; does not modify FCD v1)
- Optional Ruflo Phase 4 when escalate ≥2 criteria
- Thin shared memory board + sidecars + append-only plan deltas
- Claim-before-edit; Headroom as read lens on large sidecars
- Slash command `/fcd-v2`
