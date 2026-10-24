# OpenCode V2 agents

Deployed from `~/.config/opencode/agents/` — nested dirs become namespaced agent IDs
(`fcd/orchestrator`, `applaud/stage-repro`). Frontmatter: `description`, `mode`
(`all` = selectable as session agent + subagent; `subagent` = dispatched only), `color`,
`model`, ordered `permissions` (`{action, resource, effect}`, last match wins).
The Markdown body is the system prompt.

## Layout

| Path | What |
| ---- | ---- |
| `fcd/` (17) | FCD/FCD-V2 delivery pipeline — orchestrator, plan/qa/review-fix loops, architect pair, implementers, reviewers to `FINDING_COUNT: 0`, `reviews-verifier` (audits the review reports against plan/code/spec), knowledge capture |
| `applaud/` (6) | applaud-debug pipeline — orchestrator, ticket-reader, stage-repro, local-matcher, fixer, repro-runner |
| root (3) | standalone reviewers: `spec-reviewer`, `code-reviewer`, `impact-reviewer` |

## Mode policy

`mode: subagent` = dispatched only (fresh child context, never selectable as the
session agent). `mode: all` = selectable as the session agent **and** dispatchable
as a subagent. Current fleet: **8 `all` / 18 `subagent`**.

`mode: all` is reserved for the 8 coordinators — the session-agent entry points:

| `mode: all` | Role |
| ------------ | ---- |
| `fcd/orchestrator`, `applaud/orchestrator` | delivery orchestrators |
| `fcd/plan-review-fix-loop`, `fcd/qa-fix-loop`, `fcd/review-fix-loop` | loop owners |
| `fcd/knowledge-capture` | corpus writer |
| `fcd/architect`, `fcd/backend-architect` | Phase 2 design pair |

Everything else is `mode: subagent`: workers (`fcd/implementer`,
`fcd/backend-implementer`, `fcd/frontend-implementer`, `fcd/qa-engineer`,
`applaud/ticket-reader`, `applaud/stage-repro`, `applaud/local-matcher`,
`applaud/fixer`, `applaud/repro-runner`) and every reviewer/auditor
(`*-reviewer`, `reviews-verifier`, `spec-reviewer`, `impact-reviewer`,
`code-reviewer`). A read-only auditor must never be selectable as the main
session agent. `bench/harness2-parity/checks/c5_subagents.py` fails the build if a
reviewer-class agent is `mode: all`.

## Brief contract

Every body names its canonical prompt/skill and an **Inputs the parent provides**
section, so a child session with fresh context can act without the parent's
transcript. `c5` scores that marker on all 26 briefs.

## Free-model policy

All agents pin free OpenCode-hosted models with variant tiers only — `#high`, `#xhigh`,
`#max` (never below `high`). Variant = task size × context load:

| Variant | Roles |
| ------- | ----- |
| `max` | whole-board / whole-repo context: `fcd/orchestrator`, `applaud/orchestrator` (GLM), `review-fix-loop`, `plan-review-fix-loop` (GLM), `impact-reviewer` (DeepSeek) |
| `xhigh` | small task, many touchpoints / heavy context: implementers, `fixer` (caller sweeps), `local-matcher` (multi-repo boot), `qa-engineer`, `reviews-verifier`, full-diff `pre-ship-reviewer`, media-heavy `ticket-reader` + `stage-repro` (Nemotron VL) |
| `high` | scoped single-task: `spec-reviewer`, `frontend-implementer` |

Models: `opencode/glm-5.3-flash-free` (orchestration + backend code), `opencode/deepseek-v4.1-flash-free` (reviews + design rigor), `opencode/nemotron-3-ultra-free` (UI build / QA / ops), `opencode/nemotron-3.5-super-vl-free` (ticket + browser vision).

Reviews and coordinators are edit/shell-denied or ask-gated; workers deny `git push/commit`.
