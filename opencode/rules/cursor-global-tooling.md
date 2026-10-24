
# Global tooling — pick and use

Installs are user-global. Load skill **cursor-global-tooling** for full how-to.

| Need | Use | How |
|------|-----|-----|
| Large tool dumps / context / tokens | **Headroom** | MCP `headroom_compress` / `retrieve` / `stats` |
| Multi-agent swarm / shared memory | **Ruflo** | MCP `swarm_init`, `agent_*`, `memory_*`; state `~/.ruflo` |
| Plan→build→verify→ship with gates | **full-cycle-delivery** | `/full-cycle-delivery` or skill; grill-me → grill-with-docs → plan-review to 0 → plan approval → review-fix to 0 |

**Check then use:** if MCP/skill missing, say so and suggest reload. Do not invent substitutes.

**Do not:** `ruflo init` in a workspace unless asked; skip FCD plan gate; use Ruflo for one-shot edits; use Headroom on tiny outputs.
