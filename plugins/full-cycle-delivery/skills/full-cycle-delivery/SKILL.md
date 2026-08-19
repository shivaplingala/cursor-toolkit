---
name: full-cycle-delivery
description: >-
  End-to-end gated delivery (intake → research → grill → plan approval →
  implement → dual code review with fix-until-zero → verify → ship). Use for
  features, channels, bug fixes, packages, workflow, and infra — especially in
  serverless-monorepo. Planning (Phases 2–3) REQUIRES grill-me then grill-with-docs
  before plan approval. After approval, Phases 4–7 MUST stay on this skill.
  When external research needed, run research-agent first and require Approved report.
  Installed globally via ~/.cursor/plugins/local/full-cycle-delivery.
---

# Full-Cycle Delivery

Repeatable delivery pipeline (primary target: `serverless-monorepo` monorepo).
**Global install:** this skill lives under
`~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery`
(also linked from `~/.cursor/skills/full-cycle-delivery`). Not workspace-bound.

**Iron laws:**

1. **No completion claims without fresh verify output** (verification-before-completion).
2. **Human plan approval** before Phase 4 (implement).
3. **No autonomous prod deploy or PR merge.**
4. **Planning must grill:** Phases 2–3 MUST invoke **grill-me** then **grill-with-docs** (read + follow each skill) before asking for plan approval. Do not skip, summarize, or substitute with AskQuestion-only.
5. **Implementation stays on this skill:** After plan approval, Phases 4–7 MUST continue under **full-cycle-delivery** (playbooks, prompts, verify-scope, review matrix). Do not freestyle implement outside this pipeline. Nested skills (subagent-driven-development, autonomous-dev-loop, verification-before-completion) run *as prescribed by this skill*, not instead of it.
6. **Grow knowledge every usage:** Read `$SKILL_ROOT/knowledge/` before Phase 4; run `prompts/knowledge-capture.md` on Phase 7 (and mid-delivery when a sharp lesson appears). Shared with `/fcd-v2`.

## Path resolution (global + workspace)

`$SKILL_ROOT` = this skill directory (plugin or `~/.cursor/skills/full-cycle-delivery`).
`$REPO` = open workspace root when delivering (usually `serverless-monorepo`).

| Path | Purpose |
| ---- | ------- |
| `$SKILL_ROOT/playbooks/*.md` | Work-type checklists |
| `$SKILL_ROOT/prompts/*.md` | Subagent briefs (implementer, reviewers, architect, review-fix loop, **qa**, **knowledge-capture**) |
| `$SKILL_ROOT/knowledge/` | Growing delivery craft (build / debug / fix / performance / qa / swarm + log) — shared with FCD-V2 |
| `$SKILL_ROOT/prompts/review-fix-loop.md` | Main-agent protocol: coding + impact → fix until 0 |
| `~/.cursor/skills/research-agent/` (or `$REPO/.claude/skills/research-agent/`) | Pre-build research |
| `$REPO/scripts/verify-scope.sh` | Per-workspace verify (required when in serverless-monorepo) |
| `$REPO/docs/plans/TEMPLATE.md` | Implementation plan template |
| `$REPO/docs/architecture/channel-capability-matrix.md` | Channel classifier |
| `$REPO/skills-agents-autos-plans/FULL-CYCLE-DELIVERY-PLAN.md` | Full spec (when present) |

## Mandatory skill gates

```text
Phase 0–1  →  intake + research (research-agent when needed)
Phase 2–3  →  design/plan + grill-me → grill-with-docs → human plan approval
Phase 4–7  →  full-cycle-delivery only (implement → review → integrate → ship)
```

| Gate | Required skills | Fail closed |
| ---- | --------------- | ----------- |
| Before plan approval (end of Phase 3) | **grill-me** then **grill-with-docs** | No Phase 4 without both sessions completed and shared understanding recorded |
| Phase 4+ | **full-cycle-delivery** (this skill) + `subagent-driven-development` + `verification-before-completion` | No ad-hoc coding outside playbook/prompts/verify loop |

