---
name: codebase-doc-updater
description: Refresh the codebase documentation layer (CODEBASE_MAP.md / CODE_DETAILS.md) after code changes, rewriting only what actually changed. Diffs the current TypeScript/JavaScript source against .codedocs/manifest.json, then adds/updates/removes the affected per-folder docs — keeping every function, class, interface, enum, and type description in sync so a tiny model can still navigate. Use this whenever the user has edited code and wants the docs brought up to date, says docs are stale/outdated, asks to sync or regenerate code docs after changes, or when .codedocs/pending.json lists pending packages. Trigger even if they just say "update the code docs", "my CODE_DETAILS files are out of date", or "re-sync the codebase map". Prefer this over the generator when docs already exist — it only touches what changed.
---

# Codebase doc updater

Keeps the docs written by **codebase-doc-generator** in sync with the code,
incrementally. It diffs the source tree against the recorded manifest and only
rewrites the `CODE_DETAILS.md` files whose code changed — fast and cheap, even on
a big monorepo.

Requires that the generator has already run at least once (so
`.codedocs/manifest.json` exists). If it hasn't, run the generator instead.

## Workflow

### 1. Detect and stage the changes

```bash
node <skill>/scripts/diff.mjs /path/to/repo --apply
```

This:
- prints a JSON change report (`packagesAdded`, `packagesRemoved`,
  `packagesChanged`, `navChanged`);
- refreshes every `CODEBASE_MAP.md` (so the navigation reflects added/removed
  folders);
- deletes `CODE_DETAILS.md` for removed packages;
- writes an **incremental** `.codedocs/plan.json` with `detailDocsToWrite`
  (changed/new packages, each with its `sourceFiles`) and `detailDocsToDelete`.

If `hasChanges` is `false`, the docs are already current — stop here and say so.

### 2. Rewrite the affected detail docs

Read `.codedocs/plan.json`. For each entry in `detailDocsToWrite`, read its
`sourceFiles` and rewrite that `CODE_DETAILS.md` following
**`references/detail-template.md`** (lookup table first, then one terse block per
symbol with **Does** and **Use when**). Confirm anything in `detailDocsToDelete`
is gone.

Only these files need attention — untouched packages keep their existing docs.

### 3. Commit the new documented state

```bash
node <skill>/scripts/diff.mjs /path/to/repo --commit
```

This rewrites `.codedocs/manifest.json` to match the now-current source, so the
next diff starts clean. If a `.codedocs/pending.json` queue exists (written by
the watcher or git hook), clear the entries you just handled.

## Working from the pending queue

The watcher and git hook record stale packages in `.codedocs/pending.json`
without running an LLM. When invoked to "clear the backlog", read that file, then
run the same three steps — `--apply` already recomputes the full diff, so it
naturally covers everything queued. After `--commit`, empty or prune
`pending.json`.

## Notes

- The diff is hash-based (per file), so it catches edits, additions, and
  deletions precisely, and survives moves between machines as long as
  `manifest.json` is committed.
- `--apply` does **not** rewrite the manifest — that happens only on `--commit`,
  after you've actually written the docs. This keeps re-runs idempotent if you're
  interrupted mid-update.
- Node only; no `npm install`. The script never calls an LLM — you write the prose.