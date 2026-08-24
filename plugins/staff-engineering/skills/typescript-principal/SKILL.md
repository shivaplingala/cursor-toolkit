---
name: typescript-principal
description: >-
  Staff/principal TypeScript: strict mode, generics, monorepos, API contracts, Nest/Fastify/Express typing, frontend TS, build tooling.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

