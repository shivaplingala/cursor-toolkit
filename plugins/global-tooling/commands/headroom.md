---
name: headroom
description: >-
  Compress large tool outputs via Headroom MCP (compress / retrieve / stats).
  Use for large dumps, context pressure, or when the user mentions Headroom /
  token savings. Not for short replies or the single file being edited.
---

# /headroom — context compression

Resolve `$SKILL_ROOT` in order (first existing `SKILL.md` wins):

1. Cursor: `~/.cursor/skills/headroom`
2. Plugin: `~/.cursor/plugins/local/global-tooling/skills/headroom`
3. Claude Code / GLM Coding Plan: `~/.claude/skills/headroom`
4. Agents hub: `~/.agents/skills/headroom`
5. Codex: `~/.codex/skills/headroom`
6. Antigravity / Gemini: `~/.gemini/config/skills/headroom`
7. OpenCode: `~/.config/opencode/skills/headroom`
8. Kilo Code: `~/.kilo/skills/headroom`
9. Kimi Code: `~/.kimi-code/skills/headroom`

Read and follow `$SKILL_ROOT/SKILL.md`. Also load **cursor-global-tooling** if choosing between Headroom / Ruflo / FCD.

Task: $ARGUMENTS

## Do

1. Confirm Headroom MCP tools exist (`headroom_stats` or attempt compress).
2. On large tool/file/log/JSON output → `headroom_compress`.
3. If a `hash=…` marker needs detail → `headroom_retrieve` (optional `query`).
4. User asks savings → `headroom_stats`.

## Do not

- Compress short replies, tiny JSON, or the single file being edited.
- Invent a compression scheme when MCP is available.
- Use Ruflo for token savings (that is Headroom).

## Ops

```bash
headroom doctor
headroom mcp install --force   # wire MCP into detected agents
headroom proxy                 # :8787 (BYOK / Claude via proxy)
headroom-cursor
```

If MCP tools are missing, say so and ask the user to reload the agent / run `headroom mcp install`.
