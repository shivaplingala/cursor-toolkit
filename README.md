# Cursor Toolkit

Personal collection of **Cursor plugins**, **skills**, and **rules** for agent-assisted development.

## Contents

| Path | What |
|------|------|
| `plugins/` | Cursor local plugins (FCD, FCD-V2, global tooling, AWS diagnose) |
| `skills/` | Standalone agent skills (backend, frontend, QA, Headroom, Ruflo, grill-me, graphify, …) |
| `rules/` | Global Cursor rules (`.mdc`) |

### Plugins

- **full-cycle-delivery** — gated plan→build→verify→ship (`/full-cycle-delivery`)
- **fcd-v2** — FCD v2 with optional Ruflo swarm (`/fcd-v2`)
- **global-tooling** — Headroom, Ruflo, FCD router rules
- **aws-diagnose** — read-only AWS/SST diagnostics

### Not included

- **stage-mongo** — contains environment credentials; keep local only
- **Cursor marketplace plugins** — install from Cursor plugin store

## Install

```bash
git clone https://github.com/shivaplingala/cursor-toolkit.git
cd cursor-toolkit
bash install.sh          # files + host links
bash install.sh --deps   # CLIs used by skills (boto3, whisper, graphify, headroom, ruflo)
```

Then **reload Cursor**.

```bash
bash install.sh --check
```

## What `install.sh` does

1. Copies plugins into `~/.cursor/plugins/local/`
2. Copies standalone skills into `~/.cursor/skills/`
3. Copies rules into `~/.cursor/rules/`
4. Runs host-discovery scripts (FCD, FCD-V2, global-tooling → Claude/Codex/Gemini/…)
5. `--deps` installs CLIs; `--check` verifies files + those CLIs + MCP entries

## Dependencies

Skills are markdown; they **call** these tools. `bash install.sh` copies files. `bash install.sh --deps` installs CLIs + MCP stubs (does **not** overwrite existing `mcp.json` servers, so tokens stay).

| Plugin / skill | Installs / checks |
|----------------|-------------------|
| **full-cycle-delivery** | Companion skills in this repo; **graphify**; MCP **gitnexus**; **gh** |
| **fcd-v2** | **ruflo** + **headroom** CLIs and MCP |
| **global-tooling** | **headroom** (`uv tool install headroom-ai`), **ruflo** (`npm i -g ruflo`) |
| **aws-diagnose** / **agents-*** | **python3**, **boto3**, **jq**; optional **aws** CLI, **agentcore** (`pip install bedrock-agentcore-starter-toolkit`) |
| **aha-video-understanding** | **ffmpeg**, **openai-whisper**, **yt-dlp**, **tesseract**; MCP **aha-mcp** + **video-analyzer** (`npx mcp-video-analyzer`) |
| **graphify** | `uv tool install graphifyy` |
| **agentmemory-*** / remember / recall / … | MCP **agentmemory** (`npx @agentmemory/mcp`) |
| **codebase-doc-*** | **node** (bundled `.mjs` scripts) |
| **playwright-qa** | App-repo Playwright (`npm run test:e2e`), not global |
| **setup-pre-commit** | `npx husky` in the target repo |
| Prompt-only (ponytail, grill-*, tdd, review, …) | No extra CLI |

`--deps` also ensures `uv`, pip packages, npm globals, and MCP stubs. Fill `AHA_API_TOKEN` / `AHA_DOMAIN` in `aha-mcp` if those env keys are empty. Reload Cursor after.

## Owner: refresh from this machine

After editing plugins/skills locally:

```bash
bash install.sh --pack
git add -A && git commit -m "Refresh toolkit from local install"
git push
```

## License

See [LICENSE](LICENSE). Plugin-specific licenses remain in each plugin folder.
