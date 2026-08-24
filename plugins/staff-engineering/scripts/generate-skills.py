#!/usr/bin/env python3
"""Generate staff/principal engineering skills. Idempotent."""
from __future__ import annotations

import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
SKILLS = PLUGIN / "skills"

UPSTREAM = "https://github.com/msitarzewski/agency-agents/tree/main/engineering"

COMMON_FOOTER = """
## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [{upstream}]({upstream})
"""


def write_skill(name: str, description: str, body: str, upstream_note: str = UPSTREAM) -> None:
    d = SKILLS / name
    d.mkdir(parents=True, exist_ok=True)
    footer = COMMON_FOOTER.format(upstream=upstream_note)
    content = f"""---
name: {name}
description: >-
  {description}
level: staff-principal
---

{body.strip()}
{footer}
"""
    (d / "SKILL.md").write_text(content, encoding="utf-8")
    print(f"  {name}")


def main() -> int:
    SKILLS.mkdir(parents=True, exist_ok=True)

    # --- Router ---
    router_body = """
# Staff Engineering — Principal / Staff Router

**Level:** Staff / Principal across full-stack JavaScript stacks, AI agent frameworks, polyglot runtimes, and multi-cloud DevOps.

## When to use

Load **`staff-engineering`** first, then the **narrowest** domain skill for the task. Do not load all skills at once.

## Task → skill

| Working on… | Skill |
| ----------- | ----- |
| MERN / MEAN / MEVN product architecture | `fullstack-js-stacks` |
| Python services, data, ML glue | `python-principal` |
| JavaScript (Node, browser, tooling) | `javascript-principal` |
| TypeScript (types, monorepos, APIs) | `typescript-principal` |
| Go services, concurrency, CLIs | `golang-principal` |
| LangChain apps, tools, RAG chains | `langchain-principal` |
| LangGraph state machines, multi-step agents | `langgraph-principal` |
| CrewAI role crews | `crewai-principal` |
| Microsoft AutoGen multi-agent | `autogen-principal` |
| Pick / compare AI frameworks | `ai-agent-frameworks` |
| AWS (Lambda, IAM, VPC, Bedrock…) | `aws-principal` |
| GCP (GKE, Cloud Run, Vertex…) | `gcp-principal` |
| Azure (AKS, Functions, Entra…) | `azure-principal` |
| Containers, images, compose | `docker-principal` |
| K8s workloads, Helm, operators | `kubernetes-principal` |
| IaC modules, state, drift | `terraform-principal` |
| Config management, playbooks | `ansible-principal` |
| Multi-cloud DevOps strategy | `devops-cloud-platforms` |
| End-to-end full-stack + AI + platform | `staff-fullstack-ai-engineer` |

## Agency-agents alignment

Maps to [agency-agents/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering) personas. Local Applaud appendices remain in `agency-engineering/*` when present.

## Iron laws

1. **Design before code** in FCD Phase 2; Ponytail in Phase 4
2. **Security and observability** are non-optional at staff level
3. **Simplest architecture** that meets SLO + team maturity — document scale path
4. **Evidence:** graphify + GitNexus before shared symbol edits in this monorepo
"""
    write_skill(
        "staff-engineering",
        "Staff/principal engineering router: full-stack JS (MERN/MEAN/MEVN), AI frameworks "
        "(LangChain, LangGraph, CrewAI, AutoGen), Python/JS/TS/Go, AWS/GCP/Azure, Docker, "
        "K8s, Terraform, Ansible. Load first, then domain skill.",
        router_body,
    )

    write_skill(
        "staff-fullstack-ai-engineer",
        "Staff/principal full-stack + AI + platform engineer: MERN/MEAN/MEVN, agent frameworks, "
        "polyglot backends, multi-cloud DevOps. Use for cross-cutting system design and technical leadership.",
        """
# Staff Full-Stack + AI Engineer

**Identity:** Staff / Principal — owns end-to-end architecture from UI through APIs, data, agents, and production platform.

## Core competencies

- **Full-stack:** MongoDB + Express + React/Vue/Angular + Node — production auth, caching, real-time, SSR/SPA trade-offs
- **AI systems:** RAG, tool use, multi-agent orchestration (LangChain, LangGraph, CrewAI, AutoGen), evals, guardrails, cost/latency
- **Polyglot:** Python (ML/data), TypeScript (product APIs), Go (high-throughput services), JavaScript (Node ecosystem)
- **Platform:** AWS/GCP/Azure, Docker, Kubernetes, Terraform, Ansible — secure CI/CD, observability, FinOps awareness

## Design checklist

- [ ] User journeys + trust boundaries mapped
- [ ] API contracts (OpenAPI/AsyncAPI) + versioning + idempotency
- [ ] Data model + indexes + migration strategy
- [ ] Agent graph: state, tools, HITL, failure/retry, token budget
- [ ] SLOs, dashboards, alerts, runbooks
- [ ] Threat model: authz, injection, secrets, supply chain
- [ ] Cost model at 1x and 10x load

## Deliverables

Options + verdict, ADR, topology diagram, reliability matrix, observability plan, test strategy (unit + integration + agent evals).
""",
    )

    stacks = """
# Full-Stack JavaScript Stacks — Staff / Principal

**Stacks:** MERN (React), MEVN (Vue), MEAN (Angular) — MongoDB, Express (or Fastify/Nest), Node.js.

## Architecture decisions

| Concern | Staff-level guidance |
| ------- | -------------------- |
| API layer | REST or GraphQL with explicit versioning; BFF when mobile + web diverge |
| Auth | HttpOnly cookies or short-lived JWT + refresh; CSRF for cookie sessions |
| Data | MongoDB schema design, compound indexes, TTL, transactions only when needed |
| Real-time | Socket.io / SSE — scale via Redis adapter; document ordering guarantees |
| Frontend | Code-split routes; SSR (Next/Nuxt) vs SPA — pick for SEO and TTFB |
| State | Server state (TanStack Query / Pinia) vs client — avoid duplicate sources of truth |

## Stack-specific notes

- **MERN:** React 18+ patterns, RSC when on Next.js, avoid prop-drilling — colocate data fetching
- **MEVN:** Vue 3 Composition API, Pinia, Vuetify/headless — match `outlook-admin-ui/AGENTS.md` in Applaud
- **MEAN:** Angular modules/standalone, RxJS lifecycle, strict TS templates

## Reliability

- Rate limits, circuit breakers on external APIs
- Idempotent webhooks (Stripe, etc.)
- Background jobs (BullMQ / SQS) for heavy work off request path

## Security

- Validate all inputs at API boundary; sanitize HTML; CSP headers
- Least-privilege DB users; no secrets in client bundles

## Testing

- API contract tests; critical UI flows E2E; load test hot endpoints before launch
"""
    write_skill(
        "fullstack-js-stacks",
        "Staff/principal MERN, MEVN, MEAN architecture: MongoDB, Express/Fastify/Nest, React/Vue/Angular, "
        "Node.js production patterns, auth, real-time, testing.",
        stacks,
    )

    langs = {
        "python-principal": (
            "Staff/principal Python: async IO, typing, FastAPI/Django, data pipelines, "
            "testing (pytest), packaging, performance, security.",
            """
# Python — Staff / Principal

## Iron laws

- Type hints on public APIs; `mypy` or pyright in CI for libraries/services
- Async for IO-bound; multiprocessing for CPU-bound — profile before optimizing
- Dependencies pinned; scan with `pip-audit` / Dependabot

## Patterns

- FastAPI for APIs; Pydantic v2 models at boundaries
- SQLAlchemy 2.0 / async drivers; connection pooling sized to DB limits
- Structured logging (`structlog`); OpenTelemetry traces
- 12-factor config via env; secrets from vault/SSM — never in repo

## Performance

- Avoid N+1 ORM; `selectinload`; pagination always
- NumPy/pandas vectorization; Polars for ETL at scale
- Memory: generators, chunked reads, explicit `del` only when profiled

## Testing

- pytest + fixtures; property-based for parsers
- Contract tests for HTTP clients; VCR for external APIs
""",
        ),
        "javascript-principal": (
            "Staff/principal JavaScript: Node.js, ESM/CJS interop, event loop, streams, "
            "Express/Fastify, testing (Vitest/Jest), security, performance.",
            """
# JavaScript — Staff / Principal

## Iron laws

- `"use strict"`; prefer `const`; async/await over raw Promise chains
- Validate at boundaries (`zod` / `joi`); never trust `req.body`
- No floating versions in production lockfiles

## Node.js depth

- Event loop phases; avoid blocking sync FS/crypto on hot path
- Streams and backpressure for large payloads
- `worker_threads` for CPU work; cluster only when measured benefit

## Patterns

- Middleware composition; central error handler → stable JSON `error` field
- Graceful shutdown: drain HTTP, close DB pools, SIGTERM handlers

## Browser (when in scope)

- Bundle analysis; lazy routes; avoid layout thrashing
- CSP, sanitize DOM inserts

## Testing

- Vitest/Jest; supertest for HTTP; mock at module boundary not implementation detail
""",
        ),
        "typescript-principal": (
            "Staff/principal TypeScript: strict mode, generics, monorepos, API contracts, "
            "Nest/Fastify/Express typing, frontend TS, build tooling.",
            """
# TypeScript — Staff / Principal

## Iron laws

- `strict: true`; no `any` in product code without `ponytail:` comment + upgrade path
- Shared types in packages; single source for API DTOs
- `unknown` + narrowing at external boundaries

## Architecture

- Monorepo: turborepo/nx — graph-aware builds, shared `tsconfig` bases
- Branded types for IDs; discriminated unions for state machines
- `satisfies` for config objects; const type parameters where useful

## API layer

- Zod/io-ts runtime validation + inferred TS types
- OpenAPI codegen or tRPC for end-to-end contracts

## Testing

- `vitest` with typecheck; `@testing-library` for UI
- Type tests (`expect-type`) for public package APIs
""",
        ),
        "golang-principal": (
            "Staff/principal Go: concurrency, interfaces, error handling, HTTP/gRPC services, "
            "testing, profiling, production operations.",
            """
# Go — Staff / Principal

## Iron laws

- Accept `context.Context` first on IO paths; enforce deadlines
- Wrap errors with `%w`; classify sentinel vs transient
- `go vet`, `staticcheck`, `race` detector in CI

## Concurrency

- Prefer channels for ownership transfer; mutex for shared state — document invariant
- `errgroup` for parallel tasks with cancel
- Worker pools with bounded goroutines — no unbounded `go func()`

## Services

- `net/http` or chi/fiber with middleware: request ID, recover, timeout
- gRPC + protobuf for internal S2S; grpc-gateway for REST edge
- Structured `slog`; RED metrics per handler

## Performance

- `pprof` CPU/heap before micro-optimizing
- `sync.Pool` only when profiled; avoid premature allocation in hot loops

## Testing

- Table-driven tests; `testify` sparingly; integration tags `//go:build integration`
""",
        ),
    }
    for name, (desc, body) in langs.items():
        write_skill(name, desc, body)

    ai_frameworks = {
        "langchain-principal": (
            "Staff/principal LangChain: LCEL, tools, retrievers, agents, memory, callbacks, "
            "production RAG, evals, cost control.",
            """
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
""",
            "https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-ai-engineer.md",
        ),
        "langgraph-principal": (
            "Staff/principal LangGraph: state graphs, checkpoints, human-in-the-loop, "
            "multi-agent workflows, persistence, streaming.",
            """
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
""",
        ),
        "crewai-principal": (
            "Staff/principal CrewAI: agents, tasks, crews, tools, memory, sequential/hierarchical process.",
            """
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
""",
        ),
        "autogen-principal": (
            "Staff/principal Microsoft AutoGen: conversable agents, group chat, code execution, "
            "Azure/OpenAI integration, human proxy patterns.",
            """
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
""",
        ),
    }
    for name, item in ai_frameworks.items():
        desc, body = item[0], item[1]
        upstream = item[2] if len(item) > 2 else UPSTREAM
        write_skill(name, desc, body, upstream)

    write_skill(
        "ai-agent-frameworks",
        "Staff/principal AI agent framework selection and architecture: LangChain, LangGraph, "
        "CrewAI, AutoGen comparison, RAG, evals, guardrails, multi-agent reliability.",
        """
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
""",
        "https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-rag-pipeline-engineer.md",
    )

    clouds = {
        "aws-principal": (
            "Staff/principal AWS: IAM, VPC, Lambda, ECS/EKS, S3, DynamoDB, SQS/SNS, "
            "Bedrock, CloudWatch, Well-Architected, cost optimization.",
            """
# AWS — Staff / Principal

## Iron laws

- IAM least privilege; no `*` actions on `*` resources in prod
- Encrypt at rest (KMS) and in transit (TLS 1.2+)
- Multi-AZ for tier-1; backups tested restore

## Serverless (Applaud default)

- Lambda: memory vs duration trade-off; provisioned concurrency only when measured
- API Gateway + authorizer patterns; avoid per-route permission sprawl
- SQS visibility timeout > Lambda timeout; DLQ on all async paths
- DynamoDB: single-table when justified; GSIs cost-aware; conditional writes for locks

## Observability

- Structured logs → CloudWatch; X-Ray or ADOT tracing
- Alarms on user symptoms (5xx rate, queue age) not only CPU

## Security

- Secrets Manager / SSM; no keys in env plaintext in CI logs
- VPC endpoints for private AWS API access

**Applaud:** pair with `aws-diagnose-read` for incidents; SST deploy-time config.
""",
            "https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-devops-automator.md",
        ),
        "gcp-principal": (
            "Staff/principal GCP: IAM, VPC, GKE, Cloud Run, Cloud SQL, Pub/Sub, "
            "Vertex AI, Cloud Monitoring, FinOps.",
            """
# GCP — Staff / Principal

## Iron laws

- Organization policies; workload identity over long-lived keys
- VPC-SC for sensitive data; private Google access

## Compute

- Cloud Run for stateless HTTP; min instances for cold-start SLO
- GKE: node pools per workload class; HPA + cluster autoscaler

## Data & AI

- Cloud SQL HA; connection pooling (AlloyDB auth proxy)
- Vertex AI: regional endpoints; quota planning; CMEK when required

## Observability

- Cloud Logging structured; Error Reporting; SLO burn alerts
""",
        ),
        "azure-principal": (
            "Staff/principal Azure: Entra ID, ARM/Bicep, AKS, Functions, App Service, "
            "Azure OpenAI, Monitor, landing zones.",
            """
# Azure — Staff / Principal

## Iron laws

- Entra ID RBAC; managed identities; Conditional Access for humans
- Subscription segmentation; policy assignments at MG scope

## Compute

- AKS: Azure CNI, workload identity, AGIC or service mesh
- Functions: consumption vs premium plan for VNet + always-warm

## AI

- Azure OpenAI: PTU vs pay-go; content safety; private endpoints

## Observability

- Application Insights + Log Analytics; distributed tracing correlation
""",
        ),
        "docker-principal": (
            "Staff/principal Docker: multi-stage builds, image security, compose, "
            "registry, rootless, supply chain.",
            """
# Docker — Staff / Principal

## Images

- Multi-stage builds; distroless or slim base; non-root USER
- Pin digests in prod; scan with Trivy/Grype in CI
- `.dockerignore`; layer cache discipline

## Runtime

- Read-only rootfs where possible; drop capabilities
- Healthchecks; graceful stop (`STOPSIGNAL`, preStop hooks in K8s)
- Resource limits always set in orchestrators

## Compose (dev)

- Service dependencies with health conditions; secrets via files not env in git
""",
        ),
        "kubernetes-principal": (
            "Staff/principal Kubernetes: workloads, networking, security, GitOps, "
            "Helm, operators, autoscaling, troubleshooting.",
            """
# Kubernetes — Staff / Principal

## Iron laws

- Requests/limits on every container; PDB for tier-1
- NetworkPolicy default-deny + explicit allow
- RBAC least privilege; no cluster-admin for apps

## Workloads

- Deployments + rolling update strategy; readiness ≠ liveness
- Jobs/CronJobs with backoff limits; idempotent job design
- HPA on CPU/memory or custom metrics; VPA cautiously

## GitOps

- Helm or Kustomize; semver charts; drift detection
- SealedSecrets / ESO for secrets; never plain Secrets in git

## Debugging

- `kubectl debug` ephemeral containers; events + logs + traces triad
""",
            "https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-sre.md",
        ),
        "terraform-principal": (
            "Staff/principal Terraform: modules, state, workspaces, IAM wiring, "
            "policy-as-code, drift, multi-env promotion.",
            """
# Terraform — Staff / Principal

## Iron laws

- Remote state + locking; no local state in team repos
- Modules with versioned releases; document inputs/outputs
- `terraform plan` required in CI; apply gated

## Structure

- Env separation: workspaces or directory per env — same modules, different tfvars
- IAM in dedicated modules; avoid inline policies sprawl
- `moved` blocks for refactors; import for brownfield

## Safety

- `prevent_destroy` on stateful resources; `-target` only in break-glass
- Sentinel/OPA/Checkov in pipeline

**Applaud note:** SST/Ion may supersede raw TF for app stacks — use TF for shared platform when ADR says so.
""",
        ),
        "ansible-principal": (
            "Staff/principal Ansible: inventories, roles, idempotency, vault, "
            "molecule testing, rolling updates.",
            """
# Ansible — Staff / Principal

## Iron laws

- Idempotent tasks; check mode in CI where possible
- Roles with defaults in `defaults/`; secrets in Ansible Vault
- Pin collections; `ansible-lint` in pipeline

## Patterns

- Dynamic inventory for cloud (AWS/GCP/Azure plugins)
- Handlers for restart-on-change only
- Serial/strategy for rolling updates; health check after batch

## vs Terraform

- TF = desired state infra; Ansible = config on existing VMs / bootstrap — compose both in platform ADR
""",
        ),
    }
    for name, (desc, body, *rest) in clouds.items():
        upstream = rest[0] if rest else UPSTREAM
        write_skill(name, desc, body, upstream)

    write_skill(
        "devops-cloud-platforms",
        "Staff/principal multi-cloud DevOps: AWS, GCP, Azure, Docker, Kubernetes, "
        "Terraform, Ansible, CI/CD, SRE, FinOps, platform engineering.",
        """
# DevOps & Cloud Platforms — Staff / Principal

## Platform engineering scope

- Golden paths for app teams (templates, CI, observability baked in)
- Environment promotion: dev → staging → prod with automated gates
- Incident response: runbooks, blameless postmortems, SLO error budgets

## CI/CD checklist

- [ ] Lint, test, security scan, IaC plan on every PR
- [ ] Immutable artifacts; deploy same digest prod as staging
- [ ] Feature flags decouple deploy from release
- [ ] Rollback tested quarterly

## Multi-cloud strategy

- Pick primary cloud per workload class; abstract only at true portability need
- Identity federation; centralized logging sink
- FinOps: tagging policy, budget alerts, rightsizing reviews

## Skill routing

Load `aws-principal`, `gcp-principal`, `azure-principal`, `docker-principal`, `kubernetes-principal`, `terraform-principal`, or `ansible-principal` for depth.

**Upstream:** DevOps Automator, SRE, FinOps personas in agency-agents/engineering.
""",
        "https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-devops-automator.md",
    )

    print(f"Generated skills under {SKILLS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
