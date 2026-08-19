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
  find a problem. If required intake is missing (stage, conversation id, tenant id,
  region, DIAG_TOKEN, etc.), ask the user before investigating — see intake-required.md.
  For conversation/email issues, or when the user gives
  2+ conversation IDs, use parallel sub-agents per orchestrator.md. This skill
  ONLY reads (describe/get/list/lookup) — it never creates, updates, deletes, or
  invokes anything. It gathers evidence, reports findings, and SUGGESTS a fix for
  the human to apply themselves.
---

# AWS Read-Only Diagnostics

## Path resolution (`$SKILL_ROOT`)

Resolve `SKILL_ROOT` to this skill directory before any script call:

- Plugin install: `~/.cursor/plugins/local/aws-diagnose/skills/aws-diagnose-read`
- Workspace copy (Claude Code): `.claude/skills/aws-diagnose-read`

```bash
SKILL_ROOT="${SKILL_ROOT:-$HOME/.cursor/plugins/local/aws-diagnose/skills/aws-diagnose-read}"
# Prefer workspace copy when present (keeps scripts next to monorepo SST sources):
[ -d .claude/skills/aws-diagnose-read ] && SKILL_ROOT=".claude/skills/aws-diagnose-read"
```

Then always: `python "$SKILL_ROOT/scripts/aws_read.py" …` and `python "$SKILL_ROOT/scripts/scan_sst.py" …`.


Investigate AWS problems by gathering evidence with read-only API calls, then
report a root-cause diagnosis and a suggested fix. The defining constraint:
**this skill never changes anything in the account.** It only observes.

## Role: orchestrator vs sub-agents

| Role | Who | Responsibilities |
| ---- | --- | ---------------- |
| **Orchestrator** | Parent agent (you when skill is active) | Intake, hypotheses, dispatch, merge, diagnose, write reports |
| **L1 sub-agent** | One per conversation (A, B, …) | All evidence for a single `CONVERSATION_ID`; returns JSON |
| **L2 sub-agent** | One per evidence domain | Logs, API, S3, SFN for one conversation; returns JSON |

**Follow `orchestrator.md` for the full phase 0 → 1 → 2 checklist.**

## Intake gate (mandatory — ask before AWS reads)

Classify path (`generic-aws` | `conversation` | `multi-conversation` | `agentcore`).
If required fields are missing, **ask the user once and stop** — see
`references/intake-required.md`.

minimum: **STAGE**, **CONVERSATION_ID**, **TENANT_ID**, **AWS_REGION**, time
window, **`DIAG_TOKEN` in env** (for API/trace). Do not guess stage (`dev-lshiva` ≠ `dev`).

### AgentCore path

If the symptom is Bedrock **AgentCore** (runtime, gateway, memory, traces,
`agentcore` CLI, `agentcore/agentcore.json`), load
`references/agentcore-handoff.md` and route:

| Intent | Sibling skill in this plugin |
| ------ | ---------------------------- |
| Broken agent / traces / logs / CLI | `skills/agents-debug/SKILL.md` |
| Add capability (memory, VPC, …) | `skills/agents-build/SKILL.md` |
| Evals / observability / cost | `skills/agents-optimize/SKILL.md` |
| Production IAM / auth / sessions / quotas | `skills/agents-harden/SKILL.md` |

While this diagnose skill is active: WRAP + read-only `agentcore traces|logs|status`
only. Mutating `agentcore add|deploy|…` is **suggest-only** until the user leaves
diagnose and runs the handoff skill.

## Token budget (mandatory)

Minimize tokens — no ultra-tier assumptions. **Run phase 0.9** in `orchestrator.md`
(or `dispatch-decision.md`) before every investigation — emit `DISPATCH:` line.

| Reads | Default mode |
| ----- | ------------ |
| ≤2 commands (after merge) | **Inline** in parent |
| 3+ independent commands | **L2 lite** |
| 2+ conversations | **L1** parallel (inline/lite inside per command count) |

Overrides: `DISPATCH_PREFERENCE=auto|inline|parallel`, `TOKEN_SENSITIVE=yes|no`
(default yes). User `inline` wins unless 2+ conversations need L1.

Parent reads `references/aws-ops-compact.md` **by row**, not whole file in prompts.
Sub-agents: max **5 findings × 200 chars**, JSON only. Do not load `services.md`.

Parallel dispatch when phase 0.9 says so:

- **2+ conversations** → L1 parallel (`subagent-conversation-investigator.md`), max 4.
- **3+ independent reads** → L2 lite parallel (`subagent-evidence-lite.md`).

Sub-agents: `readonly: true`, commands pre-filled by parent, JSON only — no reports, no fixes.

## Infra resolution (phase 0.5 — before AWS)

