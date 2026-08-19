# Orchestrator checklist (parent agent only)

The **orchestrator** runs phases 0 and 2. Sub-agents run phase 1. Only the
orchestrator writes reports and chats the 2–3 line summary.

Cross-links: `dispatching-parallel-agents` (when to fan out),
`systematic-debugging` (hypotheses first).

## Phase 0 — scope (sequential, parent only)

1. Recommend read-only IAM (`references/iam-readonly-policy.json` or `ReadOnlyAccess`).
2. Confirm creds in env; never echo secrets.
3. Run identity check once:

```bash
python "$SKILL_ROOT/scripts/aws_read.py" sts get_caller_identity
```

4. **Intake gate (mandatory)** — classify path and collect required fields per
   `references/intake-required.md`. If anything required is missing, **ask the user
   in one message and stop** — do not run SST scan, log filters, or API calls yet.

```text
INTAKE_PATH: generic-aws | conversation | multi-conversation
INTAKE_OK: yes | no
MISSING: <list or empty>
```

Minimum fields: `STAGE`, `CONVERSATION_ID`, `TENANT_ID`, `AWS_REGION`,
time window, `DIAG_TOKEN` in env (if API/trace). Never guess stage.

Optional overrides:

```text
DISPATCH_PREFERENCE: auto | inline | parallel   # default auto
TOKEN_SENSITIVE: yes | no                        # default yes
```

5. Compute `EPOCH_START_MS` / `EPOCH_END_MS` per conversation:

```bash
bash "$SKILL_ROOT/scripts/diag_epoch.sh" --hours-ago 2 --hours-window 1
```

6. Form 2–3 hypotheses from `references/playbooks.md` (parent only).
7. **Resolve infra from SST** (phase 0.5) — before guessing log groups, SSM paths,
   or API routes:

```bash
python "$SKILL_ROOT/scripts/scan_sst.py" \
  --stage "$STAGE" --search "<lambda or queue name>" --json
```

email/web minimum: `conversation-service`, `channels/outlook`, `workflow`
(see `references/sst-infra-scan.md`). Pass `log_group_hint`, `handler`, and
`resolved_path` into L2 sub-agent prompts.

8. **Phase 0.9 — dispatch decision (mandatory).** Run this before phase 1.
   See also `dispatch-decision.md`.

### Step A — list domains and commands

From hypotheses, list **evidence domains** (not AWS services in the abstract).
One domain = one independent read batch (one log filter, one queue attrs, one API GET).

Draft the exact `COMMAND_LIST` you would run (numbered). Count **commands**, not
playbook bullets.

Merge domains when they share the same target (same log group, same queue, same API
resource) — counts as one domain.

### Step B — score

| Rule | Points |
| ---- | ------ |
| +1 per domain (after merges) | |
| +2 if 2+ `CONVERSATION_ID`s | forces **L1** (may inline or lite inside) |
| −1 if domains share one log group / queue / API resource (merged) | |
| −1 if `TOKEN_SENSITIVE=yes` (default) and score would be 3 | prefer inline |

User overrides:

- `DISPATCH_PREFERENCE=inline` → inline unless 2+ conversations require L1
- `DISPATCH_PREFERENCE=parallel` → L2 lite when score ≥ 2 and commands are independent
- `TOKEN_SENSITIVE=yes` → tie-break toward inline

### Step C — decide

| Condition | Mode |
| --------- | ---- |
| 2+ conversations | **L1** parallel — `subagent-conversation-investigator.md`; inside each L1 use inline if ≤2 commands else lite |
| 1 conversation, ≤2 commands after draft | **INLINE** — parent runs WRAP |
| 1 conversation, score ≥ 3, independent commands | **L2 LITE** parallel — `subagent-evidence-lite.md` + `COMMAND_LIST` only |
| Reads are sequential (B needs output of A) | **INLINE** — never parallelize dependent reads |
| Shared AWS outage suspect | **INLINE** wave 0: sts + one of cloudwatch / cloudtrail / health |

**Command-count tie-breaker:** if drafted `COMMAND_LIST` has ≤2 lines → **INLINE**
even when the playbook suggests more "nice to have" reads.

**Two-wave pattern:** discovery (`describe_log_groups`, `list_queues`) inline first;
re-score after names are known — only parallelize wave 2 if still ≥3 independent domains.

### Step D — record (parent only, do not put in report)

Emit before phase 1:

```text
DISPATCH: inline | l2-lite | l1-parallel
REASON: <one line>
DOMAINS: <comma-separated>
COMMANDS: <count>
```

