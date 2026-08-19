# Playbook: aws-infra

Research type: `aws-infra` | `config-only`

SST stacks, IAM, queues, API Gateway splits, secrets/SSM strategy — infrastructure design without feature logic.

## Checklist

- [ ] SST stack ownership (`tenant-management` vs channel app vs shared packages)
- [ ] IAM least privilege table (actions + resource patterns)
- [ ] API Gateway integration cap (~300 per HTTP API) — split strategy if near limit
- [ ] SSM shared vs personal stage resolution (`getSharedResourceStage()` pattern)
- [ ] Secrets Manager recovery-window behavior (Outlook `secrets.ts` pattern)
- [ ] Deploy-time vs runtime config — prefer deploy-time per AGENTS.md
- [ ] EventBridge bus, SQS DLQ, Lambda concurrency if relevant
- [ ] Cross-stack references and SSM export paths
- [ ] `scan_sst.py` discovery for existing resources (read-only)
- [ ] Cost and quota notes
- [ ] Rollback / destroy considerations

## Report emphasis

- Table mapping **resource → SST file → stack name pattern**
- Explicit IAM policy skeleton (actions only, no account-specific ARNs)
- When to use shared stage resources vs personal stage overrides

## Sub-agent focus

| Sub-agent | Extra focus |
| --------- | ----------- |
| external-docs | AWS service limits, SST docs |
| github-samples | Repo SST patterns; aws-samples for edge cases |
| aws-config-catalog | Primary — full inventory template |
| codebase | Existing stack files, learned workspace facts |

## Optional live evidence

If approaching production limits, recommend `aws-diagnose-read` appendix to count live integrations — intake must approve.