Do not guess Lambda names, log groups, SSM paths, or API routes. Scan SST source:

```bash
python "$SKILL_ROOT/scripts/scan_sst.py" --stage STAGE --search KEYWORD --json
```

Full CLI and scan sets: `references/sst-infra-scan.md`. App map:
`references/sst-app-catalog.md`. Stage vs shared: `references/sst-stage-resolution.md`.

Paste `log_group_hint`, `handler`, `file`, and `resolved_path` into L2 gatherer prompts.

## The read-only guarantee (read this first)

Three layers keep this safe. Do not weaken any of them in sub-agent prompts.

1. **Use the wrapper, not raw boto3/CLI.** Every AWS call goes through
   `$SKILL_ROOT/scripts/aws_read.py`, which refuses mutating
   operations. Sub-agents must use the same path.
2. **Recommend least-privilege credentials.** `ReadOnlyAccess` or
   `references/iam-readonly-policy.json`.
3. **Suggest, never apply.** Fixes are for the human. Sub-agents must not suggest fixes.

If the user asks you to mutate AWS, decline warmly and hand them the change.

## Skill file index

| File | Purpose |
| ---- | ------- |
| `orchestrator.md` | Phase 0/1/2 checklist, dispatch modes, anti-patterns |
| `dispatch-decision.md` | Phase 0.9 — inline vs lite examples + DISPATCH line |
| `references/intake-required.md` | **Ask user** — required fields before investigation |
| `subagent-conversation-investigator.md` | L1 prompt — one conversation |
| `subagent-evidence-lite.md` | **Default** L2 prompt — token-minimal |
| `subagent-evidence-prompt.md` | Legacy L2 shell (avoid unless needed) |
| `subagent-logs.md` | Orchestrator reference — CloudWatch log domains |
| `subagent-api.md` | Orchestrator reference — conversation-service GET |
| `subagent-s3.md` | Orchestrator reference — S3 observability traces |
| `subagents-aws-index.md` | Token budget + domain map |
| `references/aws-ops-compact.md` | **Orchestrator** ops table (per-row, not pasted to sub-agents) |
| `merge-template.md` | Timeline + A vs B comparison tables |
| `report-template.md` | Final report skeleton |
| `subagent-sst-scan.md` | Optional L2 SST scan sub-agent |
| `references/sst-infra-scan.md` | **Phase 0.5** — `scan_sst.py` CLI |
| `references/sst-app-catalog.md` | App → domain map |
| `references/sst-stage-resolution.md` | `stage` vs `sharedStage` |
| `scripts/scan_sst.py` | SST config/stack scanner |
| `references/playbooks.md` | Symptom → hypothesis maps (parent only) |
| `references/services.md` | Detailed ops catalog (parent only, rare) |
| `references/conversation-debug.md` | SFN, bucket, extended playbook |
| `references/agentcore-handoff.md` | Route AgentCore issues → agents-debug/build/optimize/harden |
| `../agents-debug/SKILL.md` | AgentCore debug (sibling skill) |
| `../agents-build/SKILL.md` | AgentCore capabilities (sibling) |
| `../agents-optimize/SKILL.md` | AgentCore evals/observability (sibling) |
| `../agents-harden/SKILL.md` | AgentCore production hardening (sibling) |

## Credentials

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...        # if temporary
export AWS_DEFAULT_REGION=us-east-1
export DIAG_TOKEN='...'             # HTTP GET — user must provide; never echo or commit
```

If AWS creds or `DIAG_TOKEN` (when API needed) are missing, **ask the user** per
`references/intake-required.md` before proceeding.

Orchestrator runs once before dispatch:

```bash
python "$SKILL_ROOT/scripts/aws_read.py" sts get_caller_identity
```

Epoch windows for log filters:

```bash
bash "$SKILL_ROOT/scripts/diag_epoch.sh" --hours-ago 0 --hours-window 2
bash "$SKILL_ROOT/scripts/diag_epoch.sh" \
  --iso-start "2026-07-02T09:55:00Z" --iso-end "2026-07-02T10:15:00Z"
```

## Workflow (orchestrator)

### 1. Scope the problem

Symptom, resource, time window, recent changes. For vague requests, ask 1–2 sharp
questions. See `references/playbooks.md`.

### 2. Form hypotheses

Parent only — drives which L2 domains to dispatch.

### 3. Gather evidence

| Domains | Action |
| ------- | ------ |
| Phase 0.9 → inline | Parent runs WRAP; `aws-ops-compact.md` rows only |
| Phase 0.9 → l2-lite | Parallel `subagent-evidence-lite.md` + `COMMAND_LIST` |
| Phase 0.9 → l1-parallel | One Task per conversation; inline/lite inside per command count |

Parent builds commands from `aws-ops-compact.md` and domain specialist files **once**.
Sub-agents never load those files.

Common wrapper (parent or lite `COMMAND_LIST`):

```bash
SKILL="$SKILL_ROOT/scripts/aws_read.py"

