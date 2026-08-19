---
name: agents-debug
description: >-
  Diagnose a broken Bedrock AgentCore agent or environment (wrong answers,
  tool failures, timeouts, missing traces/logs, CLI doctor). Bundled with
  aws-diagnose; pairs with /aws-diagnose for general AWS reads.
---

# /agents-debug

Follow **agents-debug** in this plugin (`skills/agents-debug/SKILL.md`).

If the issue is general AWS/SST (Lambda, API Gateway, conversation-service)
rather than AgentCore, use `/aws-diagnose` instead (read-only WRAP).

When invoked after `/aws-diagnose`, keep AWS mutations off until the user
explicitly asks to apply a fix; prefer `agentcore traces|logs|status` and WRAP.
