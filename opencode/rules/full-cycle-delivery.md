
# Full-cycle delivery — use the gated pipeline

Skill is **global**. Prefer plugin path over any workspace copy.

- For delivery work, load **full-cycle-delivery** first.
- Phases 2–3 require **grill-me** then **grill-with-docs** then **plan-review-fix-loop** to 0 before plan approval.
- Phase 2 backend (APIs / Lambda / data / IAM): dispatch **`backend-architect`** agent + skill from FCD plugin.
- Phase 2 staff/principal design: load **`staff-engineering`** router + narrowest domain skill.
- No Phase 4 without explicit plan approval.
- After approval, stay on full-cycle-delivery — do not freestyle.
- **Plan review (Phase 3):** coding-reviewer + impact-reviewer until both `FINDING_COUNT: 0`; edit the plan, not code.
- **Review-fix loop (Phase 4–5):** coding-reviewer + impact-reviewer until both `FINDING_COUNT: 0`.
- No autonomous prod deploy or PR merge.
- Pair with **research-agent** when external docs are needed.
