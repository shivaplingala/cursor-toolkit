---
name: verify-reviews
description: Audit review reports (code review, spec review, impact review) as a third party — re-verify every reported finding freshly against the code, the plan, and the spec, re-run the impact evidence, cross-check reviewers against each other, and flag mismatches between findings, plan, and spec. Classifies each finding VERIFIED / REFUTED / MISALIGNED / STALE / UNSUPPORTED and scores reviewer accuracy. Use when review findings must be cross-audited before acting on them, when reviewers disagree, or when a fix loop keeps circling the same finding.
---

# Verify reviews

Third-party audit of one or more review reports. The reviewers already ran a
self-verification pass; this skill is the **outside check on that pass** — the audit
of the audit. Its job is to catch mismatch in every direction:

- findings that don't reproduce against the code (`REFUTED`)
- findings true in code but contradicted by the plan or spec (`MISALIGNED`)
- findings whose evidence expired (`STALE`)
- blast-radius or caller claims the tools no longer reproduce (`UNSUPPORTED`)
- reviewer-vs-reviewer contradictions and plan-vs-spec contradictions — findings in
  their own right

## Inputs

Collect before auditing (ask the parent for anything missing, once):

1. The review report(s): code review, spec review, impact review — including each
   report's `VERIFICATION:` line and `FINDING_COUNT`.
2. The plan (task list, acceptance criteria, progress status).
3. The spec / ACs / ADR text the work claims to implement.
4. The diff or changed files — or `BASE_SHA..HEAD_SHA`.
5. Work type / playbook path (for the review-matrix rows, where applicable).

If no report exists yet, stop and tell the parent to run the reviews first — this skill
audits reports, it does not replace them.

## Process

### 1. Extract the claims

For each report, list its findings as `report · #n · claimed verdict · cited evidence
(file:line / symbol / tool output)`. Parse the `VERIFICATION:` summary line and record
each reviewer's claimed split (verified / refuted / misaligned / stale / unsupported) so
the audit can score it against reality at the end.

### 2. Re-verify each finding fresh

You are a hostile third party. Never reuse the reviewer's own quote as evidence —
re-open the cited `file:line` yourself, re-read the plan task line / AC / spec sentence
the finding maps to, and re-run the one query or command that would disprove it
(`git diff`, graphify/GitNexus for impact claims, the verify script for build claims).
Classify each finding with the same scheme the reviewers use:

- `VERIFIED` — reproduces against a fresh read. Keep.
- `REFUTED` — the reviewer's second look was wrong too (misread, already handled,
  wrong line). The finding is dead; say why in one line.
- `MISALIGNED` — true about the code, but the plan/spec explicitly requires or defers
  it. The defect is in the plan text, not the code — quote the plan/spec line.
- `STALE` — code/plan/spec moved since the report. Say what moved.
- `UNSUPPORTED` — the audit cannot reproduce the evidence either (moved lines, missing
  tool output). Neither side wins; needs a live re-check.

### 3. Cross-checks (the mismatch matrix)

Run all four rows — mismatches are the point of this skill:

| Row | What you compare | A hit means |
| --- | --- | --- |
| reviewer ↔ code | finding vs the file at the cited lines | `REFUTED` / `UNSUPPORTED` |
| reviewer ↔ plan | finding vs the mapped plan task + ACs | `MISALIGNED` (plan made the call) |
| reviewer ↔ reviewer | claims about the same symbol/line across reports | report the contradiction, cite both reports |
| plan ↔ spec | task text vs spec/AC text | contradiction finding against the plan text — quote both |

### 4. Verdict and accuracy

Output, in this order:

1. `AUDIT: ACCEPT | DISPUTED | UNRELIABLE` —
   `ACCEPT` = every re-checked finding reproduces; `DISPUTED` = ≥1 finding changes
   verdict; `UNRELIABLE` = a report's `VERIFICATION:` line materially miscounts its own
   findings.
2. Mismatch matrix — one row per finding:
   `report · #n · review claim → audit verdict · one-line evidence`.
3. `REVIEWER ACCURACY: <report> verified/re-verified · ...` per report.
4. Contradictions section (reviewer↔reviewer, plan↔spec) — never silently aligned to
   either side; parent resolves.
5. Final line: `VERIFICATION: <v> verified · <r> refuted · <m> misaligned · <s> stale · <u> unsupported — audited <n> findings across <reports> report(s)`.

Self-audit rule: this skill's own audit claims live under the same standard — before
emitting, re-open each source once more and apply the same five verdicts to the audit
itself. An audit finding you cannot re-reproduce is `UNSUPPORTED`, not an accusation.
