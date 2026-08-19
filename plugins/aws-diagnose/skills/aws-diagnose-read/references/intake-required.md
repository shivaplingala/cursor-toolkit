# Required intake — ask before investigating

**Gate rule:** If any **required** field for the investigation path is missing,
**stop and ask the user in one message**. Do not run `scan_sst.py`, log filters,
API GETs, or dispatch sub-agents until the gate passes.

Exception: after AWS env creds are confirmed, `sts get_caller_identity` is OK to
verify the session.

## 1. Classify the investigation

| Path | When |
| ---- | ---- |
| **generic-aws** | Lambda/S3/RDS/ECS/API GW/etc. — no conversation |
| **conversation** | conversation-service, web vs email, message/trace/debug |
| **multi-conversation** | 2+ conversation IDs to compare |

## 2. Required by path

### All paths

| Field | Required | Notes |
| ----- | -------- | ----- |
| Symptom | **yes** | What failed, error text, wrong behavior |
| Time window | **yes** | `APPROX_TIME_UTC` or "last N hours" — needed for logs/metrics |
| AWS credentials | **yes** | `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (+ `AWS_SESSION_TOKEN` if temp) or `AWS_PROFILE` in env |
| `AWS_REGION` | **yes** | e.g. `us-west-2` — ask if not in env and not inferable |

### generic-aws (additional)

| Field | Required | Notes |
| ----- | -------- | ----- |
| Resource id | **yes** | Lambda name/ARN, bucket, queue name, DB id, cluster, API id — **ask per symptom** |
| `STAGE` | if -named resources | e.g. `dev-lshiva` in Lambda/log group names — ask when logs mention stage suffix |

### conversation (additional)

| Field | Required | Notes |
| ----- | -------- | ----- |
| `STAGE` | **yes** | Deployed SST stage: `dev`, `dev-lshiva`, `staging`, etc. — **never guess** |
| `CONVERSATION_ID` | **yes** | |
| `TENANT_ID` | **yes** | Needed for logs, API, S3 trace prefix |
| `DIAG_TOKEN` | **yes** if API/S3 trace | `export DIAG_TOKEN='...'` in shell — API Bearer; ask user to set, never echo |
| `USER_ID` | **ask if missing** | Often needed for context; ask in same batch |
| `WEB_MESSAGE_ID` / `EMAIL_MESSAGE_ID` | **ask if channel issue** | At least one when debugging web vs email or a specific message |
| `API_BASE_URL` | optional | Default `https://{STAGE}.api.example.com` |

### multi-conversation (per conversation row)

| Field | Required |
| ----- | -------- |
| `label` (A, B, …) | **yes** |
| `conversation_id` | **yes** |
| `tenant_id` | **yes** |
| `approx_time_utc` | **yes** per row |
| `web_message_id` / `email_message_id` | ask if comparing channels |

Plus shared: `STAGE`, `AWS_REGION`, `DIAG_TOKEN` (if API).

## 3. Optional (do not block)

`DISPATCH_PREFERENCE`, `TOKEN_SENSITIVE`, `COMPARATIVE_REPORT`, `WORKFLOW_RUN_ID`,
`SFN_EXECUTION_ARN`, `DID_USER_TYPE_ON_WEB_FIRST`

## 4. How to ask (one message, no investigation yet)

List **only missing** fields. Include format examples. Do not ask for fields
already provided.

```markdown
I can investigate once I have a few details:

1. **Stage** — which deployed environment? (e.g. `dev-lshiva`, `dev`, `staging`)
2. **Conversation ID** — the `conversationId` for this thread
3. **Tenant ID** — tenant UUID
4. **AWS region** — e.g. `us-west-2` (if not already in your session)
5. **Approx time (UTC)** — when the issue occurred (or "last 2 hours")
6. **DIAG_TOKEN** — please `export DIAG_TOKEN='…'` in the terminal for API reads (I won't echo it)

Optional but helpful: **user ID**, **web message ID**, **email message ID**.
```

For **generic-aws**, swap in resource-specific asks (function name, bucket, queue, etc.).

## 5. Anti-patterns

- Guessing `STAGE` as `dev` when user said "dev environment"
- Running `scan_sst.py` without `STAGE`
- Calling conversation-service without `DIAG_TOKEN`
- Filtering logs with only tenant id and no time window
- Proceeding with "two users had issues" without conversation ids
- Echoing or committing `DIAG_TOKEN`, AWS secrets, or message bodies

## 6. Gate checklist (orchestrator)

Before step 5 (epochs) and step 7 (SST scan):

```text
INTAKE_PATH: generic-aws | conversation | multi-conversation
INTAKE_OK: yes | no
MISSING: <list or empty>
```

If `INTAKE_OK=no` → ask user (section 4), then stop.
