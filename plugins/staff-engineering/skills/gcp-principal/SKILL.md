---
name: gcp-principal
description: >-
  Staff/principal GCP: IAM, VPC, GKE, Cloud Run, Cloud SQL, Pub/Sub, Vertex AI, Cloud Monitoring, FinOps.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

