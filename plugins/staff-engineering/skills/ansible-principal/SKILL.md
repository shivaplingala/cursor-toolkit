---
name: ansible-principal
description: >-
  Staff/principal Ansible: inventories, roles, idempotency, vault, molecule testing, rolling updates.
level: staff-principal
---

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

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/tree/main/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering)

