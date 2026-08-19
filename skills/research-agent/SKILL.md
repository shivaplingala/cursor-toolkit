---
name: research-agent
description: >-
  Pre-implementation research for features, channels, integrations, infra, and
  bug design. Use whenever the user needs official docs, GitHub samples, AWS/provider
  configuration inventory, or codebase mapping BEFORE writing code — e.g.
  "research WhatsApp channel", "investigate Copilot integration", "design fix for
  [symptom]", "what IAM do we need for X", "compare Twilio vs Meta for SMS".
  Output: cited report at docs/research/YYYY-MM-DD-<slug>-report.md. Does NOT
  implement, deploy, or mutate AWS. If intake fields are missing, ask once and stop.
  For live AWS evidence after deploy, use aws-diagnose-read in parallel — not instead
  of this skill for pre-build research.
---

# Research Agent

Produce a **detailed, cited research report** before any implementation. The human
approves the report; implementation is a separate skill (`full-cycle-delivery` or
direct Ponytail work).

## Hard constraints

1. **No code, no deploy, no AWS writes.** Report only.
2. **No secrets in reports.** Document names and value **shapes** only.
3. **Official docs first.** Every non-obvious claim needs URL + access date.
4. **Mandatory intake** before research — see Phase 0 below.
5. **internal research is mandatory** — graphify, GitNexus, DOX chain.

## Role: orchestrator vs sub-agents

| Role | Who | Responsibilities |
| ---- | --- | ---------------- |
| **Orchestrator** | Parent agent (you when skill is active) | Intake, classify, dispatch, merge, write report, list open questions |
| **Sub-agent** | One per domain (parallel when independent) | Structured JSON or fixed markdown sections — not full prose reports |

Sub-agents: `readonly: true` where supported. Max **8 findings per domain** in JSON;
parent expands in final report.

## Phase 0 — Intake gate (mandatory)

If any **required** field is missing, use `AskQuestion` once and **stop**. Do not
research until intake is complete.

| Field | Required | Example |
| ----- | -------- | ------- |
| Task summary | Yes | "Add WhatsApp async push channel" |
| Research type | Yes | `new-async-channel` (see classifier below) |
| Target workspace(s) | Yes | `apps/channels/` (new), `conversation-service` |
| Provider(s) | Yes | Meta WhatsApp Cloud API, AWS |
| Environment scope | Yes | personal SST stage; no prod |
| Acceptance criteria | Yes | 3–5 bullets |
| Out of scope | Recommended | "No UI admin panel in v1" |
| Constraints | Recommended | "Reuse channels/shared outbound" |
| Need live AWS state? | Yes/No | If yes, appendix via `aws-diagnose-read` |
| Output path | Recommended | `docs/research/YYYY-MM-DD-<slug>-report.md` |

**AskQuestion triggers:**

- Product choice between two provider APIs (e.g. Twilio vs Meta direct)
- Sandbox vs production credentials scope
- Whether integration channel needs outbound callback or persist-only model

Record intake verbatim in the report **Problem / goal / acceptance criteria** section.

## Phase 1 — Classify and select playbook

| Type ID | When | Playbook |
| ------- | ---- | -------- |
| `feature-greenfield` | New capability in existing app | `playbooks/feature-greenfield.md` |
| `new-async-channel` | WhatsApp, SMS — callback + async push | `playbooks/new-async-channel.md` |
| `integration-channel` | ChatGPT, Claude, Copilot — no async push | `playbooks/integration-channel.md` |
| `aws-infra` | SST, IAM, queues, API Gateway splits | `playbooks/aws-infra.md` |
| `third-party-api` | Non-channel external API | `playbooks/third-party-api.md` |
| `bug-design-investigation` | Fix design before coding | `playbooks/bug-design-investigation.md` |
| `config-only` | Portal/AWS setup without code | `playbooks/aws-infra.md` + `references/provider-index.md` |

Read the selected playbook checklist. It drives sub-agent focus and report sections.

## Phase 2 — Parallel research (dispatch sub-agents)

Run independent sub-agents **in parallel** when possible:

| Sub-agent | Prompt file | When to skip |
| --------- | ----------- | ------------ |
| External docs | `subagents/external-docs.md` | Never (always run) |
| GitHub samples | `subagents/github-samples.md` | Pure internal refactor with no external API |
| AWS config catalog | `subagents/aws-config-catalog.md` | No AWS touchpoints |
| codebase | `subagents/codebase.md` | Never (always run) |

**Before codebase sub-agent:** run `graphify query "<task>"` per workspace rules.

Paste into each sub-agent prompt:

- Intake fields (task, type, targets, providers, scope, acceptance criteria)
- Playbook name and top 5 checklist items
- `OUTPUT_FORMAT: json` (see subagent files)

### Optional: live AWS appendix

If intake says **Need live AWS state = Yes**, run `aws-diagnose-read` **in parallel**
for evidence only. Link appendix in report; do not merge incident diagnosis into
recommended approach unless the task is `bug-design-investigation`.

## Phase 3 — Merge and write report

1. **Dedupe** overlapping findings across sub-agents.
2. **Resolve conflicts** — prefer official docs > repo patterns > community. Note disagreements.
3. **Tag confidence** on each major recommendation: `confirmed` | `likely` | `possible`.
4. **Fill configuration inventory** — use `references/config-checklist.md`; mark N/A with reason.
5. **Write report** from `report-template.md` to intake output path (default:
   `docs/research/YYYY-MM-DD-<slug>-report.md`).
6. **List open questions** requiring human decision — do not hide as I'm assumptions.
7. **Stop.** Do not implement, plan tasks, or open PRs.

### Merge rules

- Sub-agent JSON is source for tables; parent adds prose in Executive summary and Recommended approach.
- Every external row in tables needs URL + access date (YYYY-MM-DD).
- paths must be real — verify with graphify/GitNexus/grep before citing.
- If sub-agent returns `gaps[]`, copy to **Risks, unknowns, open questions**.

## Phase 4 — Human gate

Report **Status** starts as `Draft`. User marks `Reviewed` then `Approved` before
implementation. Do not start `full-cycle-delivery` or code until **Approved**.

## Skill file index

| File | Purpose |
| ---- | ------- |
| `report-template.md` | Required output sections |
| `references/source-priority.md` | Official > SDK > internal > community |
| `references/provider-index.md` | Starting URLs by provider |
| `references/internal.md` | Monorepo scan checklist |
| `references/config-checklist.md` | AWS + portal + app config tables |
| `playbooks/*.md` | Type-specific research checklists |
| `subagents/*.md` | Sub-agent prompts and JSON schemas |

## Related skills (do not conflate)

| Skill | When |
| ----- | ---- |
| **research-agent** (this) | Before building — docs, config inventory, design |
| **aws-diagnose-read** | After deploy — logs, live AWS state, incidents |
| **full-cycle-delivery** | After research approved — implement, verify, ship |
| **graphify / GitNexus** | Internal code — used inside codebase sub-agent |

## Example invocation

```
Use research-agent skill.
Task: Research adding WhatsApp as async push channel.
Type: new-async-channel
Providers: Meta WhatsApp Cloud API calls, AWS (SST personal stage)
Target: new apps/channels/whatsapp, conversation-service routing
Output: docs/research/2026-07-02-whatsapp-channel-report.md
Ask intake questions first. Include full AWS + Meta configuration inventory.
Do not implement.
```
