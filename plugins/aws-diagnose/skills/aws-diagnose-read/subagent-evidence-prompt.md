# Evidence gatherer sub-agent prompt (legacy — high tokens)

> **Use `subagent-evidence-lite.md` instead.** This file duplicates constraints and
> invites loading specialist docs. Keep only for edge cases needing the full schema.

Copy this block into L2 `Task()` only when lite is insufficient. Replace `{{...}}`
placeholders.

---

```markdown
READ-ONLY EVIDENCE GATHERER

## Constraints (mandatory)

- All AWS calls via:
  `python "$SKILL_ROOT/scripts/aws_read.py" <service> <op> ...`
- Do **NOT** diagnose, write reports, or suggest fixes.
- Return **only** the JSON below. Max 5 findings, 200 chars/snippet.

## Context

STAGE={{STAGE}} AWS_REGION={{AWS_REGION}} DOMAIN={{DOMAIN_NAME}}
EPOCH_START_MS={{EPOCH_START_MS}} EPOCH_END_MS={{EPOCH_END_MS}}

## Commands to run (ONLY these — do not read other skill files)

{{COMMAND_LIST}}

## Return JSON only

{"domain":"{{DOMAIN_NAME}}","status":"ok|partial|blocked","commands_run":[],"findings":[{"t":"utc","s":"source","summary":"line","snippet":"≤200c"}],"gaps":[],"confidence":"high|medium|low"}
```
