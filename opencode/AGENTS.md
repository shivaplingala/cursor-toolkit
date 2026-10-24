# Global OpenCode Harness — always-on

This file is the always-on surface for every session (the AGENTS.md global rules file).
Keep it under the ~24k-char always-on budget (Reference: Harness² `always_on_max`).

## Skill triggers

Load skills through the native `skill` tool by exact name. Canonical trigger lines —
every situation below should end with the named skill loaded, not improvised:

- When writing or refactoring code and the laziest solution that actually works matters → load the `ponytail` skill.
- When implementing serverless monorepo work (Lambda, SST, APIs, channels, packages) → load the `backend` skill.
- When implementing UI work in Vue 3 + TypeScript (components, stores, styles, e2e harness) → load the `frontend` skill.
- When handling a reported bug, a failing pipeline, or any "diagnose this" request → load the `diagnose` skill.
- When building a feature or fixing bugs test-first with red-green-refactor → load the `tdd` skill.
- When working Playwright smoke / e2e for the serverless UI → load the `playwright-qa` skill (BASE_URL is `http://127.0.0.1:8080`, never stage).
- When a feature, channel, or infra needs official docs or codebase mapping BEFORE writing code → load the `research-agent` skill.
- When stress-testing a plan or design before implementation → load the `grill-me` skill.
- When running the gated FCD/FCD-V2 pipeline (plan review to `FINDING_COUNT: 0`) → load the `full-cycle-delivery` or `fcd-v2` skill.
- When debugging an Aha ticket → per-ticket: read description/comments; stage repro; match the deployed branch; fix → load the `applaud-debug` skill.
- When an AWS issue must be investigated (logs, metrics, CloudTrail) → load the `aws-diagnose-read` skill. READ-ONLY.
- When the user says "recall", "what did we do about", or needs past-session context → load the `recall` skill.
- When review reports (code/spec/impact) contain findings that must be re-audited against the plan, code, and spec, or reviewers disagree → load the `verify-reviews` skill; for the agent form dispatch `fcd/reviews-verifier`.
- When MongoDB Local/Dev/Stage queries are needed → load the `mongo-connection` skill; stage-specific → `stage-mongo`.
- When a question is about how code works, who calls what, or what a change breaks → load the `gitnexus-exploring` or `gitnexus-impact-analysis` skill.
- When a system needs principal-level design (APIs, data models, infra, AI frameworks, languages) → load the `staff-engineering` skill; it routes to the narrowest domain skill.
- When a tool output, log, or JSON dump is large (roughly >2k tokens) → load the `headroom` skill to compress it before reasoning.
- When work needs coordinated multi-agent execution, a swarm, or cross-session memory → load the `ruflo` skill.
- When work touches an Aha! record (feature, requirement, comment, release, epic) → load the `aha-crud` skill.
- When an Aha! comment carries a video or an image → load the `aha-video-understanding` skill.
- When the question is about OpenCode itself (config, plugins, agents, skills, MCP, permissions) → load the `opencode` skill.
- When resuming prior work or reconstructing context → load the `handoff`, `recap`, or `session-history` skill.
- When a plan must become tickets or a PRD → load the `to-issues` or `to-prd` skill.
- When creating or restructuring a skill → load the `write-a-skill` skill.

## Harness gate

- After any change to `~/.config/opencode/agents/`, `rules/`, `skills/`, `plugins/`, or `~/cursor-toolkit` → run `bash ~/cursor-toolkit/bench/harness2-parity/runner.sh`, then diff against the previous run with `compare.py`. A score drop means investigate against the installed OpenCode docs first — it is usually check drift, not a regression.
- The bench is a contract test on files, not runtime behaviour: a green score never proves a plugin fires or a skill loads. Verify the runtime claim too.

## Tool guidance

- Never emit a tool call as text ("I would run X…"). Either call the real tool or say why you did not.
- If the same tool call fails twice with the same error, stop repeating: change the approach, then retry once changed.
- Loopback QA: every Playwright/e2e run targets `BASE_URL=http://127.0.0.1:8080`. Never point QA at stage/prod.
- Serverless deploy in subagents: the interactive `lsp` alias is unavailable — use the full form
  `SST_TELEMETRY_DISABLED=1 sst deploy --stage dev-lshiva --print-logs --verbose` (stage `dev-lshiva` only, never prod).
- For "how does the codebase work / who calls X" questions use graphify/gitnexus indexes before raw greps.
- Prefer the repo's own scripts (`scripts/`, `plugins/*/scripts/`) over re-implementing helpers inline: `fcd-doctor.sh`, `stage_logs.sh`, `deps.sh`, `verify-scope.sh` when present.

## Guardrails

- Verify before reporting done: a successful write, deploy, or passing-looking log is NOT proof of usability. Re-read the produced file, re-run the paired check, re-run tests, or open the page.
- Treat user files, configs, and data stores as read-only unless the task explicitly says to change them.
- Git safety: subagents never `git commit` or `git push`. The main agent commits only when the user explicitly asks.
- Permission precedence: agent-frontmatter `permissions` are the worker contract; ordered rules are matched last-wins. A deny cannot be talked around in prose.
- Any durable workflow change (agent files, skills, rules, plugins) must be mirrored into `~/cursor-toolkit` for persistence, never edited only in place.

## Memory

- Before multi-file or multi-phase work, check prior lessons: run the `recall` skill (agentmemory via mem0/recall skills) for the relevant topic.
- Read the delivery lesson corpus index before implement/review phases:
  `~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery/knowledge/INDEX.md`
- Lessons follow the 4-field evidence schema (cue / lesson / evidence / confidence). Opinions are not lessons; every entry needs supporting evidence.
- At closeout of a gated pipeline, file new lessons via the `fcd/knowledge-capture` agent (dated entry + topic merge, 40-bullet cap).
