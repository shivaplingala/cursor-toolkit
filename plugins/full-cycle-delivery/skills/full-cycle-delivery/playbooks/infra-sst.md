# Playbook: infra-sst

**Work type:** `infra-sst`

## Preferences (root AGENTS.md)

- Deploy-time config over runtime SSM/Secrets writes
- Secrets Manager recovery-window handling (Outlook `secrets.ts` pattern)
- API Gateway integration cap — split APIs if needed

## Checklist

- [ ] SST stack ownership (`tenant-management` vs channel app)
- [ ] IAM least privilege table in plan
- [ ] `sst deploy --stage <personal>` smoke — never prod without human
- [ ] Research-agent or `aws-infra` playbook for new resources

## Persona

DevOps Automator (SST appendix — ignore upstream K8s/Terraform templates)
