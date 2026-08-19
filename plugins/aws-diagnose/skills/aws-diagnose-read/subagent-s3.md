# — S3 observability trace evidence (L2)

Trace key pattern:

`traces/{tenantId}/{sessionId}/{messageId}/{traceId}.json.gz`

Source: `apps/conversation-service/src/utils/tracing/trace-logger.ts`

## Resolve traces bucket / SSM

```bash
python "$SKILL_ROOT/scripts/scan_sst.py" \
  --app conversation-service --topic ssm --search trace --stage "$STAGE" --json
```

Or from message list API (`trace.bucket`). See `references/sst-infra-scan.md` if path unknown.

## List + fetch

```bash
SKILL_ROOT="${SKILL_ROOT:-.claude/skills/aws-diagnose-read}"
BUCKET="<traces-bucket>"
PREFIX="traces/${TENANT_ID}/${CONVERSATION_ID}/"

python "$SKILL_ROOT/scripts/aws_read.py" s3 list_objects_v2 \
  --param Bucket="$BUCKET" \
  --param Prefix="$PREFIX" \
  --param MaxKeys=50 \
  --region "$AWS_REGION"

python "$SKILL_ROOT/scripts/aws_read.py" s3 get_object \
  --param Bucket="$BUCKET" \
  --param Key="<full-key-from-list-or-api>" \
  --region "$AWS_REGION"
```

Wrapper caps object size (~256KB). Decompress gzip output:

```bash
# If wrapper writes JSON with body base64, decode per wrapper output format;
# or save to file and: gunzip -c trace.json.gz | jq '.metadata | {channel, userMessage, aiResponse}'
```

## Key trace fields

- `metadata.channel`, `metadata.aiResponse`, `metadata.userMessage`
- Workflow/agent events in `events[]`

## Redaction

Do not return full `aiResponse` or email bodies — short previews only.
