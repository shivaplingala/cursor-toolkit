---
name: devops-cloud-platforms
description: >-
  Staff/principal multi-cloud DevOps: AWS, GCP, Azure, Docker, Kubernetes, Terraform, Ansible, CI/CD, SRE, FinOps, platform engineering.
level: staff-principal
---

# DevOps & Cloud Platforms — Staff / Principal

## Platform engineering scope

- Golden paths for app teams (templates, CI, observability baked in)
- Environment promotion: dev → staging → prod with automated gates
- Incident response: runbooks, blameless postmortems, SLO error budgets

## CI/CD checklist

- [ ] Lint, test, security scan, IaC plan on every PR
- [ ] Immutable artifacts; deploy same digest prod as staging
- [ ] Feature flags decouple deploy from release
- [ ] Rollback tested quarterly

## Multi-cloud strategy

- Pick primary cloud per workload class; abstract only at true portability need
- Identity federation; centralized logging sink
- FinOps: tagging policy, budget alerts, rightsizing reviews

## Skill routing

Load `aws-principal`, `gcp-principal`, `azure-principal`, `docker-principal`, `kubernetes-principal`, `terraform-principal`, or `ansible-principal` for depth.

**Upstream:** DevOps Automator, SRE, FinOps personas in agency-agents/engineering.

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-devops-automator.md](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-devops-automator.md)

