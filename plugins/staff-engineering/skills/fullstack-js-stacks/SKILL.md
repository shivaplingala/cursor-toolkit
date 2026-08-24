---
name: fullstack-js-stacks
description: >-
  Staff/principal MERN, MEVN, MEAN architecture: MongoDB, Express/Fastify/Nest, React/Vue/Angular, Node.js production patterns, auth, real-time, testing.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

