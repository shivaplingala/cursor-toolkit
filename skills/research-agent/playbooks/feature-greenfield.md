# Playbook: feature-greenfield

Research type: `feature-greenfield`

New capability inside an existing app or package — not a new channel surface.

## Checklist

- [ ] Bounded context — rc/app owns the feature (`conversation-service`, `workflow`, etc.)
- [ ] Existing similar feature in repo (graphify + grep)
- [ ] API contract: new routes vs extend existing; authorizer pattern
- [ ] Data stores: Mongo collections, DynamoDB tables, S3 prefixes
- [ ] Events: EventBridge, SQS, SFN if async
- [ ] Identity / authz: Cedar policies, role matrix in `docs/authz/`
- [ ] Prompt or LLM touchpoints if AI-facing
- [ ] UI packages affected (`conversation-ui`, admin UIs)
- [ ] i18n / case-i18n if user-visible strings
- [ ] SST stack ownership and deploy-time config
- [ ] GitNexus impact on shared symbols before recommending edits
- [ ] Full configuration inventory (AWS + app env as applicable)
- [ ] Testing: unit scope, integration, personal stage smoke

## Report emphasis

- **Recommended approach:** minimal extension vs new module (Ponytail alignment)
- **Alternatives:** build in existing service vs new micro-app
- **Implementation outline:** phases without code

## Sub-agent focus

| Sub-agent | Extra focus |
| --------- | ----------- |
| external-docs | Provider SDK only if external API involved |
| github-samples | Similar patterns in monorepo first, then official samples |
| aws-config-catalog | IAM + SST for new resources only |
| codebase | Primary — paths, reuse, blast radius |
