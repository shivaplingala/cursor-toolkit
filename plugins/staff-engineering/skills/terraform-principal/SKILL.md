---
name: terraform-principal
description: >-
  Staff/principal Terraform: modules, state, workspaces, IAM wiring, policy-as-code, drift, multi-env promotion.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

