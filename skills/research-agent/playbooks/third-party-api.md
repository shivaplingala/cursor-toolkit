# Playbook: third-party-api

Research type: `third-party-api`

External API integration that is **not** a messaging channel (connectors, knowledge sources, billing, etc.).

## Checklist

- [ ] API product and auth model (API key, OAuth2, mTLS)
- [ ] Rate limits, pagination, idempotency keys
- [ ] Official SDK vs raw HTTP in Node/Lambda
- [ ] Webhooks from provider (if any) — verification method
- [ ] Data residency / PII handling
- [ ] Retry and DLQ strategy for Lambda consumers
- [ ] Where it lives in monorepo (`apps/connectors/`, `packages/apis`, etc.)
- [ ] Existing similar connector (SharePoint, etc.)
- [ ] Secrets and env var shapes — SST deploy-time binding
- [ ] IAM if AWS intermediary (S3, Secrets Manager, VPC endpoint)
- [ ] Test strategy: sandbox credentials, contract tests

## Report emphasis

- Auth flow diagram (ASCII or mermaid)
- Error handling alignment with `apis` retry patterns if applicable
- Configuration inventory for provider portal + AWS

## Sub-agent focus

| Sub-agent | Extra focus |
| --------- | ----------- |
| external-docs | Primary — API reference, auth, limits |
| github-samples | Official SDK repo + `apps/connectors/` patterns |
| aws-config-catalog | Secrets, IAM, VPC if needed |
| codebase | Connector architecture, tool executor patterns |
