---
name: autogen-principal
description: >-
  Staff/principal Microsoft AutoGen: conversable agents, group chat, code execution, Azure/OpenAI integration, human proxy patterns.
level: staff-principal
---

# AutoGen — Staff / Principal

## Patterns

- `AssistantAgent` + `UserProxyAgent` for HITL flows
- GroupChat with bounded rounds and speaker selection function
- Code execution in Docker sandbox only — never host executor in prod

## Azure / enterprise

- Entra ID auth to Azure OpenAI; managed identity over API keys
- Log redaction; content filtering policies

## Reliability

- Max turns; terminate on tool success predicate
- Persist conversation state for long runs

## vs LangGraph/CrewAI

- AutoGen shines in conversational multi-agent prototyping → harden with explicit graphs for prod

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

