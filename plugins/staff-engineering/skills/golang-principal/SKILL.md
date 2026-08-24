---
name: golang-principal
description: >-
  Staff/principal Go: concurrency, interfaces, error handling, HTTP/gRPC services, testing, profiling, production operations.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

