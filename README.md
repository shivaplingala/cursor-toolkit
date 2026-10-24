# Cursor Toolkit

Personal collection of **plugins**, **skills**, **rules**, and **agents** for gated delivery across AI code editors.

Repo: [github.com/shivaplingala/cursor-toolkit](https://github.com/shivaplingala/cursor-toolkit)

## Contents

| Path | What |
|------|------|
| `plugins/` | Canonical Cursor plugins (source of truth) |
| `skills/` | Standalone skill copies (backend, frontend, QA, Headroom, Ruflo, grill-me, graphify, …) |
| `rules/` | Global Cursor rules (`.mdc`) |
| `agents/opencode/` | OpenCode V2 agents for FCD/FCD-V2 + applaud-debug (25, free models, variant-tiered) |
| `opencode/` | OpenCode always-on harness: global `AGENTS.md` (skill triggers, tool guidance, guardrails, memory beats) + `plugins/` (budget-guard enforcement) |
| `SCRIPT-OS-EXCLUSIONS.md` | Which `.sh` / `.py` / `.ps1` run on Linux, macOS, Windows native |

### Plugins

| Plugin | Command | What it does |
|--------|---------|----------------|
| **full-cycle-delivery** | `/full-cycle-delivery` | Gated plan → implement → dual review to 0 → verify → ship |
| **fcd-v2** | `/fcd-v2` | Same FCD gates; optional Ruflo swarm in Phase 4 |
| **staff-engineering** | load `staff-engineering` | Staff/principal router + 19 domain skills |
| **global-tooling** | — | Headroom, Ruflo, FCD router rules |
| **aws-diagnose** | — | Read-only AWS/SST diagnostics |

**Bundled with FCD (not a separate plugin):** `backend-architect` skill + agent for Phase 2 APIs / Lambda / data / IAM.

### Standalone skills (host publish)

| Skill | Command | Notes |
|-------|---------|--------|
| **applaud-debug** | `/applaud-debug` | Aha ticket → stage repro → fix; needs **aha-video-understanding**, **graphify**, optional **stage-mongo** (local) |

### OpenCode agents

`agents/opencode/` holds 26 OpenCode V2 agents for the gated pipelines — markdown +
frontmatter (`description`, `mode`, `color`, `model`, ordered `permissions`
`{action, resource, effect}`, last match wins), body = system prompt.
`bash install.sh` syncs them to `~/.config/opencode/agents/` (override with
`OPENCODE_AGENTS`; `--check` gates on the orchestrator pair and on every plugin in
`opencode/plugins/` being installed live).

| Group | Agents | Modes |
|-------|--------|-------|
| `fcd/` (17) | `orchestrator`, `plan-review-fix-loop`, `qa-fix-loop`, `review-fix-loop`, `knowledge-capture` · `architect` + `backend-architect` · `backend-implementer`, `frontend-implementer`, `implementer` · `spec-reviewer`, `coding-reviewer`, `impact-reviewer`, `quality-reviewer`, `pre-ship-reviewer`, `reviews-verifier` · `qa-engineer` | loops/knowledge-capture = `all`, workers + reviewers = `subagent` |
| `applaud/` (6) | `orchestrator` · `ticket-reader`, `stage-repro`, `local-matcher`, `fixer`, `repro-runner` | orchestrator = `all`, workers = `subagent` |
| root (3) | `spec-reviewer`, `code-reviewer`, `impact-reviewer` | `subagent` |

Pick an `all`-mode coordinator as the session agent; workers and reviewers run only
as fresh-context subagents it dispatches. Reviewers are `subagent`-only by policy —
a read-only auditor must never be selectable as the main session agent
(`bench/harness2-parity/checks/c5_subagents.py` fails the build if one is `all`).
Reviewers and loops are edit/shell-denied or
ask-gated (`impact-reviewer` may run only `graphify`); workers deny `git push/commit`;
`local-matcher` alone can deploy serverless via `lsp` to personal stage `dev-lshiva`.
Full role map and guardrail details: [`agents/README.md`](agents/README.md).

**Free-model policy** — every agent pins a free OpenCode-hosted model; the variant reflects
task size × context load and is never below `#high`:

| Variant | Where |
|---------|-------|
| `#max` | whole-board / whole-repo context: `fcd/orchestrator`, `applaud/orchestrator`, `review-fix-loop`, `plan-review-fix-loop` (GLM-5.3-Flash Free); `impact-reviewer` (DeepSeek V4.1 Flash Free) |
| `#xhigh` | small tasks, many touchpoints: `backend-implementer`, `implementer`, `fixer`, `qa-fix-loop`, `knowledge-capture` (GLM); `coding-reviewer`, `quality-reviewer`, `pre-ship-reviewer`, `backend-architect`, `architect`, `repro-runner` (DeepSeek); `qa-engineer`, `local-matcher` (Nemotron 3 Ultra Free); `ticket-reader`, `stage-repro` (Nemotron 3.5 Super VL Free) |
| `#high` | scoped single-task: `spec-reviewer` (DeepSeek), `frontend-implementer` (Nemotron 3 Ultra Free) |

`bash install.sh` runs `scripts/install-applaud-debug.sh` so the skill and command land on Cursor, Claude, Codex, OpenCode, Antigravity, Zed, Kilo, Kimi, Qwen, and DeepSeek paths (see host matrix below).

### Not included

- **stage-mongo** — credentials; keep local only
- **Cursor marketplace plugins** — install from the Cursor plugin store

## Install

```bash
git clone https://github.com/shivaplingala/cursor-toolkit.git
cd cursor-toolkit
bash install.sh          # files + publish to all hosts
bash install.sh --deps   # CLIs used by skills (boto3, whisper, graphify, headroom, ruflo)
```

**OS:** Linux and macOS (Terminal). Windows: **Git Bash or WSL** — not `cmd.exe` or PowerShell. `--deps` uses apt (Linux), Homebrew (macOS), or prints winget hints (Windows). If `ln -s` fails, skills are copied instead.

Then **reload every editor** you use (Cursor, Claude Code, Codex, …).

```bash
bash install.sh --check
```

Health after install:

```bash
~/.cursor/plugins/local/full-cycle-delivery/scripts/fcd-doctor.sh
~/.cursor/plugins/local/full-cycle-delivery/scripts/install-all-hosts.sh --check
```

## What `install.sh` does

1. Copies plugins into `~/.cursor/plugins/local/`
2. Copies standalone skills into `~/.cursor/skills/`
3. Copies rules into `~/.cursor/rules/`
4. Syncs `agents/opencode/` into `~/.config/opencode/agents/` (OpenCode V2 agents)
5. Copies `opencode/AGENTS.md` + `opencode/plugins/` into `~/.config/opencode/`
6. Installs the **pre-commit harness gate** into `.git/hooks/pre-commit`
7. Runs `install-all-hosts.sh` so the same skills, commands, rules, and agents land on every supported host
8. `--deps` installs CLIs; `--check` verifies files + every opencode plugin + those CLIs + MCP entries

## Harness gate (harness2-parity bench)

`bench/harness2-parity/` grades this toolkit's OpenCode setup against the eight
Harness² levers plus two local checks (install parity, runtime load). Ten checks,
deterministic, no model calls.

```bash
bash bench/harness2-parity/runner.sh          # score + table, writes a result file
bash scripts/bench-verify.sh                   # gate: exits non-zero when red
python3 bench/harness2-parity/compare.py A.json B.json   # diff two runs
```

Enforcement, so a green score is not optional:

| Where | What it does |
| ----- | ------------ |
| `scripts/bench-gate.py` | single gate decision point: exits 1 unless **every** check scored 1.0 (the average must also clear `BENCH_THRESHOLD`) |
| `scripts/bench-verify.sh` | runs the bench + gate and exits 1 on any weak check |
| `.git/hooks/pre-commit` (installed by `install.sh`) | blocks a commit that stages `agents/`, `rules/`, `opencode/`, `skills/`, `scripts/`, `install.sh`, `bench/` while the gate is red |
| `~/.config/opencode/plugins/bench-guard.js` | always-on nudge: one line in the system context when the last run was red or older than 24h |
| `~/.config/opencode/AGENTS.md` → *Harness gate* | every agent is told to run the bench after a harness change |

Current: **10/10 checks, total 1.000** (2026-10-22). Baselines and the ranked
improvement history live in `bench/harness2-parity/BENCHMARK.md`.

## Hosts

One catalog: `plugins/full-cycle-delivery/scripts/lib/host-discovery.sh`.

| Host | Skills | Commands | Rules |
|------|--------|----------|-------|
| **Cursor** | `~/.cursor/skills/` | `~/.cursor/commands/` | plugin + `~/.cursor/rules/*.mdc` |
| **Claude Code** | `~/.claude/skills/` | `~/.claude/commands/` | stripped `~/.claude/rules/*.md` |
| **GLM Coding Plan** | Claude Code paths | same as Claude | same |
| **GLM ZCode** | `~/.zcode/skills/` | skill as `/name` | — |
| **Codex** | `~/.codex/skills/` | `~/.codex/prompts/` | stripped `~/.codex/rules/*.md` |
| **Antigravity / Gemini** | **copy** both Gemini skill roots | both command roots | dual `.mdc` + stripped `.md` |
| **Zed** | `~/.agents/skills/` | `~/.agents/commands/` | — |
| **OpenCode** | `~/.config/opencode/skills/` | `~/.config/opencode/command/` | — |
| **Kilo Code** | `~/.kilo/skills/` | `~/.config/kilo/command/` | — |
| **Kimi Code** | `~/.kimi-code/skills/` | `~/.kimi-code/commands/` | — |
| **Qwen Code** | `~/.qwen/skills/` | `~/.qwen/commands/` | — |
| **DeepSeek Harness** | `~/.dsh/skills/` and `~/.agents/skills/` | — | — |
| **Orca** | universal `~/.agents/skills/`; aggregates every agent home (`orca skills installed`) | — | — |

Agents copy to `~/.cursor/agents`, `~/.claude/agents`, `~/.agents/agents`, `~/.config/kilo/agent`; OpenCode agents sync to `~/.config/opencode/agents` via `install.sh`.

Antigravity uses **real copies** (not symlinks). Re-run `bash install.sh` after plugin updates.

Config mirrors kept in-repo: `opencode/rules/` (`~/.config/opencode/rules/*.md`), `opencode/plugins/orca-*` (Orca status panel plugins), `docs/agent-host-discovery/` (host-matrix ADRs), `docs/instructions/applaud-AGENTS.md` (applaud workspace DOX snapshot). Refresh these copies whenever the live files change.

## Full-cycle delivery (FCD)

Iron laws: grill-me then grill-with-docs, then plan coding+impact review to **0 findings**, then human plan approval, then implement. No autonomous prod merge.

| Phase | What happens |
|-------|----------------|
| 2 Design | `staff-engineering` + domain skill; **`backend-architect`** for APIs/data/IAM |
| 3 Plan | `plan-review-fix-loop` until coding + impact `FINDING_COUNT: 0` |
| 4–5 Code | Implement → spec-review → **coding-reviewer + impact-reviewer** until both 0 |
| 6–7 | Verify, QA gate (localhost), pre-ship, human merge |

**Coding review** (mentor tone, not style nits):

1. **Correctness** — does it do what it should?
2. **Security** — validation, auth, vulnerabilities
3. **Maintainability** — readable in 6+ months; JSDoc/comments on complex areas
4. **Performance** — CPU/memory; flag unjustified high usage
5. **Testing** — if/else/switch branches and important paths (unit + integration)

**Impact review** uses **graphify and GitNexus together**.

FCD-V2 is the same pipeline; Phase 4 may use a Ruflo swarm when escalate score ≥ 2.

## Staff engineering

Load **`staff-engineering`** first, then the narrowest domain skill. Index: `plugins/staff-engineering/INDEX.md`.

| Area | Skills |
|------|--------|
| Full-stack | `fullstack-js-stacks` (MERN / MEVN / MEAN) |
| Languages | `python-principal`, `javascript-principal`, `typescript-principal`, `golang-principal` |
| AI | `langchain-principal`, `langgraph-principal`, `crewai-principal`, `autogen-principal`, `ai-agent-frameworks` |
| Cloud / DevOps | `aws-principal`, `gcp-principal`, `azure-principal`, `docker-principal`, `kubernetes-principal`, `terraform-principal`, `ansible-principal`, `devops-cloud-platforms` |
| Meta | `staff-engineering` (router), `staff-fullstack-ai-engineer` |

Aligned with [agency-agents/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering). Phase 4 code still uses **ponytail**.

## Dependencies

Skills are markdown; they **call** these tools. `bash install.sh` copies files. `bash install.sh --deps` installs CLIs + MCP stubs (does **not** overwrite existing `mcp.json` servers, so tokens stay).

| Plugin / skill | Installs / checks |
|----------------|-------------------|
| **full-cycle-delivery** | Companion skills in this repo; **graphify** + MCP **gitnexus** (impact uses **both**); **gh** |
| **fcd-v2** | Same impact stack as FCD; **ruflo** + **headroom** CLIs and MCP |
| **staff-engineering** | No extra CLI (markdown skills) |
| **global-tooling** | **headroom** (`uv tool install headroom-ai`), **ruflo** (`npm i -g ruflo`) |
| **aws-diagnose** / **agents-*** | **python3**, **boto3**, **jq**; optional **aws** CLI, **agentcore** |
| **aha-video-understanding** | **ffmpeg**, **openai-whisper**, **yt-dlp**, **tesseract**; MCP **aha-mcp** + **video-analyzer** |
| **applaud-debug** | **node** + `npm i` in `skills/applaud-debug` for repro Playwright; **graphify**; **aha-video-understanding**; optional personal **stage-mongo** |
| **graphify** | `uv tool install graphifyy` |
| **agentmemory-*** / remember / recall / … | MCP **agentmemory** (`npx @agentmemory/mcp`) |
| **codebase-doc-*** | **node** (bundled `.mjs` scripts) |
| **playwright-qa** | App-repo Playwright (`npm run test:e2e`), not global |
| **setup-pre-commit** | `npx husky` in the target repo |
| Prompt-only (ponytail, grill-*, tdd, review, …) | No extra CLI |

`--deps` also ensures `uv`, pip packages, npm globals, and MCP stubs. Fill `AHA_API_TOKEN` / `AHA_DOMAIN` in `aha-mcp` if those env keys are empty. Reload after.

## Owner: refresh from this machine

After editing plugins/skills locally:

```bash
bash install.sh --pack
git add -A && git commit -m "Refresh toolkit from local install"
git push
```

## License

See [LICENSE](LICENSE). Plugin-specific licenses remain in each plugin folder.
