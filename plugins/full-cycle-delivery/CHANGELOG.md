# Changelog

## 1.10.0 — 2026-08-24

- Host catalog in `scripts/lib/host-discovery.sh`: Qwen Code, DeepSeek Harness (`~/.dsh/skills`), GLM ZCode (`~/.zcode/skills`), plus existing Cursor/Claude/Codex/Antigravity/Zed/OpenCode/Kilo/Kimi
- `scripts/install-all-hosts.sh` publishes FCD + FCD-V2 + staff-engineering + global-tooling
- ADR `docs/agent-host-discovery/docs/adr/0003-host-matrix.md`

## 1.9.0 — 2026-08-24

- Bundled **backend-architect** skill + agent for Phase 2 (APIs, Lambda, data, IAM, observability, reliability)
- Phase 2 **staff-engineering** router integration (`~/.cursor/plugins/local/staff-engineering/`)
- `prompts/backend-architect.md`; install links `~/.cursor/skills/backend-architect`
- Coding reviewer expanded: correctness, security, maintainability (JSDoc/comments on complex code), performance (CPU/memory), branch/test coverage
- Review output adds `REVIEW_SUMMARY` and optional `PRAISE`; mentor-style specific findings
- `knowledge/performance.md` — CPU/memory heuristics for code review

## 1.8.0 — 2026-08-24

- Phase 3 gate: after research + grill + complete plan, run `plan-review-fix-loop` (coding + impact of planned files and callers) until both `FINDING_COUNT: 0` before asking human plan approval
- Coding/impact reviewers accept `MODE=PLAN`; sidecars `docs/plans/<slug>.plan-review.round-<n>.md`

## 1.7.2 — 2026-08-21

- Impact reviewer requires **both** graphify and GitNexus (no graphify-only PASS when shared symbols changed); emit `EVIDENCE:` line

## 1.4.0 — 2026-08-12

- Shared `scripts/lib/host-discovery.sh`; installers use it
- `fcd-doctor.sh`, `install-multi-agent.sh --check`, `test-host-matrix.sh`
- Work type `host-tooling` playbook; verify-scope N/A for plugin work
- Plan `## WAIVED` + Grill-Q&A; Zed via `~/.agents/skills`


## 1.3.1 — 2026-08-07

- Antigravity dual-shape rules (`.mdc` + stripped `.md`) for `full-cycle-delivery`
- Command path list includes `~/.gemini/antigravity/skills/full-cycle-delivery`
- Document copy freshness + link to `docs/agent-host-discovery/`

## 1.3.0 — 2026-07-31

- Multi-agent install: `scripts/install-multi-agent.sh` (Claude, Codex, Antigravity, OpenCode, Kilo, Kimi, Agents hub)
- GLM Coding Plan covered via Claude Code skill/command paths
- Antigravity uses real skill copies (symlink discovery gaps)
- Slash command resolves `$SKILL_ROOT` across all host paths

## 1.2.0 — 2026-07-25

- Self-contained global skill copy under the plugin (no repo symlink)
- Link `~/.cursor/skills/full-cycle-delivery` → plugin skill
- Document global path resolution; prefer plugin over workspace copies
- Ensure grill-me / grill-with-docs / research-agent available under `~/.cursor/skills`

## 1.1.0 — 2026-07-22

- Add dual review → fix loop until 0 findings: `coding-reviewer`, `impact-reviewer`, `review-fix-loop` prompts + Cursor agents
- Phase 4/5 require coding + full-codebase impact reviews; main agent owns fixes; max 10 rounds then escalate
- Bump command/rule/docs to match

## 1.0.0 — 2026-07-21

- Initial local plugin: symlinked `full-cycle-delivery` skill, `/full-cycle-delivery` command, agent-requestable rule
