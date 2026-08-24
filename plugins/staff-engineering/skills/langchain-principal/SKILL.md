---
name: langchain-principal
description: >-
  Staff/principal LangChain: LCEL, tools, retrievers, agents, memory, callbacks, production RAG, evals, cost control.
level: staff-principal
---

# LangChain — Staff / Principal

## When LangChain vs lighter

- Multi-provider LLM + tool + retriever composition → LangChain/LCEL
- Single Bedrock call with one tool → stdlib/SDK may suffice (Ponytail)

## Architecture

- LCEL chains; RunnableParallel for fan-out; fallbacks for model outage
- Tools: strict JSON schemas; validate tool args; cap tool loop iterations
- Retrievers: hybrid search; rerankers; cite sources in user-facing output

## Production

- Callbacks for token/cost tracing; LangSmith or OTel export
- Cache embeddings; batch where provider allows
- Prompt templates versioned in git; regression eval set before prompt changes

## Security

- Sanitize retrieved docs (prompt injection via RAG)
- Secrets via env; never log prompts with PII

## Evals

- Golden set + LLM-as-judge sparingly; deterministic checks for tool routing

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-ai-engineer.md](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-ai-engineer.md)

