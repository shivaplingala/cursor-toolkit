# Provider index — starting URLs

Use as seeds for `external-docs` sub-agent. Prefer latest stable API docs; note version on fetch.

## AWS

| Topic | URL |
| ----- | --- |
| IAM actions reference | https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html |
| Lambda | https://docs.aws.amazon.com/lambda/latest/dg/wait/welcome.html |
| API Gateway HTTP APIs | https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html |
| API Gateway quotas | https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-execution-service-limits.html |
| SQS | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html |
| EventBridge | https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html |
| DynamoDB | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html |
| Secrets Manager | https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html |
| SSM Parameter Store | https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html |
| KMS | https://docs.aws.amazon.com/kms/latest/developerguide/overview.html |
| SST (Ion) | https://sst.dev/docs |

## Microsoft

| Topic | URL |
| ----- | --- |
| Microsoft Graph | https://learn.microsoft.com/en-us/graph/overview |
| Entra app registration | https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app |
| Graph webhooks | https://learn.microsoft.com/en-us/graph/webhooks |
| Outlook mail | https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview |
| Teams bots | https://learn.microsoft.com/en-us/microsoftteams/platform/bots/what-are-bots |
| Copilot extensibility | https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/ |

## Meta

| Topic | URL |
| ----- | --- |
| WhatsApp Cloud API | https://developers.facebook.com/docs/whatsapp/cloud-api |
| Webhooks | https://developers.facebook.com/docs/graph-api/webhooks/getting-started |
| Message templates | https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates |

## Twilio

| Topic | URL |
| ----- | --- |
| Messaging API | https://www.twilio.com/docs/messaging/api |
| WhatsApp (Twilio) | https://www.twilio.com/docs/whatsapp/api |
| Webhooks | https://www.twilio.com/docs/usage/webhooks |

## Slack

| Topic | URL |
| ----- | --- |
| Bolt / Events API | https://api.slack.com/events-api |
| OAuth scopes | https://api.slack.com/scopes |

## OpenAI / Anthropic

| Topic | URL |
| ----- | --- |
| OpenAI API | https://platform.openai.com/docs/api-reference |
| Assistants / GPTs | https://platform.openai.com/docs/assistants/overview |
| Anthropic API | https://docs.anthropic.com/en/api/getting-started |
| Claude on Bedrock | https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html |

## internal (not external — use codebase sub-agent)

| Topic | Path |
| ----- | ---- |
| Async push extensibility | `docs/analysis/async-channel-push-extensibility-review.md` |
| Channel routing plan | `docs/analysis/async-channel-push-routing-plan.md` |
| Async delivery architecture | `docs/analysis/channel-async-delivery-architecture.md` |
| Reference channel | `apps/channels/outlook/AGENTS.md` |
| Allowed channels | `apps/conversation-service/src/utils/security/input-validation.ts` |
| Shared outbound | `apps/channels/shared/utils/outbound` |
| SST scan (read-only) | `.claude/skills/aws-diagnose-read/scripts/scan_sst.py` |
