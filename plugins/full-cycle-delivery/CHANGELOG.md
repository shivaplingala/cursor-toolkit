# Changelog

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
