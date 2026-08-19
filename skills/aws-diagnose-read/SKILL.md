---
name: aws-readonly-diagnostics
description: >-
  Debug and diagnose AWS issues using READ-ONLY access. Use this skill whenever
  the user wants to investigate, debug, troubleshoot, or root-cause a problem in
  AWS — e.g. "my Lambda is throwing errors", "diagnose why this S3 access is
  failing", "check CloudWatch logs for my service", "why is my app 500ing",
  "look into this AWS bug", "what's wrong with my ECS task / RDS / API Gateway".
  Trigger it whenever the user supplies AWS credentials or asks you to inspect
  CloudWatch logs, S3 data, metrics, CloudTrail, or any AWS resource state to
  find a problem. This skill ONLY reads (describe/get/list/lookup) — it never
  creates, updates, deletes, or invokes anything. It gathers evidence, reports
  findings, and SUGGESTS a fix for the human to apply themselves.
---

# AWS Read-Only Diagnostics

Investigate AWS problems by gathering evidence with read-only API calls, then
report a root-cause diagnosis and a suggested fix. The defining constraint:
**this skill never changes anything in the account.** It only observes. The fix
is described for the human to apply; it is never applied here.

## The read-only guarantee (read this first)

Three layers keep this safe. Do not weaken any of them.

1. **Use the wrapper, not raw boto3/CLI.** Every AWS call goes through
   `scripts/aws_read.py`, which refuses any operation that isn't a verified read
   (it blocks `put/create/delete/update/modify/invoke/run/...` and fails closed
   on unknown verbs). Never bypass it by calling `boto3`, `aws` CLI, or HTTP
   endpoints directly to perform an action the wrapper would refuse.
2. **Recommend least-privilege credentials.** Before starting, tell the user the
   safest setup is credentials scoped to read-only (e.g. the AWS-managed
   `ReadOnlyAccess` policy, or the tighter custom policy in
   `references/iam-readonly-policy.json`). This way AWS itself rejects any write,
   independent of this skill. If the user can only provide broader credentials,
   proceed — but the wrapper is then the sole guardrail, so be especially strict.
3. **Suggest, never apply.** Findings end in a *recommended* fix. Do not offer to
   run the fix, generate console-free "just paste this" mutation commands, or
   write a script that performs the change. You may show the user the read-only
   commands you ran so they can reproduce your investigation.

If the user explicitly asks you to make a change ("just delete the bad object",
"go ahead and update the policy"), decline that part warmly: explain this skill
is read-only by design, then hand them the exact change to make themselves.

## AgentCore path

If the symptom is Bedrock **AgentCore** (runtime, gateway, memory, traces,
`agentcore` CLI, `agentcore/agentcore.json`), load
`references/agentcore-handoff.md` and route to sibling skills:

| Intent | Skill |
| ------ | ----- |
| Broken agent / traces / logs / CLI | `agents-debug` |
| Add capability | `agents-build` |
| Evals / observability / cost | `agents-optimize` |
| Production IAM / auth / sessions / quotas | `agents-harden` |

Mutating `agentcore add|deploy|…` is suggest-only until the handoff skill is active.

## Credentials

Read credentials from the standard AWS environment chain. Have the user provide
them as environment variables in the session — never hardcode, echo, or log
secret values, and never write them to a file:

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...        # only if temporary credentials
export AWS_DEFAULT_REGION=us-east-1 # or pass --region per call
```

First call should always confirm identity and scope:

```bash
python scripts/aws_read.py sts get_caller_identity
```

This tells you the account ID, the principal, and confirms the credentials work
before you start digging. If it returns `AccessDenied` on later read calls,
that's expected and safe — it means IAM is correctly limiting access; report
which permission is missing rather than trying to work around it.

## Workflow

### 1. Scope the problem
Before touching AWS, get the user to pin down: what's the symptom (error message,
status code, wrong output, latency, cost)? which resource or service? what time
window? what changed recently? If the request is vague ("AWS is broken"), ask one
or two sharp questions first — a diagnosis is only as good as the starting signal.

### 2. Form hypotheses
List the few most likely causes given the symptom. This drives which data you
pull — don't blindly dump every log. See `references/playbooks.md` for
symptom→cause→evidence maps for the common cases (Lambda errors, 5xx from
API Gateway/ALB, S3 access denied, ECS task crashes, RDS connectivity, IAM
permission failures, throttling, cost spikes).

### 3. Gather evidence (read-only)
Pull only what tests your hypotheses, using `scripts/aws_read.py`. The most
common reads:

```bash
# CloudWatch Logs — find errors in a log group over a time window
python scripts/aws_read.py logs filter_log_events \
  --param logGroupName=/aws/lambda/my-fn \
  --param startTime=1718900000000 --param endTime=1718910000000 \
  --param filterPattern=?ERROR ?Exception ?Timeout \
  --region us-east-1

