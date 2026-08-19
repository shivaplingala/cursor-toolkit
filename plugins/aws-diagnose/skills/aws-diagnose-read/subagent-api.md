# — conversation-service HTTP GET evidence (L2)

**GET only.** Requires `export DIAG_TOKEN='...'` in the shell (never paste into
reports or git).

## Endpoints

Base: `https://${STAGE}.api.example.com`

| Purpose | Path |
| ------- | ---- |
| List messages | `GET /conversations/{id}/messages` |
| Get conversation | `GET /conversations/{id}` |
| Message trace | `GET /messages/{id}/trace` |
| Agent steps | `GET /messages/{id}/agent-steps` |

Routes: `apps/conversation-service/sst/stacks/api-stack-routes.ts`

## Commands

```bash
API="https://${STAGE}.api.example.com"

curl -sS -H "Authorization: Bearer $DIAG_TOKEN" \
  "$API/conversations/$CONVERSATION_ID/messages" \
  | jq '[.messages[]? | {id, channel, role, created, preview: (.content[:200] // "")}]'

# Per known message ids:
for MID in "$WEB_MESSAGE_ID" "$EMAIL_MESSAGE_ID"; do
  [ -z "$MID" ] || curl -sS -H "Authorization: Bearer $DIAG_TOKEN" \
    "$API/messages/$MID/trace" \
    | jq '{id: "'"$MID"'", metadata: .metadata | {channel, userMessage, aiResponse}, trace_ref: .trace}'
done
```

## 403 on trace

Employee tokens may list messages but not trace. Record in `gaps` and hand off to
`subagent-s3.md` using `trace: { bucket, key, region }` from message list.

## Return fields for orchestrator

- Message ids per channel (web vs email)
- Whether web/email assistant ids match
- `metadata.channel` from traces
- Short content previews only
