---
name: aws-principal
description: >-
  Staff/principal AWS: IAM, VPC, Lambda, ECS/EKS, S3, DynamoDB, SQS/SNS, Bedrock, CloudWatch, Well-Architected, cost optimization.
level: staff-principal
---

# AWS — Staff / Principal

## Iron laws

- IAM least privilege; no `*` actions on `*` resources in prod
- Encrypt at rest (KMS) and in transit (TLS 1.2+)
- Multi-AZ for tier-1; backups tested restore

## Serverless (Applaud default)

- Lambda: memory vs duration trade-off; provisioned concurrency only when measured
- API Gateway + authorizer patterns; avoid per-route permission sprawl
- SQS visibility timeout > Lambda timeout; DLQ on all async paths
- DynamoDB: single-table when justified; GSIs cost-aware; conditional writes for locks

## Observability

- Structured logs → CloudWatch; X-Ray or ADOT tracing
- Alarms on user symptoms (5xx rate, queue age) not only CPU

## Security

- Secrets Manager / SSM; no keys in env plaintext in CI logs
- VPC endpoints for private AWS API access

**Applaud:** pair with `aws-diagnose-read` for incidents; SST deploy-time config.

## FCD / delivery integration

- **Phase 2 design:** load this skill + `staff-engineering` router; pair with `full-cycle-delivery` or `fcd-v2`
- **Phase 4 implement:** Ponytail + domain implementer (`backend-implementer`, `frontend-implementer`); GitNexus on shared symbols
- **Deliverables:** options table, ADR when structural, failure modes, open questions — no silent assumptions

**Upstream personas:** [https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-devops-automator.md](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-devops-automator.md)

