---
name: codebase-doc-generator
description: Generate a complete, navigable documentation layer for a TypeScript/JavaScript codebase (especially monorepos with apps/, packages/, connectors/). Writes a CODEBASE_MAP.md navigation index at the repo root and at every nesting level, and a detailed CODE_DETAILS.md in every folder that contains a src/ — documenting every function, class, interface, enum, and type so even a tiny model can find what it needs without reasoning. Use this whenever the user wants to document, map, index, or "explain" a codebase, make a repo AI-friendly or LLM-readable, create per-folder code reference docs, onboard a model/teammate to a repo's structure, or bootstrap docs before setting up auto-updating. Trigger even if they just say "document my repo", "map the codebase", or "add code explanation files" without naming this skill.
---

# Codebase doc generator

Builds a two-tier documentation layer over a TS/JS codebase:

- **`CODEBASE_MAP.md`** — a navigation index at the repo root and at each folder
  that has sub-folders of code. It says, in a table, which child folder holds
  what and where to look next. Pure structure.
- **`CODE_DETAILS.md`** — in every folder that directly contains a `src/`, a
  detailed reference of every symbol under that `src/`: functions, classes,
  interfaces, enums, types — written for a small model to grep, not reason.

A bundled Node script does the deterministic work (scanning, writing the maps,
hashing files for change detection). **You** write the detail docs, because the
valuable part — "what does this do and when would I use it" — requires reading
the code, not just parsing signatures.

## Workflow

### 1. Run the scaffold script

From the repo root (pass the path if running elsewhere):

```bash
node <skill>/scripts/generate.mjs /path/to/repo
```

This walks the tree (ignoring `node_modules`, `dist`, build output, etc.),
writes every `CODEBASE_MAP.md`, writes `.codedocs/manifest.json` (content
hashes), and writes `.codedocs/plan.json`. It prints a summary like
`{ packages, navMapsWritten, detailDocsToWrite }`. The maps and manifest are now
done — only the detail docs remain.

### 2. Write each CODE_DETAILS.md

Read `.codedocs/plan.json`. Its `detailDocsToWrite` array lists, per package, the
`detailDoc` path to create and the `sourceFiles` to read. For each entry:

1. Read every file in `sourceFiles`.
2. Write the `detailDoc` following **`references/detail-template.md`** exactly —
   a "Quick lookup" table first, then one terse block per symbol with a **Does**
   and a **Use when** line. Read that template now if you haven't; the lookup-table-first
   shape is what makes the docs usable by a tiny model.

Work through packages in order. For a large repo, batch the file reads per
package rather than reading everything up front.

### 3. Mark the state as documented

Once all detail docs are written:

```bash
node <skill>/scripts/generate.mjs /path/to/repo   # (already current — manifest written in step 1)
```

The manifest from step 1 already reflects the documented state, so nothing more
is needed here unless source changed while you worked. If it did, just re-run the
script and update the affected docs.

### 4. Offer the follow-ups

Mention that the user can keep these docs current automatically with the
**codebase-doc-updater** skill (refresh after edits) and the
**codebase-doc-watcher** skill (run the updater on every file change / commit).

## What counts as a "package"

Any folder that directly contains a `src/` sub-folder. That folder gets a
`CODE_DETAILS.md`; the script never recurses past `src/` for navigation — `src/`
contents are documented in the detail file, not mapped. Folders with only
sub-packages (no `src/` of their own) get a `CODEBASE_MAP.md` only.

## Conventions

- Doc files: `CODEBASE_MAP.md` (navigation), `CODE_DETAILS.md` (per-package detail).
- State lives in `.codedocs/` (`manifest.json`, `plan.json`). Commit
  `manifest.json` so change detection works across machines.
- Default code extensions: `.ts .tsx .js .jsx .mjs .cjs .mts .cts`; `.d.ts`,
  test/spec files, and minified files are skipped. To support other languages,
  extend `CODE_EXT` in `scripts/core.mjs`.

## Notes

- The script is idempotent — safe to re-run; it rewrites maps and the manifest.
- It needs only Node (no `npm install`). It does not call any LLM itself.
- Don't hand-edit the structural tables in `CODEBASE_MAP.md`; re-run the script
  or use the updater instead.