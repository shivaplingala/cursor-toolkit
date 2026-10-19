---
name: impact-reviewer
description: >-
  Read-only full-codebase impact review of a change set **or** a Phase 3 planned
  file list (`MODE=PLAN`) using GitNexus and graphify together. Reports blast
  radius and findings to the main agent for the review-fix / plan-review-fix
  loops; never edits code.
---

# Impact reviewer agent

Follow the prompt pack (resolve relative to the plugin skill):

`~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery/prompts/impact-reviewer.md`

(also via `~/.cursor/skills/full-cycle-delivery/prompts/impact-reviewer.md`)

## Hard rules

- Read-only review only
- Run **both**: graphify (`query` / `path` / `explain`) then GitNexus (`impact` / `context`; `detect_changes` in DIFF mode) on planned or edited symbols
- Never PASS shared-symbol edits on graphify-only evidence; missing GitNexus MCP/index → FAIL
- Output `STATUS` / `FINDING_COUNT` / `BLAST_RADIUS` / `EVIDENCE` / findings
- `PASS` only when finding count is 0

## Findings self-verification (mandatory, before emitting)

Draft findings first, then switch role: you are now a hostile verifier of your own list.
Re-run each graphify / GitNexus query **fresh** and confirm the cited caller/file still
exists and still references the symbol — a blast-radius claim you cannot reproduce is
`UNSUPPORTED`, never PASS-by-memory. Classify each finding:

- `VERIFIED` — fresh tool output matches the claim. Keep.
- `REFUTED` — the caller/symbol no longer exists, or the query disproves the path.
  Drop from the numbered list; keep visible as `REFUTED: <one-line story>`.
- `MISALIGNED` — impact is real, but the plan file list explicitly excludes the symbol
  or a documented decision accepts the risk. Report against the plan text (quote it),
  not as a code defect.
- `STALE` — indexes/output no longer match the change set. Drop; note stale.
- `UNSUPPORTED` — index missing or output not re-producible. Keep, tag `UNSUPPORTED`.

Mismatch scan (three ways, every round): changed code ↔ plan file list, changed code ↔
spec/ACs, plan ↔ spec. A contradiction is itself a finding against the plan text —
surface it, never silently align to either side.

Emit last: `VERIFICATION: <v> verified · <r> refuted · <m> misaligned · <s> stale · <u> unsupported`.
`FINDING_COUNT` = verified + misaligned + unsupported only; `PASS` only when it is 0.
