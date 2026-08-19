# — CloudWatch log evidence (L2)

**First:** resolve Lambda logical names via `scan_sst.py` (see `references/sst-infra-scan.md`):

```bash
python "$SKILL_ROOT/scripts/scan_sst.py" \
  --app conversation-service --topic lambda --stage "$STAGE" --json
python "$SKILL_ROOT/scripts/scan_sst.py" \
  --app channels/outlook --topic lambda --stage "$STAGE" --json
python "$SKILL_ROOT/scripts/scan_sst.py" \
  --app workflow --search RunAgent --stage "$STAGE" --json
```

Use each function's `log_group_hint` with `describe_log_groups` prefix filter before
blind `filter_log_events`.

Run from skill directory or use full path to `scripts/aws_read.py`.

## Discover log groups (wave 1, once per stage/region)

```bash
SKILL_ROOT="${SKILL_ROOT:-.claude/skills/aws-diagnose-read}"
python "$SKILL_ROOT/scripts/aws_read.py" logs describe_log_groups \
  --param logGroupNamePrefix="/aws/lambda/" \
  --paginate --max-items 100 \
  --region "$AWS_REGION"
```

Filter results for stage substring (e.g. `dev-lshiva`). Prefer `log_group_hint`
from `scan_sst.py` over this table:

| Component | Logical name (scan) | Fallback name pattern |
| --------- | ------------------- | ----------------------- |
| WebSocket handler | `MessagesWebSocketHandler` | `conversatio-*-{stage}-MessagesWebSocketHandler*` |
| Outbound email | `outlookOutboundReplyProcessor` | `outloo-*-{stage}-outlookOutboundReplyProcessor*` |
| run-agent | `WorkflowRunAgent` | `*run-agent*` or workflow stack + stage |
| Email ingest | email-processor handler in `functions.ts` | `outloo-*-{stage}-*email*processor*` |

## Wave 2 — filter per domain

Replace `LOG_GROUP`, epochs, and filter id.

```bash
SKILL_ROOT="${SKILL_ROOT:-.claude/skills/aws-diagnose-read}"
python "$SKILL_ROOT/scripts/aws_read.py" logs filter_log_events \
  --param logGroupName="$LOG_GROUP" \
  --param startTime="$EPOCH_START_MS" \
  --param endTime="$EPOCH_END_MS" \
  --param filterPattern="$CONVERSATION_ID" \
  --region "$AWS_REGION"
```

### WebSocket / orchestrator (`logs-websocket`)

Filter on `conversationId` or `Processing WebSocket message`.
Capture: turn start, Bedrock/agent completion, finalize, `channelOutboundReply`.

### Outbound reply (`logs-outbound`)

Filter on `conversationId`, `assistantMessageId`, or `channelOutboundReply`.
Capture: `INIT_START`, `Init Duration`, Graph send, `deliveryDurationMs`,
`Async workflow reply emailed`.

### run-agent (`logs-run-agent`)

Filter on `conversationId`, execution name, or `assistantMessageId`.
Capture: SFN/Lambda start, channel in input, completion.

### Email ingest (`logs-email-ingest`)

Use when lag is **before** AI (webhook → SQS → processor). Filter on
`internetMessageId`, `messageId`, subscription id.

## Epoch helper

```bash
bash "$SKILL_ROOT/scripts/diag_epoch.sh" \
  --hours-ago 2 --hours-window 1
# or --iso-start "2026-07-02T09:55:00Z" --iso-end "2026-07-02T10:15:00Z"
```

## Redaction

- No full email HTML bodies in findings.
- Truncate log lines to ~500 chars in `raw_snippet_redacted`.
