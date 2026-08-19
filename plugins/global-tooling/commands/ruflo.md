---
name: ruflo
description: >-
  Multi-agent orchestration via Ruflo MCP (swarms, memory, agents). Use when
  the user wants coordinated multi-agent work, cross-session memory, or
  swarm/hive/autopilot. Not for one-shot edits or token savings (use Headroom).
---

# /ruflo — multi-agent orchestration

Resolve `$SKILL_ROOT` in order (first existing `SKILL.md` wins):

1. Cursor: `~/.cursor/skills/ruflo`
2. Plugin: `~/.cursor/plugins/local/global-tooling/skills/ruflo`
3. Claude Code / GLM Coding Plan: `~/.claude/skills/ruflo`
4. Agents hub: `~/.agents/skills/ruflo`
5. Codex: `~/.codex/skills/ruflo`
6. Antigravity / Gemini: `~/.gemini/config/skills/ruflo`
7. OpenCode: `~/.config/opencode/skills/ruflo`
8. Kilo Code: `~/.kilo/skills/ruflo`
9. Kimi Code: `~/.kimi-code/skills/ruflo`

Read and follow `$SKILL_ROOT/SKILL.md`. Also load **cursor-global-tooling** if choosing between Headroom / Ruflo / FCD.

Task: $ARGUMENTS

## Do

1. Prefer the host’s built-in Task/subagent for simple parallel work.
2. Escalate to Ruflo when shared memory / topology / multi-agent consensus is needed.
3. Start small: `memory_search` / `memory_store` → `swarm_init` (hierarchical, maxAgents ≤5) → `agent_spawn` / `agent_execute` → `swarm_status` → `swarm_shutdown`.
4. State lives in `~/.ruflo` — never `ruflo init` inside an open repo unless the user wants project-local files.

## Do not

- Use Ruflo for one-shot edits or token compression (use Headroom).
- Dump the full 300+ tool catalog into the plan.
- Create project-local `.claude-flow/` / `.mcp.json` for Ruflo unless asked.

## Ops

```bash
ruflo --version
ruflo doctor
cd ~/.ruflo && ruflo status
ruflo-cursor
```

If MCP tools are missing, say so and ask the user to reload the agent / ensure `ruflo` is in MCP config (Cursor: `~/.cursor/mcp.json`).
