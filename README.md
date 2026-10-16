# Cursor Toolkit

Personal collection of **plugins**, **skills**, **rules**, and **agents** for gated delivery across AI code editors.

Repo: [github.com/shivaplingala/cursor-toolkit](https://github.com/shivaplingala/cursor-toolkit)

## Contents

| Path | What |
|------|------|
| `plugins/` | Canonical Cursor plugins (source of truth) |
| `skills/` | Standalone skill copies (backend, frontend, QA, Headroom, Ruflo, grill-me, graphify, …) |
| `rules/` | Global Cursor rules (`.mdc`) |
| `SCRIPT-OS-EXCLUSIONS.md` | Which `.sh` / `.py` run on Linux, macOS, Windows native |

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
4. Runs `install-all-hosts.sh` so the same skills, commands, rules, and agents land on every supported host
5. `--deps` installs CLIs; `--check` verifies files + those CLIs + MCP entries

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

Agents copy to `~/.cursor/agents`, `~/.claude/agents`, `~/.agents/agents`, `~/.config/kilo/agent`.

Antigravity uses **real copies** (not symlinks). Re-run `bash install.sh` after plugin updates.

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
