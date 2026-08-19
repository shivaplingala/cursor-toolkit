# Global Tooling (Headroom · Ruflo)

User-global skills + slash commands for **Headroom** (context compression) and
**Ruflo** (multi-agent orchestration), plus the **cursor-global-tooling** router.

## Canonical

| Piece | Path |
| ----- | ---- |
| Plugin | `~/.cursor/plugins/local/global-tooling/` |
| Skills | `~/.cursor/skills/{headroom,ruflo,cursor-global-tooling}/` |
| Cursor MCP | `~/.cursor/mcp.json` (`headroom`, `ruflo`) |
| Ruflo state | `~/.ruflo` (never `ruflo init` in a project unless asked) |

## Multi-agent install

Same pattern as full-cycle-delivery: one skill tree, per-host discovery + command.

```bash
~/.cursor/plugins/local/global-tooling/scripts/install-multi-agent.sh
```

| Host | Skill | Command | Rule |
| ---- | ----- | ------- | ---- |
| Cursor | `~/.cursor/skills/…` | plugin `/headroom` `/ruflo` | plugin `.mdc` |
| Claude Code | `~/.claude/skills/…` | `~/.claude/commands/…` | stripped `.md` |
| GLM Coding Plan | Claude Code paths | same | same |
| Codex | `~/.codex/skills/…` | `~/.codex/prompts/…` | stripped `.md` |
| Antigravity | `~/.gemini/config/skills/…` + `~/.gemini/antigravity/skills/…` (**copy**) | `~/.gemini/config/commands/…` | dual `.mdc` + stripped `.md` (headroom, ruflo, cursor-global-tooling) |
| OpenCode | `~/.config/opencode/skills/…` | `~/.config/opencode/command/…` | — |
| Kilo Code | `~/.kilo/skills/…` | `~/.config/kilo/command/…` | — |
| Kimi Code | `~/.kimi-code/skills/…` | `~/.kimi-code/commands/…` | — |
| Agents hub / **Zed** | `~/.agents/skills/…` (Zed global) | `~/.agents/commands/…` | — |

Re-run the install script after updating plugin skills (**copy freshness**). Glossary/ADRs: `docs/agent-host-discovery/` in the workspace.

## MCP (required for tools to work)

Skills tell the agent **when** to use the tools; MCP must be registered on the host.

```bash
# Headroom → every detected agent registrar
headroom mcp install --force

# Optional durable Claude/Codex proxy hooks
# headroom init claude -g
# headroom init codex -g
```

This machine was also wired for **Ruflo** MCP (same stdio server as Cursor) into:

- `~/.claude.json`
- `~/.codex/config.toml`
- `~/.config/opencode/opencode.json`
- `~/.gemini/antigravity/mcp_config.json` + `~/.gemini/config/mcp.json`
- `~/.config/kilo/kilo.json`
- `~/.kimi-code/mcp.json`

Restart each agent/IDE after install.

## Related

- Router skill: `cursor-global-tooling`
- FCD plugin: `full-cycle-delivery`
