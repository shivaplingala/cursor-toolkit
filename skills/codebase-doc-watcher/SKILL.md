---
name: codebase-doc-watcher
description: Set up automatic re-running of the codebase doc updater whenever files change — on every add/edit/delete and/or on git commit. Installs a zero-dependency Node file watcher, a git hook, and agent-rule files (.cursor/rules, CLAUDE.md, AGENTS.md) so Cursor, Claude Code, and Codex all refresh stale CODE_DETAILS.md / CODEBASE_MAP.md docs automatically. Use this whenever the user wants the codebase docs to stay current on their own, asks to auto-update or watch the repo for changes, wants a pre/post-commit hook for docs, or wants docs regenerated continuously without manual runs. Trigger even if they just say "keep the docs updated automatically", "watch my repo", or "run the updater on every change". Set up the generator + updater first if they aren't in place.
---

# Codebase doc watcher

Makes the documentation layer self-maintaining. It detects every file
add/change/delete and keeps `.codedocs/pending.json` (the queue of stale
packages) current — with **zero dependencies** and no LLM needed for detection.

The honest constraint worth stating to the user: **rewriting a `CODE_DETAILS.md`
needs an LLM to read code, so a watcher alone can't do it.** This skill therefore
splits the job in two:

1. **Detection (always automatic, no agent):** a Node watcher + git hook record
   what changed into `.codedocs/pending.json`.
2. **Rewrite:** runs either immediately (if an agent command is configured) or at
   the next agent session — the installed rule files tell Cursor / Claude /
   Codex to run the **codebase-doc-updater** when the queue is non-empty.

## Prerequisite

The generator and updater must already be set up (so `.codedocs/manifest.json`
exists). If not, run **codebase-doc-generator** first.

## Setup

Run the installer from the repo root:

```bash
node <skill>/scripts/install.mjs /path/to/repo [--hook=post-commit|pre-commit] [--no-agent-rules]
```

It copies the runtime into `<repo>/.codedocs/` (`core.mjs`, `diff.mjs`,
`watch.mjs`) so everything works without the skill bundle present, then installs:

- a git hook (`post-commit` by default) running `node .codedocs/diff.mjs --pending`;
- `.cursor/rules/codebase-docs.mdc`, plus managed blocks appended to `CLAUDE.md`
  and `AGENTS.md`, instructing whichever agent is active to refresh queued docs;
- `.gitignore` entries for `pending.json`;
- `.codedocs/watch.config.json` for the live watcher.

Tell the user to commit `.codedocs/{core,diff,watch}.mjs` and the rule files so
teammates and CI get the same behaviour.

## The two triggers (user picked "both, choose later")

**Git hook** — fires on commit, queues whatever the commit changed. Good baseline;
always on once installed. Use `--hook=pre-commit` to queue before the commit is
recorded, or the default `post-commit` to stay non-blocking.

**Live watcher** — catches changes the moment they're saved, not just at commit:

```bash
node .codedocs/watch.mjs /path/to/repo
```

It debounces bursts, updates `pending.json`, and prints what went stale. To make
it rewrite docs unattended, set `agentCommand` in `.codedocs/watch.config.json`,
e.g. for Claude Code:

```json
{ "debounceMs": 800, "agentCommand": "claude -p 'Run the codebase-doc-updater skill to clear .codedocs/pending.json'" }
```

Leave `agentCommand` as `null` (the default) if no headless CLI is available —
detection still works, and the agent-rule files handle the rewrite next session.

## Help the user choose

- Want it hands-off and you have a CLI agent (e.g. Claude Code): live watcher +
  `agentCommand` → docs refresh seconds after you save.
- No reliable headless CLI (typical Cursor-only setup): keep `agentCommand` null;
  the git hook + rule files mean docs refresh whenever an agent next works in the
  repo. Recommend this as the safe default for a mixed Cursor/Claude/Codex team.
- You can run both triggers at once; they share the same `pending.json`.

## How a rewrite actually happens

When an agent (or `agentCommand`) runs the updater, it executes
`node .codedocs/diff.mjs --apply`, rewrites the `CODE_DETAILS.md` files named in
`.codedocs/plan.json`, then `node .codedocs/diff.mjs --commit` and clears the
queue. That logic lives in the **codebase-doc-updater** skill and in the rule
files this installer drops.

## Notes

- The watcher watches recursively without relying on platform-specific recursive
  `fs.watch`, so it works on Linux/macOS/Windows. Node only; no installs.
- Re-running the installer is safe — it won't duplicate hook lines or rule blocks
  (they're marked and replaced in place).