python $SKILL logs filter_log_events \
  --param logGroupName=/aws/lambda/my-fn \
  --param startTime=1718900000000 --param endTime=1718910000000 \
  --param filterPattern=?ERROR \
  --region us-east-1

python $SKILL <service> --list-ops
```

See `references/services.md` for the full catalog.

### 4. Diagnose (parent only)

Merge JSON from sub-agents via `merge-template.md`. Distinguish observed vs
inferred. Rank causes with confidence.

### 4b. Trace to source code (when repo available)

After correlating AWS evidence, map failures to code before writing the report.
Use `scan_sst.py` (`handler`, `file`, `route_key`) plus grep/stack traces.

| Signal | How to resolve |
| ------ | -------------- |
| Lambda log group | `scan_sst.py --topic lambda` → `handler` + stack `file` |
| Log line / error text | Grep workspace |
| Stack trace in CloudWatch | `file.ts:line` from trace |
| HTTP path | `scan_sst.py --topic api` or `api-stack-routes.ts` |
| SFN state | `get_execution_history` → Lambda ARN → handler |

Record confidence: **confirmed** | **likely** | **possible**. See **Code location**
in `report-template.md`.

### 5. Report (parent only)

- Directory: `.aws-details/reports/`
- One file per conversation: `YYYY-MM-DD-HHmm-<slug>-conv-<label>.md`
- Comparative: `...-compare-a-b.md` when user asks or `COMPARATIVE_REPORT=yes`
- Skeleton: `report-template.md`
- Chat: 2–3 lines + path(s) only

## Hard boundaries

- No mutating AWS calls; wrapper blocks them.
- No credential minting (`AssumeRole`, `GetSessionToken`, presign, etc.).
- No secrets or tokens in reports or git.
- Sub-agents do not write reports or diagnose for the user in chat.

---

## conversation-service debugging

AWS via wrapper; **GET only** on conversation-service. Full playbook:
`references/conversation-debug.md`.

### Intake — single conversation

Required fields marked **(R)**. Orchestrator must ask for any missing **(R)** item.

```
STAGE:                          (R) e.g. dev-lshiva
AWS_REGION:                     (R) e.g. us-west-2
API_BASE_URL:                   https://{stage}.api.example.com

TENANT_ID:                      (R)
USER_ID:                        ask if missing
CONVERSATION_ID:                (R)

WEB_MESSAGE_ID:                 ask if web/email issue
EMAIL_MESSAGE_ID:               ask if web/email issue

APPROX_TIME_UTC:                (R)
DID_USER_TYPE_ON_WEB_FIRST:     yes / no / not sure
WORKFLOW_RUN_ID / SFN_EXECUTION_ARN:   optional
DISPATCH_PREFERENCE:            auto | inline | parallel
TOKEN_SENSITIVE:                  yes | no

DIAG_TOKEN:                     (R) in shell env for API/trace — export DIAG_TOKEN='...'
```

Full gate rules: `references/intake-required.md`.

### Intake — multiple conversations (parallel L1)

Per row: **conversation_id**, **tenant_id**, **approx_time_utc** are required.

```
STAGE:                          (R)
AWS_REGION:                     (R)
COMPARATIVE_REPORT:             yes | no
DISPATCH_PREFERENCE:            auto | inline | parallel
TOKEN_SENSITIVE:                  yes | no
DIAG_TOKEN:                     (R) in env if API used

CONVERSATIONS:
  - label: A
    conversation_id:            (R)
    tenant_id:                  (R)
    web_message_id:
    email_message_id:
    approx_time_utc:            (R)
  - label: B
    conversation_id:            (R)
    ...
```

Dispatch **one L1 sub-agent per entry** in parallel. Default: separate report per
label; comparative section when `COMPARATIVE_REPORT=yes`.

### APIs (GET only)

| Purpose | Path |
| ------- | ---- |
| List messages | `/conversations/{id}/messages` |
| Message trace | `/messages/{id}/trace` |
| Agent steps | `/messages/{id}/agent-steps` |

Routes: `apps/conversation-service/sst/stacks/api-stack-routes.ts`

### Web vs email correlation (parent merge)

1. Different `messageId` → different LLM runs.
2. Same `messageId` → one generation; diff may be outbound post-processing.
3. Async push uses `lastUserInteractionChannel`, not SFN `channel`.

Report add-ons: message id table, `metadata.channel`, `channelOutboundReply` in
logs. Redact bodies and tokens.