**Grill order (mandatory):**

1. Load and follow **grill-me** — one question at a time; explore codebase when a question is answerable that way; recommend an answer each time. **After each locked answer**, append it under `## Grill-Q&A` in the active plan file (create the heading if missing). Format: `- Q: … A: …`.
2. Load and follow **grill-with-docs** — same interview style, but challenge against domain docs (`CONTEXT.md` / glossary), sharpen terms, update docs/ADRs inline when decisions crystallise. Append the same way under `## Grill-Q&A` (prefix with `(docs)` if useful).
3. Only then: request explicit human plan approval and stop if not approved.

**Plan waivers:** Optional plan section `## WAIVED` lists nits the human accepts with a one-line reason. Coding/impact reviewers must not count those toward `FINDING_COUNT` (still list under `WAIVED:`). Blockers / should-fix / edge-case cannot be waived without a new human approval line.

**Verify note:** `verify-scope` is required for serverless-monorepo workspaces. For `host-tooling`, use `scripts/fcd-doctor.sh` / `install-*.sh --check` / `scripts/test-host-matrix.sh` instead — see playbook.

**Progress ledger (resume):** After plan approval (end of Phase 3), create `docs/plans/YYYY-MM-DD-<slug>.progress.md` from `$SKILL_ROOT/templates/progress.md` (or `.fcd-v2/<slug>/progress.md` when using FCD-V2 swarm layout). On **every** later `/full-cycle-delivery` or `/fcd-v2` start for that work: if a progress file exists → **read it first and resume**; do not re-intake or re-grill locked decisions. Keep Tasks rows updated (status, agent, coding/impact, verify, history). Fat detail → `briefs/` + `sidecars/`; never dump findings into swarm `memory.md` (pointers only). Coding edits: skill **ponytail** only.

**Knowledge (grow every usage):** On implement start, skim `$SKILL_ROOT/knowledge/INDEX.md` + topic files that match the work (build/debug/fix/performance/qa). Capture lessons via `prompts/knowledge-capture.md` — mandatory at Phase 7 / meaningful stop; optional mid-flight for sharp wins. FCD-V2 writes the **same** corpus (`$FCD_ROOT/knowledge/`).

Announce when entering each: `Using grill-me to stress-test the plan` / `Using grill-with-docs to align with domain docs`.

## Phase 0 — Intake (mandatory)

If fewer than 2 of {trigger, outcome, scope, deploy env} are known, use `AskQuestion` once and **stop**.

**Classifier questions:**

1. Work type ID (table below)
2. Workspace(s) in scope
3. Acceptance criteria (3–5 bullets)
4. Shared symbols? → GitNexus impact required
5. Auth/secrets/webhooks? → security-review required
6. Deploy boundary: local / personal SST / prod path
7. Cross-cutting: workflow channel, i18n, authz, multi-tenant

### Work-type classifier

| Work type ID | When | Playbook |
| ------------ | ---- | -------- |
| `async-channel-greenfield` | New push channel (WhatsApp, SMS) | `playbooks/async-channel-greenfield.md` |
| `async-channel-extension` | Outbound push for existing channel app | `playbooks/async-channel-extension.md` |
| `integration-channel` | No async push (ChatGPT, Claude, Copilot) | `playbooks/integration-channel.md` |
| `conversation-service-feature` | Orchestrator, messages, tools | `playbooks/conversation-service-feature.md` |
| `workflow-feature` | SFN, run-agent, workflow UI | `playbooks/workflow-feature.md` |
| `platform-app-feature` | Identity, tenant, case, analytics | `playbooks/platform-app-feature.md` |
| `package-library` | Shared npm package | `playbooks/package-library.md` |
| `connector-feature` | Knowledge / SharePoint connectors | `playbooks/connector-feature.md` |
| `frontend-package` | Vue UI libraries | `playbooks/frontend-package.md` |
| `infra-sst` | Stacks, SSM, IAM, queues | `playbooks/infra-sst.md` |
| `bugfix-minimal` | Smallest diff bug fix | `playbooks/bugfix-minimal.md` |
| `host-tooling` | User-global plugins / install / skill discovery (not serverless apps) | `playbooks/host-tooling.md` |

