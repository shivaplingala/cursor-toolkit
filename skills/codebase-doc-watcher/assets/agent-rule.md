## Codebase docs are auto-maintained

This repo keeps machine-readable code docs beside the source:
`CODEBASE_MAP.md` (navigation) and `CODE_DETAILS.md` (per-folder reference of
every function, class, interface, enum, and type under that folder's `src/`).
`.codedocs/pending.json` lists packages whose docs went stale after edits.

**Whenever you add, change, or delete code under any `src/`, refresh the docs before finishing:**

1. `node .codedocs/diff.mjs --apply` — refreshes maps and writes
   `.codedocs/plan.json` listing which `CODE_DETAILS.md` to rewrite or delete.
2. For each entry in `detailDocsToWrite`, read its `sourceFiles` and rewrite that
   `CODE_DETAILS.md` (lookup table first, then one terse block per symbol: what it
   does, when to use it, params, returns). Delete anything in `detailDocsToDelete`.
3. `node .codedocs/diff.mjs --commit` to mark the state documented.

If `.codedocs/pending.json` is non-empty at the start of a session, treat that as
a backlog and do the same refresh for the listed packages.