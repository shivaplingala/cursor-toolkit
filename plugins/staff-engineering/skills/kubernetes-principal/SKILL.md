---
name: kubernetes-principal
description: >-
  Staff/principal Kubernetes: workloads, networking, security, GitOps, Helm, operators, autoscaling, troubleshooting.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-sre.md](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-sre.md)

