# Cursor Toolkit

Personal collection of **Cursor plugins**, **skills**, and **rules** for agent-assisted development.

## Contents

| Path | What |
|------|------|
| `plugins/` | Cursor local plugins (FCD, FCD-V2, global tooling, AWS diagnose) |
| `skills/` | Standalone agent skills (backend, frontend, QA, Headroom, Ruflo, grill-me, graphify, …) |
| `rules/` | Global Cursor rules (`.mdc`) |

### Plugins

- **full-cycle-delivery** — gated plan→build→verify→ship (`/full-cycle-delivery`)
- **fcd-v2** — FCD v2 with optional Ruflo swarm (`/fcd-v2`)
- **global-tooling** — Headroom, Ruflo, FCD router rules
- **aws-diagnose** — read-only AWS/SST diagnostics

### Not included

- **stage-mongo** — contains environment credentials; keep local only (`~/.cursor/skills/stage-mongo`)
- **Ruflo / Headroom MCP servers** — install separately; skills document how to wire them
- **Cursor marketplace plugins** — install from Cursor plugin store

## Install

```bash
git clone https://github.com/shivaplingala/cursor-toolkit.git
cd cursor-toolkit
bash install.sh
```

Then **reload Cursor**.

Verify:

```bash
bash install.sh --check
```

## What `install.sh` does

1. Copies plugins into `~/.cursor/plugins/local/`
2. Copies standalone skills into `~/.cursor/skills/`
3. Copies rules into `~/.cursor/rules/`
4. Runs each plugin's host-discovery symlink scripts (Claude, Codex, Gemini, … when those folders exist)

## Owner: refresh from this machine

After editing plugins/skills locally:

```bash
bash install.sh --pack
git add -A && git commit -m "Refresh toolkit from local install"
git push
```

## License

See [LICENSE](LICENSE). Plugin-specific licenses remain in each plugin folder.
