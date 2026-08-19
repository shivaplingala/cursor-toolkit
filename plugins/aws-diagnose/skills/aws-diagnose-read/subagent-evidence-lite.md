# L2 evidence gatherer — lite (token-minimal)

**Default for all L2 dispatches.** Parent fills placeholders; sub-agent must **not**
read `services.md`, `playbooks.md`, `subagent-aws-*`, or domain specialist files.

---

```text
READ-ONLY GATHERER — domain {{DOMAIN}}

Rules: Run ONLY commands below via WRAP. No boto3/aws CLI writes. No diagnose/fix/report.
Do not read any other files. GET-only HTTP if listed. Redact secrets.

WRAP=python "$SKILL_ROOT/scripts/aws_read.py"
REGION={{AWS_REGION}}  START_MS={{EPOCH_START_MS}}  END_MS={{EPOCH_END_MS}}

COMMANDS:
{{COMMAND_LIST — parent pre-fills exact shell lines}}

RETURN JSON ONLY (max 5 findings, 200 chars/snippet):
{"domain":"{{DOMAIN}}","status":"ok|partial|blocked","commands_run":[],"findings":[{"t":"utc|null","s":"source","summary":"one line","snippet":"≤200c"}],"gaps":[],"confidence":"high|medium|low"}
```

## Parent checklist (before Task)

1. Pick domain row from `references/aws-ops-compact.md` (that row only — not whole file in prompt).
2. Write exact `COMMAND_LIST` (numbered). Sub-agent executes mechanically.
3. domains: parent reads domain specialist **once**, extracts commands here — sub-agent does not.

## subagent_type

`shell` + `readonly: true` + fast model for AWS reads. `generalPurpose` only for IAM/SFN JSON parse.
