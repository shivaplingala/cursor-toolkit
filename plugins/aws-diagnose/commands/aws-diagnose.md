---
name: aws-diagnose
description: >-
  Start a read-only AWS/SST diagnosis for the current workspace. Runs the
  aws-readonly-diagnostics skill: intake → SST scan → evidence → report under
  .aws-details/reports/.
---

# /aws-diagnose

Follow the **aws-readonly-diagnostics** skill in this plugin (`skills/aws-diagnose-read/SKILL.md`).

## Steps

1. **Intake first** — ask once for missing required fields; do not call AWS until intake is complete (`references/intake-required.md`).
2. **Resolve `$SKILL_ROOT`** to this skill’s directory (plugin copy under `~/.cursor/plugins/local/aws-diagnose/skills/aws-diagnose-read`, or the workspace `.claude/skills/aws-diagnose-read` if that is what is loaded). Use only:
   - `python "$SKILL_ROOT/scripts/aws_read.py" …`
   - `python "$SKILL_ROOT/scripts/scan_sst.py" …`
3. **Dispatch** — phase 0.9 (`dispatch-decision.md`); prefer inline when cheap.
4. **Report** — write markdown with `report-template.md` to `.aws-details/reports/YYYY-MM-DD-HHmm-<slug>.md`.
5. **Chat reply** — 2–3 line summary + report path(s). No secrets, tokens, or raw PII.

If the user asks to mutate AWS (create/update/delete/invoke): refuse and hand them the suggested change from the report.

## AgentCore

If the issue is Bedrock AgentCore (runtime, gateway, memory, traces, `agentcore`
CLI), classify via `skills/aws-diagnose-read/references/agentcore-handoff.md`, then
load the matching command/skill:

- `/agents-debug` — broken agent, traces, logs, CLI doctor
- `/agents-build` — add memory/VPC/multi-agent/browser/etc. (after diagnose)
- `/agents-optimize` — evals, monitoring, observability, cost
- `/agents-harden` — IAM, auth, cold start, sessions, quotas

Diagnose stays read-only; mutating `agentcore` steps belong in those skills after handoff.
