# Configuration inventory checklist

Every report **must** include applicable subsections. Mark **N/A** with one-line reason if not relevant.

**Never paste secret values.** Document names and shapes only.

## AWS

### IAM (least privilege)

| Action | Resource ARN pattern | Purpose | Doc link |
| ------ | -------------------- | ------- | -------- |

### SSM Parameter Store

| Path pattern | Purpose | Publisher (stack/script) | Consumer |
| ------------ | ------- | ------------------------ | -------- |

### Secrets Manager

| Secret name pattern | Rotation | Recovery-window notes | Consumer |
| ------------------- | -------- | --------------------- | -------- |

### Lambda environment variables

| Name | Required | Source (SSM/secret/env) | Purpose |
| ---- | -------- | ------------------------- | ------- |

### SQS / SNS / EventBridge

| Resource | Name pattern | DLQ | Batch size / rules |
| -------- | ------------ | --- | ------------------ |

### API Gateway

| API | Routes | Authorizer | Integration limit notes |
| --- | ------ | ---------- | ----------------------- |

### DynamoDB

| Table | Keys | TTL | Purpose |
| ----- | ---- | --- | ------- |

### KMS

| Key alias/pattern | Grants | Purpose |
| ----------------- | ------ | ------- |

### VPC / security groups

| Resource | Purpose |
| -------- | ------- |

### Service quotas

| Service | Quota | Known limit | Mitigation |
| ------- | ----- | ----------- | ---------- |

### SST stacks / files

| Stack / file | Resources provisioned | Stage vs shared |
| ------------ | --------------------- | --------------- |

**defaults:**

- Prefer deploy-time provisioning in SST over runtime writes to SSM/Secrets
- Channel queues: `apps/tenant-management/sst/stacks/messaging-queue-stack.ts`
- Personal vs shared stage: see `aws-diagnose-read/references/sst-stage-resolution.md`

## Third-party portals

| Portal | Setting | Value shape (not value) | Doc link | Sandbox vs prod |
| ------ | ------- | ----------------------- | -------- | --------------- |

### Portal quick reference

| Portal | Typical settings |
| ------ | ---------------- |
| Microsoft Entra / Graph | App registration, API permissions, redirect URIs, webhooks |
| Meta WhatsApp | Business account, phone number ID, webhook verify token, templates |
| Twilio | Account SID, messaging service SID, webhook URLs |
| Slack / Teams | Bot app, OAuth scopes, event subscriptions, manifest |
| OpenAI / Anthropic | API keys, assistant IDs, platform bot registration |

## Application configuration

| Variable | Required | Example shape | `.env.example` path to update |
| -------- | -------- | ------------- | ----------------------------- |

List target `.env.example` paths in report; do not commit secrets.

## Discovery tools (read-only)

| Need | Tool |
| ---- | ---- |
| Existing SST resources | `python .claude/skills/aws-diagnose-read/scripts/scan_sst.py --stage STAGE --search KEYWORD --json` |
| IAM action names | AWS Knowledge MCP + official IAM reference |
| Live account values | `aws-diagnose-read` appendix only — not default for pre-build research |
