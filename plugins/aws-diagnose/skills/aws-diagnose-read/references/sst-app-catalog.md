# App catalog — SST deployables

| Path | SST name | Primary domains |
| ---- | -------- | ----------------- |
| `apps/conversation-service` | conversation-service | Chat API, WebSocket, traces, agent tools, attachments |
| `apps/channels/outlook` | outlook-channel | Email ingest, Graph, outbound reply |
| `apps/channels/slack` | slack-bot | Slack channel |
| `apps/channels/teams` | teams-bot | Teams channel |
| `apps/workflow` | workflow | SFN, run-agent, workflow APIs |
| `apps/tenant-management` | tenant-management | Tenant bus, **channel messaging queue**, quota |
| `apps/identity-management` | identity-management | Authorizer, Cognito, WebSocket connections |
| `apps/case-management` | case-management | Cases, case portal API |
| `apps/knowledge` | knowledge-engine | KB pipeline, ingestion |
| `apps/connectors/knowledge/sharepoint` | sharepoint-connector | SharePoint sync |
| `apps/analytics` | analytics | Athena, filters API |
| `apps/docgen` | docgen | Document generation |
| `apps/attachment-converter` | attachment-converter | Attachment conversion |
| `infra` | infra | Domain, DB secret, VPC, shared foundation |

## Common cross-app flows

| Symptom domain | Apps to scan |
| -------------- | ------------ |
| Email lag / duplicate | conversation-service, channels/outlook, workflow, tenant-management |
| Web vs email content | conversation-service, channels/outlook |
| Auth / 403 on API | identity-management, conversation-service |
| Workflow step failure | workflow, conversation-service |
| Queue backlog | tenant-management, channels/outlook |

## Key SSM publishers

| SSM prefix | Owner app |
| ---------- | --------- |
| `/<stage>/messaging/*` | tenant-management |
| `/<stage>/tenant-management/*` | tenant-management |
| `/<shared>/database/*` | infra |
| `/<stage>/conversation-service/*` | conversation-service |
| `/<stage>/outlook/*` | channels/outlook |
| `/<stage>/authorizer/*` | identity-management |
