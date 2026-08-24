---
name: python-principal
description: >-
  Staff/principal Python: async IO, typing, FastAPI/Django, data pipelines, testing (pytest), packaging, performance, security.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

