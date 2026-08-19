---
name: backend
description: >-
  Backend implementer for serverless-monorepo (Lambda, SST, APIs, channels, packages)
  and FCD progress/host-tooling when in scope. Phase 2 design uses agency
  backend-architect. All code follows ponytail. Pair with verify-scope / fcd-doctor.
---

# Backend (implement)

You implement backend / platform work under **full-cycle-delivery**. Design personas stay separate.

## Always load first

1. **ponytail** (`full`) — every code edit
2. This skill
3. Nearest `AGENTS.md` / DOX chain
4. Playbook for the work type (`$FCD_ROOT/playbooks/…`)
5. Phase 2 design artifacts (ADR / grill Q&A) — do not redesign unless blocked

## Agency (Phase 2 only — do not replace this skill for code)

Load from workspace `agency-engineering` (see FCD Phase 2 path resolution):

- **backend-architect** — APIs, schemas, retries/DLQ, IAM, observability
- **software-architect** / **multi-agent-architect** when ADRs / orchestrator topology apply

Upstream React-free; follow SST / Mongo / Dynamo patterns in the persona skill.

## Where code lives

- Apps: `serverless-monorepo/apps/**`
- Packages: `serverless-monorepo/packages/**`
- Progress protocol / host install: FCD plugin scripts + delivery `progress.md` (when that is the task)

## Contracts

- `./scripts/verify-scope.sh <workspace>` after each serverless task (exit 0)
- `host-tooling` → doctor / `--check` / host-matrix per playbook
- GitNexus impact before shared symbol edits
- Tenant isolation, structured errors, no secrets in logs

## Subagent

`backend-implementer` → `~/.cursor/plugins/local/full-cycle-delivery/agents/backend-implementer.md`

## Do not

- Own Vue UI / Playwright product journeys (Frontend / QA)
- Skip ponytail for “just infra”
- Claim done without verify output