Channel matrix: `docs/architecture/channel-capability-matrix.md`

## Phase 1 — Research

| Need | Skill / tools | Output |
| ---- | ------------- | ------ |
| External docs, GitHub, full config inventory | **research-agent** | `docs/research/YYYY-MM-DD-<slug>-report.md` |
| Small bugfix, known internal pattern | graphify + GitNexus + DOX | `docs/plans/YYYY-MM-DD-<slug>-research.md` |

**Gate:** research-agent reports must be **Approved** before Phase 2 when used.

Lightweight research must include: files/symbols to touch, patterns to reuse, GitNexus blast radius, risks.

## Phase 2 — Design and architecture

**Personas (agency-agents):** Resolve `agency-engineering` from the open workspace first:

1. `$REPO/serverless-monorepo/.cursor/skills/agency-engineering/` (or `.claude/skills/agency-engineering/`)
2. `$REPO/.cursor/skills/agency-engineering/` if present
3. Else fail closed for persona load: use `prompts/architect.md` + link upstream from `AGENCY-AGENTS-ENGINEERING.md` — do **not** invent a parallel architect skill

Router: `agency-engineering/SKILL.md` + `INDEX.md`.

| Need | Persona skill |
| ---- | ------------- |
| APIs / Lambda / data / IAM | `backend-architect` |
| Vue UI contracts / a11y | `frontend-developer` (Vue appendix; ignore React) |
| Orchestrator / SFN / agents | `multi-agent-architect` |
| Module boundaries / ADR | `software-architect` |
| Mail / MIME → LLM | `email-intelligence` |
| Prompts | `prompt-engineer` |

**QA is not a Phase 2 architect persona** — catalog work starts Phase 3/4 via **qa-engineer**. Reality-Checker posture (evidence before “ready”) applies at Phase 6–7.

**Deliverables:** ADR for structural decisions (`docs/adrs/TEMPLATE.md`); two options + trade-offs; failure-mode notes; UI contract when Frontend in scope.

Dispatch `prompts/architect.md` for non-trivial design.

**Mandatory grill (design):** After draft options exist, run **grill-me** then **grill-with-docs** on the design tree before Phase 3. Do not proceed on unresolved branches.

## Phase 3 — Implementation plan

**Skill:** writing-plans

**Output:** `docs/plans/YYYY-MM-DD-<slug>.md` from `docs/plans/TEMPLATE.md`

**Mandatory grill (plan):** After the draft plan exists, run **grill-me** then **grill-with-docs** again on the plan (tasks, verify commands, risks, docs impact). Update the plan (and CONTEXT/ADRs if grill-with-docs requires it) until shared understanding.

**Human gate:** explicit plan approval before Phase 4 — only after both grill sessions complete.

**Stop rule:** If the user has not approved the grilled plan, **stop**. Do not start Phase 4.

**QA in the plan:** When the delivery is user-facing, touches `ui-vue3-app`, or needs Playwright/resume-board gates, include QA tasks (catalog, id-map, gate, smoke, sign-off). Dispatch via `prompts/qa.md` / agent **`qa-engineer`**.

## Phase 4 — Implement (per task)

**Stay on full-cycle-delivery.** Nested skill: subagent-driven-development (required; does not replace this skill).

**Before first task:** skim `$SKILL_ROOT/knowledge/` for prior build/debug/fix/perf/qa lessons that apply.

