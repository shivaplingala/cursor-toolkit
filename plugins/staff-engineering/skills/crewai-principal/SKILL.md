---
name: crewai-principal
description: >-
  Staff/principal CrewAI: agents, tasks, crews, tools, memory, sequential/hierarchical process.
level: staff-principal
---

# CrewAI — Staff / Principal

## Modeling

- One agent = role + goal + backstory — keep backstory factual not fluffy
- Tasks with explicit `expected_output` and context dependencies
- Hierarchical process only when manager agent adds real routing value

## Tools

- Thin wrappers over APIs; timeouts; structured return types
- Shared tool pool; rate-limit per tenant

## Production gaps to address

- Built-in memory → externalize (vector DB) for multi-tenant
- Add eval harness; CrewAI verbosity off in prod
- Containerize; horizontal scale via queue + worker pattern

## Security

- Tool allowlists per crew; sandbox code execution never on prod paths without isolation

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

