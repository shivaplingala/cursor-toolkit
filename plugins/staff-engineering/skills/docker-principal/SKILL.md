---
name: docker-principal
description: >-
  Staff/principal Docker: multi-stage builds, image security, compose, registry, rootless, supply chain.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