# List log groups / streams when you don't know exact names
python scripts/aws_read.py logs describe_log_groups --param limit=50

# CloudWatch metrics — e.g. Lambda errors/throttles, ALB 5xx, RDS CPU
python scripts/aws_read.py cloudwatch get_metric_data --param ... 

# S3 — inspect bucket layout and object metadata (no downloads needed to start)
python scripts/aws_read.py s3 list_objects_v2 --param Bucket=my-bucket --param MaxKeys=100
python scripts/aws_read.py s3 head_object --param Bucket=my-bucket --param Key=path/to/obj
python scripts/aws_read.py s3 get_bucket_policy --param Bucket=my-bucket

# Read a small config/log object's contents (capped at 256KB by the wrapper)
python scripts/aws_read.py s3 get_object --param Bucket=my-bucket --param Key=config.json

# Resource state
python scripts/aws_read.py ec2 describe_instances --param ...
python scripts/aws_read.py lambda get_function_configuration --param FunctionName=my-fn
python scripts/aws_read.py rds describe_db_instances

# Who did what / recent changes — CloudTrail is invaluable for "what changed"
python scripts/aws_read.py cloudtrail lookup_events --param ...
```

For the full per-service catalog of useful read operations and their key
parameters, read `references/services.md`. Use `--list-ops` on any service to
see everything the wrapper will allow:

```bash
python scripts/aws_read.py <service> --list-ops
```

Tips:
- Use `--paginate --max-items N` for list/describe calls that page.
- CloudWatch Logs times are **epoch milliseconds**. Compute them rather than
  guessing; e.g. `python -c "import time;print(int(time.time()*1000)-3600000)"`
  for "one hour ago".
- Correlate across sources: a log error + the matching CloudTrail event + the
  resource config usually pins the root cause faster than logs alone.
- Don't over-pull. Filter logs by pattern and time window; sample rather than
  dumping millions of lines.

### 4. Diagnose
Correlate the evidence into a root cause. Distinguish what you *observed* from
what you *infer*. If the evidence is ambiguous, say so and state what additional
read would disambiguate — don't manufacture certainty.

### 4b. Trace to source code (when a repo is available)
AWS evidence names *what* failed; the report should also name *where in code* when
you can resolve it. Do this after correlating logs/SFN/API evidence, before writing
the report. Skip only for pure infra issues (IAM, quotas, misconfigured buckets)
with no application handler involved.

**Map AWS → file/function:**

| Signal | How to resolve |
| ------ | -------------- |
| Lambda log group `/aws/lambda/...` | `lambda get_function_configuration` → `Handler` + env; grep repo for SST function name or handler path |
| Distinctive log line / error text | Grep the string in the workspace |
| Stack trace in CloudWatch | Parse `at fnName (path/file.ts:line:col)` — cite file, function, line |
| API Gateway / HTTP path | Route table in SST (`routeKey:`) or OpenAPI → handler file |
| Step Functions state | `get_execution_history` → Lambda ARN → handler file |
| S3 key / env var naming | Grep bucket prefix or constant in repo |

Prefer `graphify query` / gitnexus `context` when the project has them; otherwise
grep and read handler headers. Read the function body only when logs pin a branch.

Record **confidence** per mapping: `confirmed` (stack trace or handler match),
`likely` (log string + call path), `possible` (inferred from naming only). If
unresolved, say what would close it (e.g. "need Lambda `Handler` field" or "no
stack trace in logs").

### 5. Report
Write the diagnosis to a **new markdown file**, then give the user a 2-3 line
chat summary plus the report path. Do not dump the full report into chat.

- Directory: `.aws-details/reports/` (create it with `mkdir -p` if missing).
- Filename: `YYYY-MM-DD-HHmm-<short-symptom-slug>.md` (current UTC time,
  lowercase hyphenated slug — e.g. `2026-06-30-1420-lambda-timeout.md`).
- Fill every section of the structure below; no placeholders left behind.

```
# AWS Diagnosis: <one-line symptom>