**Never** paste `services.md`, full `aws-ops-compact.md`, or legacy `subagent-aws-*`
into Task prompts. Parent reads only matching rows in `references/aws-ops-compact.md`.

## Single-conversation intake 

See `references/intake-required.md` for required vs optional. Template:

```text
STAGE:                          e.g. dev-lshiva  (REQUIRED)
AWS_REGION:                     e.g. us-west-2    (REQUIRED)
API_BASE_URL:                   https://{stage}.api.example.com

TENANT_ID:                      (REQUIRED)
USER_ID:                        (ask if missing)
CONVERSATION_ID:                (REQUIRED)

WEB_MESSAGE_ID:                 (ask if web/email issue)
EMAIL_MESSAGE_ID:               (ask if web/email issue)

APPROX_TIME_UTC:                (REQUIRED)
DID_USER_TYPE_ON_WEB_FIRST:     yes / no / not sure
WORKFLOW_RUN_ID / SFN_EXECUTION_ARN:   optional
DISPATCH_PREFERENCE:            auto | inline | parallel
TOKEN_SENSITIVE:                  yes | no

# User sets in shell (REQUIRED for API reads):
# export DIAG_TOKEN='...'
```

## Multi-conversation intake

```text
STAGE:                          e.g. dev-lshiva
AWS_REGION:                     e.g. us-west-2
COMPARATIVE_REPORT:             yes | no   # default no → one file per conv
DISPATCH_PREFERENCE:            auto | inline | parallel   # default auto
TOKEN_SENSITIVE:                  yes | no   # default yes

CONVERSATIONS:
  - label: A
    conversation_id:
    tenant_id:
    web_message_id:
    email_message_id:
    approx_time_utc:
    workflow_run_id:             optional
  - label: B
    conversation_id:
    ...
```

Refuse vague "two users had issues" without ids. Max **4** parallel L1 agents.
Per-row **conversation_id**, **tenant_id**, and **approx_time_utc** are required.

### Anti-patterns (intake)

- Starting investigation without `INTAKE_OK=yes`
- Guessing stage or region
- Missing `DIAG_TOKEN` while calling conversation-service API

## Phase 1 — parallel evidence (sub-agents)

### L1 — per conversation (2+ conversations)

Single parent message, multiple `Task` calls:

```text
Task(readonly=true, subagent_type=generalPurpose): investigator A — full prompt from subagent-conversation-investigator.md
Task(readonly=true, subagent_type=generalPurpose): investigator B — ...
```

### L2 — per evidence domain (3+ domains only)

Parent builds `COMMAND_LIST` from `references/aws-ops-compact.md` (relevant rows
only). Dispatch **lite** prompts in one message — max 6–8 tasks:

| Domain type | Parent reads (once) | Sub-agent gets |
| ----------- | ------------------- | -------------- |
| `logs-*`, `api-*`, `s3-traces` | domain specialist file | `subagent-evidence-lite.md` + commands only |
| AWS `aws-*` | `aws-ops-compact.md` row | `subagent-evidence-lite.md` + commands only |
| `sfn-history` | `conversation-debug.md` | lite + SFN command lines |

Legacy full shell (avoid — higher tokens): `subagent-evidence-prompt.md`.

### Sub-agent rules

- `readonly: true` always.
- Self-contained prompt — no chat history.
- JSON return only; no reports; no fix suggestions.
- Wrapper path: `$SKILL_ROOT/scripts/aws_read.py`

### Anti-patterns

- Dispatching sub-agents for 1–2 simple reads (use inline).
- Attaching specialist markdown files to Task prompts.
- Pasting full `services.md` or `aws-ops-compact.md` into sub-agents.
- One agent walking conv A then conv B sequentially when independent.
- "Investigate everything" in one sub-agent.
- Sub-agents writing `.aws-details/reports/`.
- >8 concurrent gatherers (CloudWatch rate limits).

## Phase 2 — diagnose & report (parent only)

1. Parse all JSON blobs from L1/L2.
2. Build unified timeline per conversation (`merge-template.md`).
3. Correlate: observed vs inferred; rank hypotheses with confidence.
4. Write report(s) to `.aws-details/reports/`:
   - Default: `YYYY-MM-DD-HHmm-<slug>-conv-<label>.md`
   - Comparative: `...-compare-a-b.md` when `COMPARATIVE_REPORT=yes`
5. Chat: 2–3 lines + report path(s) only.

## Model hints

| Role | Model |
| ---- | ----- |
| L2 log/API shell | fast |
| L1 conversation investigator | standard |
| Parent merge + diagnosis | capable |
