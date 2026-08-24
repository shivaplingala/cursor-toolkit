---
name: javascript-principal
description: >-
  Staff/principal JavaScript: Node.js, ESM/CJS interop, event loop, streams, Express/Fastify, testing (Vitest/Jest), security, performance.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