1. Prefer **QA first** when plan has catalog/gate tasks: dispatch **`qa-engineer`** (`prompts/qa.md`) before Frontend harness work depends on case IDs.
2. Dispatch implementer with task, playbook excerpt, GitNexus impact (**ponytail** for all code):
   - Serverless / packages / host-tooling / progress protocol → agent **`backend-implementer`** + skill **backend** (`prompts/backend.md`)
   - UI / `ui-vue3-app` → agent **`frontend-implementer`** + skill **frontend** (+ **playwright-qa** for E2E)
   - QA catalog / gate / smoke / sign-off → agent **`qa-engineer`** + skills **qa** / **playwright-qa**
   - Else → `prompts/implementer.md`
3. Verify after each task (exit 0 required):
   - serverless-monorepo workspaces → `./scripts/verify-scope.sh <workspace>`
   - `host-tooling` → `bash -n` on touched scripts + `scripts/fcd-doctor.sh` and/or that plugin’s `install-*.sh --check` (+ `scripts/test-host-matrix.sh` when install layout changed)
   - QA smoke → `npm run test:e2e` (or plan command); record gate in progress
4. Update **progress.md**: task status, agent, verify; on subagent spawn create `briefs/T<id>.md` and a Tasks row
5. Dispatch `prompts/spec-reviewer.md` → fix until plan matches
6. **Zero-finding review loop** — follow `prompts/review-fix-loop.md` end to end:
   - Dispatch `prompts/coding-reviewer.md` (coding / bugs / edge cases) — read-only; reports to main agent
   - Dispatch `prompts/impact-reviewer.md` (full codebase impact via GitNexus + graphify) — read-only; reports to main agent
   - Write `sidecars/T<id>.round-<n>.md` with STATUS / FINDING_COUNT / OPEN; set Tasks `coding` / `impact` / `history` (e.g. `R1 FAIL → R2`)
   - Main agent merges findings and dispatches fixes (`backend-implementer` / `frontend-implementer` / `implementer` or inline)
   - Re-verify + re-review until **both** return `PASS` with `FINDING_COUNT: 0`
7. Mark task `done` only when coding PASS 0, impact PASS 0, and verify green (unless human `deferred`). QA tasks: gate/status vocabulary from **qa** / progress template.
8. Check off tasks in plan only after the loop exits clean (QA non-code tasks: catalog/gate reviewed, no review-fix required unless they changed product code)

**Also apply** `prompts/quality-reviewer.md` checklist inside coding review (domain rows).

**Iteration limits:** verify 5×/task; review-fix loop max **10 rounds**/task then escalate to human with open findings. Do **not** advance with open blocker / should-fix / edge-case.

Optional pairing: `autonomous-dev-loop` for fix/retest — still under this skill’s Phase 4–6 gates.

## Phase 5 — Cross-cutting review

Apply applicable rows from review matrix in `FULL-CYCLE-DELIVERY-PLAN.md` §10.

Re-run the **zero-finding review loop** on the whole-branch diff (coding + impact) before Phase 6. Same exit rule: both `PASS` / `FINDING_COUNT: 0`.

## Phase 6 — Integration

1. `npm run build:packages` if packages touched
2. Scoped or full `npm run build`
3. Root `npm run quality` (minimum) or `quality:full` (large features)
4. Personal SST deploy if infra/channels touched
5. Smoke per work type (plan §17)
6. **QA gate + fix loop:** When plan has QA / UI E2E tasks, follow **`prompts/qa-fix-loop.md`**:
   - **localhost only** (`http://127.0.0.1:8080`) — never Playwright-Automation remote envs for local QA
   - Dispatch **`qa-engineer`** → FAIL_LIST to orchestrator → **backend-implementer** / **frontend-implementer** fix → impact → targeted QA → full QA
   - Exit only when `QA_ISSUE_COUNT: 0` (or human waiver); write `sidecars/qa-round-<n>.md`
   - Update **progress.md** (Tasks + history)

## Phase 7 — Ship

