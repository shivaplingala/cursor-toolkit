# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

- **Coding style:** Skill **ponytail** (`full` unless user sets lite/ultra) for **all** code edits (apps, plugins, install scripts, Playwright harness). Do not substitute another coding-style skill.
- **Aha! comment media:** Skill `aha-video-understanding` in `.claude/skills/` (also `~/.cursor/skills/`, `~/.codex/skills/`, `~/.agents/skills/`, `~/.gemini/config/skills/`). **Read comment text first** (`aha_list_comments.py`). Videos → download + `video-analyzer` MCP. Images → download + built-in Read. Local `aha-mcp` does not return comments. **Delete all local downloads and `/tmp/mcp-video-*` frames after understanding** — no permanent cache.
- **AC-695 WhatsApp/SMS delivery posture:** Build code + infra first (mocks default). **No claim of customer-ready while phone numbers are unconfigured.** After numbers: provision → live flags/ARNs → E2E test → harden bugs/edge cases → then GA. Track % separately for build vs numbers vs live harden (`docs/AC-695-messaging-channels-whatsapp-and-sms/memory.md`).
- **Stage mongo queries:** Skill **stage-mongo** (`~/.cursor/skills/stage-mongo/`, personal — not in git). When the user says go to stage mongo / run a query on stage, SSH + mongo CLI via that skill and return the exact CLI output or error. Do not put SSH passwords in the repo.
- **Applaud debug:** Skill **applaud-debug** (`~/.cursor/skills/applaud-debug/`, personal — not in git; symlinked for Claude `~/.claude/skills`, Codex `~/.codex/skills`, OpenCode `~/.config/opencode/skills`, Antigravity `~/.gemini/config/skills`, and Orca/universal via `~/.agents/skills`). Slash command `/applaud-debug` in Claude `~/.claude/commands`, Codex `~/.codex/prompts`, OpenCode `~/.config/opencode/command`, Antigravity `~/.gemini/config/commands`. Aha ticket or link → read description, comments, **requirements**, acceptance criteria, history, videos, images, and other files → ask if it reproduces on stage. Yes, or not checked yet → reproduce on stage (Playwright spec + browser network/ws/console + stage pm2 or CloudWatch logs) and read the deployed branch. If it reproduces, check out that same branch locally and fix. Verify the fix locally first (`yarn` / `yarn seed` / `yarn server:api`, `npm run dev`, serverless `lsp` to `dev-lshiva`). Then run the same Playwright spec on local and on stage. Do not `npm run dev` in applaud-serverless. Confirm the repro is gone and check other callers of the code you changed. If it does not reproduce, or you get stuck, ask. `agents-debug` stays AgentCore-only.
- **FCD / FCD-V2 plan impact review:** After research, grill-me, grill-with-docs, and a complete plan — before asking for plan approval — run `plan-review-fix-loop` (coding + impact of planned files and where that code is used). Edit the plan until both reviews are `FINDING_COUNT: 0` (0 issues, bugs, edge cases, other). Same gate for `/full-cycle-delivery` and `/fcd-v2`.
- **FCD / FCD-V2 coding review:** `coding-reviewer` must cover correctness, security (validation/auth), maintainability (6+ month readability; JSDoc/comments on complex areas), performance (CPU/memory — flag unjustified high usage), and testing (if/else/switch branches + important paths; unit and integration). Mentor tone; specific findings with why + suggested fix.
- **FCD / FCD-V2 Phase 2 backend design:** Dispatch **`backend-architect`** agent + skill (bundled in FCD plugin). Merge workspace `agency-engineering/backend-architect` Applaud patterns when in applaud-serverless.
- **Staff/principal engineering:** Plugin **`staff-engineering`** (`~/.cursor/plugins/local/staff-engineering/`) — 20 skills at principal level: MERN/MEAN/MEVN (`fullstack-js-stacks`), LangChain/LangGraph/CrewAI/AutoGen, Python/JS/TS/Go, AWS/GCP/Azure/Docker/K8s/Terraform/Ansible. Install: `install-staff-engineering.sh` or `full-cycle-delivery/scripts/install-all-hosts.sh`. Use in FCD Phase 2 via `staff-engineering` router + narrowest domain skill. Aligns with [agency-agents/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering).
- **Host discovery:** Publish FCD / FCD-V2 / staff-engineering / global-tooling to all editors with `~/.cursor/plugins/local/full-cycle-delivery/scripts/install-all-hosts.sh`. Host list: `docs/agent-host-discovery/docs/adr/0003-host-matrix.md`.
- **PR 724 role-collapse commit (ask through 2026-10-26, then delete this bullet):** User will ask about [2007b358](https://github.com/ApplaudSolutions/applaud-serverless/pull/724/changes/2007b358f2cc9f16b5e197625fa06c15f399c0bd) (`fix(reporting): collapse Users role fan-out to one row per user`, 2026-10-01). Inactive/Suspended/Never-Logged-In fanned out one row per role because dedupe only collapsed identical projected rows. `shouldCollapseRolesToUserGrain` + `generateRoleCollapseStages` in `applaud-serverless/apps/reporting-service/src/services/report-query-builder/aggregation-resolver.service.ts`, wired from `query-builder.service.ts` (log `step-11a-role-collapse-to-user-grain`) instead of `generateJoinFanoutDedupeStages`. Distinct `roles.name` are comma-joined; roleless is null. On when `roles_name` is projected, join alias `roles` exists, the report is not grouped/aggregated, and sort is not `roles_name`. Roster grain (sort by `roles_name`, USR-B-07) stays one row per role. Only `roles_name` is combined. Tests: `report-query-builder.test.ts` (`users role collapse to user grain`).

## Child DOX Index

- `gn-graph/AGENTS.md` — Go + SurrealDB code graph (GitNexus/Graphify/CodeGraph unify); `docs/` has implementation plan
- `docs/agent-host-discovery/CONTEXT.md` — glossary for host discovery install (Antigravity skill/command/rule publish); ADRs under `docs/agent-host-discovery/docs/adr/`
- `fcd-cursor-share/AGENTS.md` — zip/share pack: FCD + FCD-V2 + staff-engineering + `install.sh`
- `~/.cursor/plugins/local/staff-engineering/` — staff/principal skills (full-stack, AI frameworks, languages, cloud/DevOps); `INDEX.md`
- `docs/fcd-progress-playwright-qa/AGENTS.md` — FCD progress board + Playwright QA delivery (Backend/Frontend/QA skill split, test cases, progress.md)
- `docs/AIA-242-sub-menu-issue/AGENTS.md` — AIA-242; **implement from `IMPLEMENT.md`**; probe in `report.md`; `AIA-242-report.md` superseded
- `applaud-serverless/docs/AIA-245-full-investigation-report.md` — AIA-245 wait-resume (wrong event stole Wait); diagnosis + shipped fix on `feat/AIA-245-wait-resume-event-match`
- `docs/AC-829-reporting-subject-areas/AGENTS.md` — AC-829 reporting subject areas; start at `findings.md`
- `docs/AC-801-knowledge-reports/AGENTS.md` — AC-801 Knowledge subject areas + OOB reports; **R20 shipped** (`2026-10-21-ac-801-r20-plan.md` tasks T1–T10, board in `progress-status.md`); **Phase 2/3:** `later-phases.md` (do not implement until product picks it up)
- `docs/mcp-chatgpt-copilot-connect/AGENTS.md` — AC-718 Copilot + AC-719 ChatGPT channels (prove existing MCP, private install, listing); Aha contract `plan.md`, live URLs/incidents `memory.md`, long-chat hybrid `hybrid-chat-job-polling-plan.md`
- `applaud-serverless/apps/channels/shared/AGENTS.md` — shared channel libs (telephony, OTP helpers, phone provisioning)
- `applaud-serverless/apps/channels/sms/AGENTS.md` — SMS channel app
- `applaud-serverless/apps/channels/whatsapp/AGENTS.md` — WhatsApp channel app
- `applaud-serverless/apps/identity-management/AGENTS.md` — auth + `appld.link` URL shortener
- `opencode-prompt-compact/AGENTS.md` — compacted OpenCode prompt variants
- (Full recursive index still incomplete — expand when touching other durable trees.)

Add Ponytail as an always-on project rule:

- Before writing code, check: stdlib, native platform, installed dependency, one-line solution.
- Only then write the minimum safe implementation.
- Never cut validation, error handling, security, accessibility, or useful smoke tests.
