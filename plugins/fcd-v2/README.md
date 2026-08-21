# FCD-V2

Standalone **alternative** delivery orchestration. Choose explicitly:

| Command | Plugin | Behavior |
| ------- | ------ | -------- |
| `/full-cycle-delivery` | `full-cycle-delivery` | Classic FCD (unchanged) |
| `/fcd-v2` | `fcd-v2` (this) | FCD gates + optional Ruflo Phase 4 |

**This plugin does not modify FCD v1.** You pick which slash command to run.

## Canonical path

```
~/.cursor/plugins/local/fcd-v2/
```

Skill: `skills/fcd-v2/` → also `~/.cursor/skills/fcd-v2` after install script.

## What V2 adds (Phase 4 only)

When escalate criteria fire (≥2):

1. Orchestrator writes dense per-agent briefs (files + AC, no ambiguity)
2. Thin shared `memory.md` board + fat **sidecars** (diffs/logs referenced, not inlined)
3. Append-only plan deltas (agents read new line ranges only)
4. Claim-before-edit; conflicts → orchestrator delta (keep vs do)
5. Headroom on large sidecar **reads**; disk stays full-fidelity
6. After all tasks: same whole-branch coding + impact review-fix to 0 as FCD

When escalate does **not** fire: follow classic FCD Phase 4 (Cursor Task / single implementer).

## Dependencies (not bundled)

- FCD skill available for gates/playbooks/prompts (read-only reference)
- **Impact review (same as FCD):** **graphify** CLI + MCP **gitnexus** — both required; never graphify-only
- Ruflo MCP `user-ruflo` (swarm / tasks / claims) — only if escalate
- Headroom MCP `user-headroom` — large sidecar context

Never `ruflo init` in a workspace unless asked.

## Install

```bash
~/.cursor/plugins/local/fcd-v2/scripts/install-symlinks.sh
```

| Host | Skill | Command | Rule |
| ---- | ----- | ------- | ---- |
| Cursor / Claude / agents hub / **Zed** | symlink (`~/.agents/skills` = Zed global) | copy | — |
| **Antigravity / Gemini** | **real copy** (both `~/.gemini/config/skills` and `~/.gemini/antigravity/skills`) | `~/.gemini/config/commands/fcd-v2.md` | dual `.mdc` + stripped `.md` under `~/.gemini/config/rules/` |

Antigravity copies drift until you re-run the installer after plugin updates (**copy freshness**). Glossary/ADRs: workspace `docs/agent-host-discovery/` when the workspace repo is open.

```bash
# Drift check
~/.cursor/plugins/local/fcd-v2/scripts/install-symlinks.sh --check
~/.cursor/plugins/local/full-cycle-delivery/scripts/fcd-doctor.sh
```

Reload Cursor / MCP / Antigravity after install.

