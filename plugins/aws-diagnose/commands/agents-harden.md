---
name: agents-harden
description: >-
  Production-harden an AgentCore agent (IAM, inbound auth, secrets, cold
  start, session lifecycle, maxVms, quotas). Bundled with aws-diagnose.
---

# /agents-harden

Follow **agents-harden** in this plugin (`skills/agents-harden/SKILL.md`).

If the live symptom is a quota/`maxVms`/timeout incident, `/agents-debug` or
`/aws-diagnose` can gather evidence first; then harden for the lasting fix.