1. Open PR; CI green (`.github/workflows/ci.yml`)
2. bugbot + code-reviewer; dispatch `prompts/pre-ship-reviewer.md`
3. Confirm last review-fix round was clean (coding + impact `FINDING_COUNT: 0`)
4. **QA sign-off:** when QA was in the plan or UI E2E ran — `qa-engineer` returns `SIGN_OFF: ready` (or human waiver). File open defects via **qa** skill before claiming ship-ready.
5. **Knowledge capture (mandatory):** follow `prompts/knowledge-capture.md` — append durable build/debug/fix/performance/qa lessons to `$SKILL_ROOT/knowledge/` (shared with FCD-V2). Note in progress history.
6. Human merges — never autonomous prod

## Review matrix (summary)

Always: work-type verify (`verify-scope` **or** host-tooling doctor/matrix) + **coding + impact review-fix loop to 0 findings**. For serverless-monorepo features also `npm run quality` when applicable. When applicable: GitNexus impact, security-review, Multi-Agent checklist, authz, i18n, workflow channel, DOX pass, channel plug-in checklist, prompt regression, staging smoke.

Full matrix: `skills-agents-autos-plans/FULL-CYCLE-DELIVERY-PLAN.md` §10.

## Exit criteria (production candidate)

- [ ] grill-me + grill-with-docs completed before plan approval
- [ ] Plan explicitly approved
- [ ] All plan tasks checked under full-cycle-delivery (not freestyle)
- [ ] `verify-scope` green for every touched serverless-monorepo workspace **or** host-tooling doctor/matrix/`--check` green when work type is `host-tooling`
- [ ] `npm run quality` green (or `quality:full`) when serverless/packages touched; skip for plugin-only host-tooling
- [ ] Coding + impact review-fix loop exited with 0 findings (per task and whole-branch)
- [ ] QA gate PASS (or N/A / waived) when UI E2E or QA tasks were in scope; sign-off ready before merge
- [ ] Knowledge capture run (`prompts/knowledge-capture.md`) — `captured` or `none-new` recorded in progress
- [ ] Review matrix applied
- [ ] DOX updated
- [ ] PR open; CI green
- [ ] Human approved merge

## Example prompts

### Async channel greenfield

```
Use full-cycle-delivery skill.
Work type: async-channel-greenfield
Task: Add WhatsApp channel (after research report Approved).
Run research-agent first if no Approved report exists.
Phases 2–3: grill-me then grill-with-docs before plan approval.
After approval: stay on full-cycle-delivery for implement → ship.
Personal SST stage only.
```

### Bugfix minimal

```
Use full-cycle-delivery skill.
Work type: bugfix-minimal
Ponytail only — smallest diff.
Still grill-me + grill-with-docs on the plan before implement.
verify-scope on touched workspace only.
```

## Related skills

| Skill | When |
| ----- | ---- |
| **grill-me** | **Required** Phases 2–3 — stress-test design/plan (before approval) |
| **grill-with-docs** | **Required** Phases 2–3 — domain/glossary/ADR alignment (after grill-me) |
| research-agent | Pre-build external/provider research |
| writing-plans | Phase 3 plan draft (before final grill + approval) |
| autonomous-dev-loop | Phases 4–8 fix/retest loop with `scripts/loop-controller.sh` (under this skill) |
| agency-engineering (workspace) | Phase 2 personas — see Phase 2 path resolution |
| aws-diagnose-read | Post-deploy incident evidence |
| **ponytail** | **Required for all code edits** (backend / frontend / QA tests). Invokable skill + always-on rule |
| **backend** | Serverless / host-tooling implement; agent **backend-implementer**; Phase 2 design → agency **backend-architect** |
| **frontend** | Vue 3 implement; agent **frontend-implementer**; Phase 2 design → agency **frontend-developer** |
| **qa** | Catalog / defects / sign-off; agent **qa-engineer**; Phase 6–7 Reality-Checker evidence posture |
| **playwright-qa** | UI E2E under **qa-engineer** / FE harness |
| **knowledge/** + `knowledge-capture` | Growing delivery craft — read Phase 4; write Phase 7 / sharp mid-flight lessons |
| subagent-driven-development | Phase 4 implementation (nested under this skill) |
| verification-before-completion | Before any "done" claim |
