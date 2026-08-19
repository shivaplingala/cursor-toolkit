---
name: ruflo
description: >-
  Multi-agent orchestration via Ruflo MCP (swarms, memory, agents, hooks).
  Use when the user wants coordinated multi-agent work, persistent cross-session
  memory search, hive-mind/swarm init, or explicitly mentions Ruflo/claude-flow.
  Do NOT use for one-shot edits or simple single-agent fixes.
---

# Ruflo (Cursor, global)

Ruflo is installed **user-global**. Runtime/config lives in `~/.ruflo` — never run `ruflo init` inside a project workspace unless the user explicitly asks for project-local install.
See also global router: skill **cursor-global-tooling**.

## Surfaces

| Surface | Path / command |
|---------|----------------|
| CLI | `ruflo` (global npm) |
| MCP | Cursor server `ruflo` → `ruflo mcp start` (cwd `~/.ruflo`) |
| Home state | `~/.ruflo/.claude-flow/` |
| Helper | `ruflo-cursor` |

## When to use

Use Ruflo MCP when:
- Multi-role delivery (architect / coder / tester / reviewer in parallel)
- Need `memory_search` / `memory_store` across sessions
- User asks for swarm / hive-mind / autopilot

Do **not** use when:
- Single-file bugfix, quick Q&A, or one Cursor Task is enough
- Token savings is the goal — use Headroom instead

## Preferred MCP tools (start small)

1. `memory_search` / `memory_store` — retrieve or save patterns
2. `swarm_init` — topology `hierarchical`, modest `maxAgents` (≤5 unless asked)
3. `agent_spawn` / `agent_execute` — specialized workers
4. `swarm_status` / `agent_list` — inspect before spawning more
5. `swarm_shutdown` — clean up when done

Avoid dumping the full 300+ tool catalog into the plan. Prefer Cursor’s built-in Task tool for simple parallel work; escalate to Ruflo when shared memory / hive coordination is required.

## Cursor limits

- Ruflo’s Claude Code hooks/plugins do **not** auto-run inside Cursor Agent.
- Orchestration is **opt-in via MCP tools** (and CLI in a terminal).
- Do not create `.claude-flow/`, `.mcp.json`, or `CLAUDE.md` in the open repo for Ruflo unless the user requests a project-local init.

## Ops

```bash
ruflo --version
ruflo doctor
cd ~/.ruflo && ruflo status
ruflo-cursor   # print Cursor wiring + health hints
```
