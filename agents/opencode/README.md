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

Worker agents are `mode: subagent` on purpose: pick an `all`-mode coordinator
(`fcd/orchestrator`, `applaud/orchestrator`, the loops, or the standalone reviewers) as the
session agent and it dispatches workers with fresh context.

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