## Summary
2-3 sentences: what's wrong and the most likely root cause. If resolved, name the
primary source file and function (e.g. `message-send.ts` → `finalizeSyncMessage`).

## Code location
Where the issue originates in the codebase. **Include this section whenever app
logic is involved**; omit only for pure AWS/IAM/config issues with no handler.

| Role | File | Function / symbol | Confidence |
| ---- | ---- | ----------------- | ---------- |
| Primary | `apps/.../file.ts` | `functionName()` | confirmed / likely / possible |
| Related | `apps/.../other.ts` | `otherFn()` | likely |

- **Primary:** one line on why this file/function is the root site (tie to a log
  line, missing call, or branch taken).
- **Gap / wiring:** if behavior depends on a call that never happens, list both
  the caller that should invoke and the callee that exists elsewhere.

If a row cannot be resolved, keep the table row with `unresolved` and note the
missing signal in **Open questions**.

## Evidence
- What you checked and what it showed. Reference concrete data
  (log lines, metric values, config fields, CloudTrail events, timestamps).
- Note the read-only commands used, so the user can reproduce.

## Root cause
The specific cause, with confidence level (confirmed / likely / possible).
If multiple causes are plausible, rank them.

## Suggested fix
Concrete steps the USER should take to fix it. Be specific (which setting,
which value, which resource). **Reference files and functions from Code location**
(e.g. "in `websocket-workflow-helpers.ts`, call `handleDeferredWorkflowActions`
from the sync path in `message-send.ts`"). Because this skill is read-only,
present this as instructions/changes for them to apply — do not apply it yourself.

## How to verify the fix
What the user should observe (metric returns to normal, errors stop, etc.)
after applying the fix.

## Open questions / next reads (if any)
If the diagnosis is incomplete, the specific further reads that would close it.
```

## Hard boundaries
- No mutating calls, ever — not even "harmless" ones. The wrapper enforces this;
  don't try to route around it.
- No minting of credentials or presigned URLs (`sts:AssumeRole`,
  `GetSessionToken`, S3 presign, `kms:Decrypt`, etc. are blocked).
- Don't print secret values you come across (env vars, secrets in logs, keys in
  config objects). If a secret appears to be the problem (e.g. an expired key),
  say *that* it's the problem and where it lives, not its value.
- Treat the credentials as sensitive: don't log, echo, or persist them.

## Reference files
- `references/services.md` — read-only operation catalog per service, with the
  parameters that matter for diagnosis.
- `references/playbooks.md` — symptom→cause→evidence playbooks for common AWS
  failure modes.
- `references/iam-readonly-policy.json` — a scoped read-only IAM policy to hand
  the user so their credentials can't write even in principle.

---

## conversation-service debugging (appendix)

Use this section when diagnosing conversation-service, workflow `run-agent`,
async channel push (Outlook email), S3 observability traces, or web-vs-email reply
mismatches. AWS calls still go through `scripts/aws_read.py`. **Read-only HTTP
GET** to conversation-service with the user's bearer token is also allowed (see
below); do not POST/PUT/DELETE.

For a longer playbook see `references/conversation-debug.md` (create if
missing). Prefer `report-template.md` for full incident reports.

### User intake — ask before investigating

If the user has not provided enough context, send this block once (minimum:
`conversationId`, `stage`, approx UTC time, token + AWS read creds in shell):

```
STAGE:                          e.g. dev-lshiva
AWS_REGION:                     e.g. eu-west-1
API_BASE_URL:                   https://{stage}.api.example.com

TENANT_ID:
USER_ID:
CONVERSATION_ID:

WEB_MESSAGE_ID:                 (assistant msg on portal, if known)
EMAIL_MESSAGE_ID:               (or "unknown")

APPROX_TIME_UTC:                e.g. 2026-07-01 14:30–15:00
DID_USER_TYPE_ON_WEB_FIRST:     yes / no / not sure

WORKFLOW_RUN_ID / SFN_EXECUTION_ARN:   (optional)

# User runs in shell — never commit or paste into reports:
# export DIAG_TOKEN='...'
# export AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN
```

- Ask user to `export DIAG_TOKEN=...` or confirm "token/creds are in the shell".
- Never echo, log, or write tokens to reports or git.
- `GET /messages/{id}/trace` needs **Tenant admin** or **Conversation audit**.
  Employee tokens may list messages but get 403 on trace — fall back to S3 traces
  via AWS creds.

### Discovering APIs from the codebase

Do not guess URLs. Resolve from the repo:

1. **Routes:** `apps/conversation-service/sst/stacks/api-stack-routes.ts` — search
   `routeKey:` for method + path.
2. **Handler:** file named in the route (e.g. `message-list.ts`) — header comment
   documents the HTTP contract.
3. **Base URL:** `apps/conversation-service/.env.example` —
   `https://{stage}.api.example.com`.

| Purpose | Method | Path |
| ------- | ------ | ---- |
| List messages | GET | `/conversations/{id}/messages` |
| Get conversation | GET | `/conversations/{id}` |
| Message trace | GET | `/messages/{id}/trace` |
| Agent steps | GET | `/messages/{id}/agent-steps` |

Read-only examples (use `$DIAG_TOKEN`, redact in reports):

```bash
API="https://${STAGE}.api.example.com"
curl -sS -H "Authorization: Bearer $DIAG_TOKEN" \
  "$API/conversations/$CONVERSATION_ID/messages" \
  | jq '.messages[] | {id, channel, role, created, preview: .content[0:200]}'

curl -sS -H "Authorization: Bearer $DIAG_TOKEN" \
  "$API/messages/$MESSAGE_ID/trace" \
  | jq '.metadata | {channel, userMessage, aiResponse}'
```

### S3 observability traces

Gzip JSON at finalize. Key pattern:

`traces/{tenantId}/{sessionId}/{messageId}/{traceId}.json.gz`

Source: `apps/conversation-service/src/utils/tracing/trace-logger.ts`. Each message
may store `trace: { bucket, key, region }` in Mongo (visible via message list API).

```bash
python scripts/aws_read.py s3 list_objects_v2 \
  --param Bucket=<traces-bucket> \
  --param Prefix="traces/<tenantId>/<conversationId>/" \
  --param MaxKeys=50 \
  --region "$AWS_DEFAULT_REGION"

python scripts/aws_read.py s3 get_object \
  --param Bucket=<traces-bucket> \
  --param Key="traces/<tenantId>/<sessionId>/<messageId>/<traceId>.json.gz" \
  --region "$AWS_DEFAULT_REGION"
```

Decompress: `gunzip -c trace.json.gz | jq '.metadata | {channel, userMessage, aiResponse}'`

**Key trace fields:** `metadata.channel`, `metadata.aiResponse`, `metadata.userMessage`,
workflow/agentContext events in `events[]`.

### Correlating web vs email (workflow / async push)

1. **Different `messageId`** → different LLM runs (sync orchestrator vs `run-agent`
   vs user web turn). Not a formatting bug.
2. **Same `messageId`** → one generation; diff may be post-processing (email:
   `outbound-reply-processor`) or web showing post-finalize Mongo content.
3. Compare `metadata.channel` in traces; check SFN input `channel` on `run-agent`
   (Step Functions `get_execution_history` via wrapper).

Log groups (stage-adjusted names): `run-agent`, conversation-service websocket
handler, Outlook `outbound-reply-processor`. Filter on `conversationId`,
`assistantMessageId`, `channel`.

Async push routing uses `lastUserInteractionChannel` on the session, not SFN
`channel`. See `docs/analysis/async-channel-push-routing-plan.md`.

### Report additions for serverless projects issues

In `.aws-details/reports/` include when relevant:

- **Code location** table (required for app-logic bugs): map Lambda names from logs
  to handler files under `apps/conversation-service`, `apps/workflow`, `apps/channels/outlook`, etc.
- Table comparing web vs email **message ids** (match or not)
- `metadata.channel` per trace
- SFN `channel` if workflow involved
- Whether async push fired (outbound-reply / `channelOutboundReply` logs)
- Redact full email bodies and tokens; cite ids and short content previews only
