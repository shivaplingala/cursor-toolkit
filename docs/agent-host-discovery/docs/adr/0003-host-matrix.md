# Host matrix: one catalog, all editors

User-global skills, commands, rules, and agents are published from canonical Cursor plugin trees into every supported host using `scripts/lib/host-discovery.sh`.

**Status:** accepted

**Hosts (symlink skill trees unless noted):**

| Host | Skill root | Command | Rule |
| ---- | ---------- | ------- | ---- |
| Cursor | `~/.cursor/skills` | `~/.cursor/commands` | plugin + `~/.cursor/rules/*.mdc` |
| Claude Code | `~/.claude/skills` | `~/.claude/commands` | stripped `~/.claude/rules/*.md` |
| GLM Coding Plan | Claude Code paths (Z.AI → Claude Code) | same | same |
| GLM ZCode | `~/.zcode/skills` | — (skills as `/name`) | — |
| Codex | `~/.codex/skills` | `~/.codex/prompts` | stripped `~/.codex/rules/*.md` |
| Antigravity / Gemini | **copy** `~/.gemini/config/skills` and `~/.gemini/antigravity/skills` | both command roots | dual `.mdc` + `.md` |
| Zed | `~/.agents/skills` | `~/.agents/commands` | — |
| OpenCode | `~/.config/opencode/skills` | `~/.config/opencode/command` | — |
| Kilo Code | `~/.kilo/skills` | `~/.config/kilo/command` | — |
| Kimi Code | `~/.kimi-code/skills` | `~/.kimi-code/commands` | — |
| Qwen Code | `~/.qwen/skills` | `~/.qwen/commands` | — |
| DeepSeek Harness | `~/.dsh/skills` **and** `~/.agents/skills` | — | — |
| Orca | universal `~/.agents/skills`; aggregates every agent home via `orca skills installed` | — | — |

**Agents** copy to: `~/.cursor/agents`, `~/.claude/agents`, `~/.agents/agents`, `~/.config/kilo/agent`.

**Consequences:** Re-run `install-all-hosts.sh` after plugin edits. Antigravity copies drift until then (ADR 0001). New hosts are added only in `host-discovery.sh`, not per-plugin.
