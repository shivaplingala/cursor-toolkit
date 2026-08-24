---
name: langgraph-principal
description: >-
  Staff/principal LangGraph: state graphs, checkpoints, human-in-the-loop, multi-agent workflows, persistence, streaming.
level: staff-principal
---

# LangGraph — Staff / Principal

## Core model

- StateGraph with typed state; reducers for merge semantics
- Nodes = pure-ish steps; edges = routing functions; avoid god-nodes
- Checkpointers (Postgres/SQLite) for durable runs and HITL resume

## Patterns

- Supervisor vs swarm; explicit termination conditions
- Subgraphs for reusable phases; compile with interrupt before sensitive tools
- Stream `values` + `updates` for UX; backpressure on slow consumers

## Reliability

- Retry transient LLM errors with backoff; idempotent side-effect nodes
- DLQ or dead-letter state for unrecoverable branches
- Max step count guard

## Observability

- Trace each node; attribute tokens per node; SLO on p95 graph latency

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

