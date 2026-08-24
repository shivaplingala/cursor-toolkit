---
name: ai-agent-frameworks
description: >-
  Staff/principal AI agent framework selection and architecture: LangChain, LangGraph, CrewAI, AutoGen comparison, RAG, evals, guardrails, multi-agent reliability.
level: staff-principal
---

# AI Agent Frameworks — Staff / Principal

## Selection matrix

| Need | Prefer |
| ---- | ------ |
| Linear RAG + tools | LangChain LCEL |
| Stateful workflows, HITL, checkpoints | LangGraph |
| Role-based team simulation | CrewAI |
| Conversational multi-agent + code exec (sandboxed) | AutoGen |
| Applaud production orchestrator | Existing `conversation-service` + SFN — don't rewrite in framework without ADR |

## Cross-framework iron laws

- **Evals before ship:** golden tasks + regression on prompt/tool changes
- **Budget:** token caps, model routing (small model for classify, large for synthesize)
- **Guardrails:** input/output filters; tool allowlists; human approval for destructive ops
- **Observability:** trace_id per run; cost per tenant/session

## RAG pipeline (staff checklist)

- Chunk strategy + metadata filters; hybrid retrieval; rerank
- Injection defense on retrieved content
- Freshness / sync jobs for knowledge bases

## Handoff

Load framework-specific skill (`langchain-principal`, etc.) after this router row matches.

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-rag-pipeline-engineer.md](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-rag-pipeline-engineer.md)

