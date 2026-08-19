---
name: cursor-global-tooling
description: >-
  Router and usage guide for globally installed Cursor tooling: Headroom
  (context compression), Ruflo (multi-agent orchestration), and
  full-cycle-delivery (gated plan→build→verify→ship). Use when choosing which
  tool to invoke, when the user mentions Headroom/Ruflo/FCD/full-cycle, or when
  deciding compress vs swarm vs delivery pipeline.
---

# Cursor global tooling (Headroom · Ruflo · FCD)

All three are **user-global** (`~/.cursor/…`), not tied to one workspace.

## Decision tree (check first, then use)

```text
Need cheaper/longer context on large tool dumps?
  → Headroom MCP (compress / retrieve / stats)

Need multi-agent swarm / cross-session memory / hive coordination?
  → Ruflo MCP (swarm_init, agent_spawn, memory_* …)
  → Skip if one Cursor Task / single agent is enough

Need gated delivery (plan approval → implement → dual review → ship)?
  → /full-cycle-delivery or skill full-cycle-delivery
  → Especially for serverless-monorepo features/channels/infra
```

They **stack**: Ruflo/FCD can produce fat outputs → Headroom can compress them. They do **not** replace each other.

## 1. Headroom — context compression

| | |
|--|--|
| **What** | Compress tool outputs/logs/JSON before reasoning; reversible via CCR |
| **When** | Large dumps (grep floods, logs, JSON arrays), context pressure, token cost |
| **When not** | Short replies, tiny JSON, the single file you are editing |
| **MCP** | Server `user-headroom` / `headroom` |
| **Tools** | `headroom_compress`, `headroom_retrieve`, `headroom_stats` |
| **CLI** | `headroom`, `headroom-cursor`, `headroom doctor`, `headroom proxy` |
| **Skill** | `~/.cursor/skills/headroom/` |

**How to use (model):**

1. Confirm tools exist (call `headroom_stats` or attempt compress).
2. On large tool/file output → `headroom_compress` with that content.
3. Reason on compressed text; if a `hash=…` marker needs detail → `headroom_retrieve`.
4. User asks savings → `headroom_stats`.

**Limits:** Default Cursor models use **MCP only** (no HTTP proxy). BYOK OpenAI Base URL `http://127.0.0.1:8787/v1` only if proxy is up (`headroom-cursor`). Telemetry off.

## 2. Ruflo — multi-agent harness

| | |
|--|--|
| **What** | Swarms, specialized agents, persistent memory (MCP + CLI) |
| **When** | Multi-role delivery, shared memory search, explicit swarm/hive ask |
| **When not** | One-shot edits, simple Q&A, token savings (use Headroom) |
| **MCP** | Server `user-ruflo` / `ruflo` (~300 tools) |
| **Start small** | `memory_search`, `memory_store`, `swarm_init`, `agent_spawn`, `agent_execute`, `swarm_status`, `swarm_shutdown` |
| **CLI** | `ruflo`, `ruflo-cursor`; state in `~/.ruflo` |
| **Skill** | `~/.cursor/skills/ruflo/` |

**How to use (model):**

1. Prefer Cursor **Task** for simple parallel work.
2. Escalate to Ruflo when shared memory / topology / multi-agent consensus is needed.
3. `swarm_init` with `topology: hierarchical`, modest `maxAgents` (≤5 unless asked).
4. Spawn/execute agents; search memory before reinventing patterns.
5. `swarm_shutdown` when done.
6. **Never** `ruflo init` inside an open repo unless user wants project-local files.

**Limits:** Claude Code hooks do not auto-run in Cursor — orchestration is **opt-in via MCP/CLI**.

## 3. Full-cycle-delivery — gated ship pipeline

| | |
|--|--|
| **What** | Intake → research → grill → plan approval → implement → dual review (coding+impact) to 0 findings → verify → ship |
| **When** | Features, channels, packages, workflow, infra, non-trivial bugfixes; user wants plan gate |
| **When not** | Tiny drive-by edits with no plan/verify expectation |
| **Invoke** | `/full-cycle-delivery` or load skill `full-cycle-delivery` |
| **Plugin** | `~/.cursor/plugins/local/full-cycle-delivery/` (v1.2+) |
| **Skill** | `~/.cursor/skills/full-cycle-delivery` → plugin |
| **Deps** | `grill-me`, `grill-with-docs`, `research-agent` (also under `~/.cursor/skills/`) |

**How to use (model):**

1. Resolve `$SKILL_ROOT`: plugin → `~/.cursor/skills/full-cycle-delivery` → workspace `.claude/skills/…`
2. Read `$SKILL_ROOT/SKILL.md`; classify work type; open matching `playbooks/*.md`
3. Phases 2–3: **grill-me** then **grill-with-docs**; stop for **human plan approval**
4. Phase 4+: implementer → `verify-scope` (in serverless-monorepo) → coding + impact review-fix until `FINDING_COUNT: 0`
5. No autonomous prod deploy / PR merge

**Repo paths** (when workspace is serverless-monorepo): `scripts/verify-scope.sh`, `docs/plans/TEMPLATE.md`, `skills-agents-autos-plans/FULL-CYCLE-DELIVERY-PLAN.md`.

## Accessibility checklist (if something fails)

```bash
# Headroom
headroom --version && headroom doctor
curl -sf http://127.0.0.1:8787/health   # proxy (systemd: headroom-proxy)
systemctl --user status headroom-proxy
headroom-cursor

# Ruflo
ruflo --version
ruflo-cursor
# MCP cwd must be ~/.ruflo

# FCD
test -f ~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery/SKILL.md
ls ~/.cursor/skills/full-cycle-delivery/playbooks | head
```

In-session: MCP servers appear as `user-headroom` and `user-ruflo`. If missing → ask user to **reload Cursor / MCP**.

## Anti-patterns

- Running `ruflo init` or writing `.claude-flow/` into a random project for “global” setup
- Using Ruflo for a one-line fix
- Using Headroom on tiny snippets (noop / waste)
- Skipping FCD grill + plan approval when the user asked for full-cycle delivery
- Claiming FCD done without fresh verify / review-fix output
