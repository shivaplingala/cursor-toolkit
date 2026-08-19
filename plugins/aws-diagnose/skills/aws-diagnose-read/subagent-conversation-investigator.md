# Conversation investigator (L1 sub-agent)

One **L1 sub-agent per conversation**. Dispatch multiple L1 agents in **one
message** when the user supplies 2+ conversations (A, B, …). Each owns a single
`CONVERSATION_ID` and may fan out L2 evidence gatherers internally or return
structured evidence for the parent to merge.

---

## When to dispatch

- User gives **2+ conversation IDs** → mandatory parallel L1 (max **4** at once).
- User gives **1 conversation** with 3+ evidence domains → orchestrator may skip
  L1 and dispatch L2 gatherers directly (see `orchestrator.md`).

## L1 prompt template

```markdown
READ-ONLY CONVERSATION INVESTIGATOR (conversation {{LABEL}})

You own **ONE** conversation only: {{CONVERSATION_ID}}.
Do NOT read logs or APIs for any other conversation.

## Constraints

- AWS: `python "$SKILL_ROOT/scripts/aws_read.py"` only
- HTTP: GET only; Bearer `$DIAG_TOKEN` from env; never log the token
- Do NOT write `.aws-details/reports/`
- Do NOT suggest fixes to the user
- Local timeline synthesis OK; final root-cause ranking is the orchestrator's job

## Context for {{LABEL}}

STAGE={{STAGE}}
AWS_REGION={{AWS_REGION}}
API_BASE_URL=https://{{STAGE}}.api.example.com
TENANT_ID={{TENANT_ID}}
USER_ID={{USER_ID}}
CONVERSATION_ID={{CONVERSATION_ID}}
WEB_MESSAGE_ID={{WEB_MESSAGE_ID}}
EMAIL_MESSAGE_ID={{EMAIL_MESSAGE_ID}}
APPROX_TIME_UTC={{APPROX_TIME_UTC}}
EPOCH_START_MS={{EPOCH_START_MS}}
EPOCH_END_MS={{EPOCH_END_MS}}
WORKFLOW_RUN_ID={{WORKFLOW_RUN_ID or empty}}
SFN_EXECUTION_ARN={{SFN_EXECUTION_ARN or empty}}

## Evidence tasks

Run **only** `COMMANDS` below (orchestrator pre-fills). Do **not** open domain
specialist files or `services.md`.

{{COMMAND_LIST — orchestrator fills per domain from aws-ops-compact / domain specialists}}

Prefer parallel shell when commands are independent.

## Return format (JSON only)

{
  "conversation_label": "{{LABEL}}",
  "conversation_id": "{{CONVERSATION_ID}}",
  "status": "ok|partial|blocked",
  "message_id_comparison": {
    "web": "{{WEB_MESSAGE_ID}}",
    "email": "{{EMAIL_MESSAGE_ID}}",
    "same_generation": true|false|null
  },
  "timeline": [
    {
      "utc": "ISO-8601",
      "component": "websocket|run-agent|outbound|graph|api",
      "event": "short label",
      "snippet_redacted": "max ~300 chars"
    }
  ],
  "metrics": {
    "llm_ms": null,
    "turn_start_to_finalize_ms": null,
    "publish_to_graph_ms": null,
    "cold_start_ms": null
  },
  "local_findings": ["factual observations only, no fix recommendations"],
  "commands_run": ["..."],
  "gaps": ["..."]
}
```

## Orchestrator after L1 returns

1. Normalize timestamps to UTC (+ user TZ in report if known).
2. Write **one report per conversation** by default:
   `YYYY-MM-DD-HHmm-<slug>-conv-<label>.md`
3. If user asked to compare A vs B: add `merge-template.md` comparison section
   or a separate `...-compare-a-b.md`.

## subagent_type

- `generalPurpose` or `shell`, `readonly: true`
- Fast model OK if log/API commands are pre-filled by orchestrator
