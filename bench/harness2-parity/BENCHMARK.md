# harness2-parity benchmark — OpenCode + cursor-toolkit vs Harness²

Audited **2026-10-18** (read-only). Framework reference: `~/harness2` (Google Research,
[Harness² — Recursive Agent Harnessing for an Open World](https://arxiv.org/abs/2610.14224)).
Code anchors verified locally: `harness2/substrate/opencode.py` (`OPENCODE_SURFACE`),
`harness2/core/tree.py` (`validate`, `autotrigger`), `harness2/core/prompts.py`
(surface/levers prose), `harness2/core/library.py` (EXPERIENCE.md lesson library).

Paper evidence cited as **(paper)**: 8 components c1–c8; one Propose–Probe–Compose
step yields **+4 to +12 pts** on WorkBuddy-Bench/JobBench/LAB; k=5 recursion adds
**+2.9–6.7** more; **tool-error rate falls 20–37%**; adopted edits are **~50% skills +
scripts**; ablations when removing a component group: prompt-group **−1.5**, skills
**−5.3**, scripts **−3.7**, lesson library **−3.1**; case-study fixes: pseudo tool
calls → tool-guidance edit (**60→100**), no verification/reopen → process guardrail +
check script (**43→78**), budget overrun without artifact → middleware plugin appending
WARN after N calls (**72→100**), stale state → skill re-derived state + offline
artifact check script (**64→100**); skill auto-load trigger lines; failure classes —
selection can pick a worse candidate, wrong premises propagate.

Scoring: `checks/c1…c8_*.py` (deterministic, no model calls). Per check,
`pass = score ≥ 0.5`; ties map to the audit narrative below.

---

## 1. Component table

| c-# | Harness² lever (paper evidence) | Current state in our assets | Severity | Expected impact |
|---|---|---|---|---|
| c1 systemprompt | Always-on surface `systemprompt.md` capped **24 000 chars** (`opencode.py:50`); trigger/invariant structure lives here | Root always-on prompt = `~/.config/opencode/opencode.json:5` → `{file:/home/shiva/applaud/opencode-prompt-compact/all-models.txt}` (4 007 chars — 17% of cap), generic persona, **zero skill-trigger lines, zero invariant/budget wording**; 25 agent bodies 1.2–3.9k chars, all under cap | MED | Prompt-group ablation **−1.5 (paper)** but budget headroom is the thing we have; adding trigger lines costs ~0.5k chars of the 20k unused |
| c2 guardrails | `guardrails.md` ALWAYS ON; harness2 "verify before finishing … a successful write call does not establish usability" (`prompts.py:364-365`) | **68 static permission gates** (deny=59, ask=9) in agent frontmatter — real structural gates, e.g. `agents/fcd/orchestrator.md:24-28,31` (git push/commit/gh pr ask), `agents/fcd/knowledge-capture.md` (git push/commit **deny**); 9 verify-before-dispatch style occurrences (e.g. `agents/applaud/orchestrator.md:4`, `~/.cursor/skills/applaud-debug/SKILL.md:24-31`); **no centralized always-on guardrails file** (`~/.config/opencode/guardrails.md` missing), **no documented precedence/last-match-wins** (grep: 0) | MED | Case study **43→78** when a verify guardrail + check script is added; we have the prose side but nothing always-on centralizes it |
| c3 memory | Per-domain lesson library: `EXPERIENCE.md` — cue / lesson / evidence / confidence, dated, with INDEX and read-before-use ordering (`library.py:131-150`, `prompts.py:1133-1147`) | FCD knowledge corpus is a **real lesson library** (better than suspected): `~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery/knowledge/` — INDEX + 6 topic files + `log.md` with 6 dated entries (`log.md:1,11`), 40-bullet cap, capture agent wired (`agents/fcd/knowledge-capture.md`, edit-allow on corpus only). Gaps: **not always-on**, read-direction only via skill, **0 agent bodies** reference agentmemory/mem0/mempalace despite MCPs configured in `opencode.json:43-115`; no cue/lesson/evidence field discipline; no domain-scoped retrieval order | MED | Lesson-library ablation **−3.1 (paper)**; "wrong premises propagate" failure class is guarded by evidence-rows + re-verification, which dated entries partially do |
| c4 tool guidance | `tool_descriptions/tool_guidance.md` ALWAYS ON; single centralized tool-prose surface | Loopback QA rule: **30 occurrences of 127.0.0.1:8080, 0 value conflicts** — but duplicated across **12 files** (e.g. `fcd-v2/SKILL.md:139`, `playwright-qa/SKILL.md:13`, `qa/SKILL.md:20`, `agents/fcd/qa-engineer.md:43`); lsp fallback guidance only inside applaude-debug findings; sst-stage guidance in 5+ skills; **no `tool_guidance.md` anywhere under `~/.config/opencode`** | MED | Case study **60→100** for a tool-guidance edit; tool-error rate **−20–37% (paper)**; centralization removes 11 redundant copies |
| c5 subagents | `sub_agents/<n>/AGENT.md`, `mode: subagent` + `description:` required, own separate context, "bounded sub-task: large input, small answer" | **25 agents** (3 root trio + 16 fcd + 6 applaud), **16 mode:subagent / 9 mode:all** (0.64); both orchestrators declare thin/delegation posture (`fcd/orchestrator.md`, `applaud/orchestrator.md:5`); 8 reviewer-named agents deny edit; 9/16 subagent briefs carry canonical-prompt/input markers | LOW | Subagent share 0.64 already exceeds the ratio harness2 sees in adopted harnesses; keep — invest here last |
| c6 skills | `skills/<n>/SKILL.md`: `name` must equal dir (mismatch **dropped silently**, `tree.py:267-297`); description required; **"EVERY SKILL NEEDS A TRIGGER LINE — the most violated rule here"** (`prompts.py:151`); auto-trigger repair (`tree.py:192`) | 239 SKILL.md (≈80 unique names × 3 mirrors); descriptions all present & unique per name; **1 name≠dir**: `aws-diagnose-read/SKILL.md:2` (`name: aws-readonly-diagnostics`); **0 canonical trigger lines** in agents/rules; only 2 loose refs (`agents/fcd/implementer.md:25`, `agents/fcd/frontend-implementer.md:26` — ponytail); skills are discovered by rules/plugins, not by always-on advertisement | **HIGH** | Skills ablation is the largest: **−5.3 (paper)**; untriggered skills are dead weight by harness2's own rule; auto-trigger lines are a case study of the paper |
| c7 scripts | `scripts/*.py` deterministic helpers; validation fails a proposal if a named script doesn't ship (`tree.py:317-333`); py_compile check; skills must carry their helpers | **54 helper scripts shipped** (skills/*/scripts/* + plugin scripts), **22 .py compile clean**, 22/32 .sh executable; 13 script refs in prompt text resolve (e.g. `stage_logs.sh` ← `applaud-debug/SKILL.md:24`, `fcd-doctor.sh` ← `fcd-v2/SKILL.md:81`); **gap: still prose placeholders** (`REPO/scripts/verify-scope.sh`) and no skill pairs its procedure with an offline deterministic artifact-check script the paper's case studies rely on | MED | Scripts ablation **−3.7 (paper)**; case studies **43→78** and **64→100** both pair guardrails/skills with shipped check scripts |
| c8 plugins | `plugin/<name>.ts` — ALWAYS registered, acts INSIDE the tool loop: "the only lever that can enforce something the model cannot skip" (`prompts.py:122-124, 443-450`); shapes: append WARN after N calls, verify a write immediately, hint after recurring error signature, capping runaway tools | **ZERO**: no `~/.config/opencode/plugin/` dir, no `plugin` key in `opencode.json`, **no .ts anywhere** in config or toolkit; the only tool-level enforcement is static permissions (the 68 gates above) — deny/ask cannot append targeted hints, verify written artifacts, or cap loops | **HIGH** | Case study **72→100** (budget-overrun WARN middleware); enforcement is prompt-independent and costs **zero** always-on budget |

---

## 2. Top 6 ranked improvement areas (by expected impact / cost)

Ordered. Each row: lever → apply where → validation via the suite → paper mirror.

1. **Skill trigger lines in the always-on prompt** (c6, feeds c1).
   *Apply:* append ~8–12 canonical lines to `~/.config/opencode/rules/*.md` — the
   auto-applied always-on rules surface — in harness2's exact format
   (`When <situation>, load the `<name>` skill.`, `tree.py:60`) for the highest-traffic
   skills (full-cycle-delivery, research-agent, grill-me, backend, frontend, qa,
   playwright-qa, applaud-debug, ruffless-debug triads…). Total ≤ 2k chars, ~5% of cap.
   *Validate:* `c6-skills` canonical trigger count 0 → ≥ 8; score 0.5 → ≥ 0.75.
   *Paper mirror:* skills ablation **−5.3** (largest) + the auto-load trigger-line case
   study.

2. **Middleware plugin as the enforcement lever** (c8).
   *Apply:* create `~/.config/opencode/plugin/*.ts` exporting a `Plugin` (per
   `prompts.py:443-450`): `tool.execute.after` handler that (a) appends a targeted
   WARN to the agent once N tool calls pass without a completed deliverable (the
   **72→100** case study), (b) re-reads a just-written artifact and checks it
   parses/holds required fields, (c) appends a hint after a recurring error signature.
   Optionally register it in `opencode.json` for discoverability.
   *Validate:* `c8-plugin` 0.25 → ≥ 0.75 (plugin dir + config key present).
   *Paper mirror:* **72→100**; "verify a write immediately after it happens" recurring
   shape.

3. **Centralize tool guidance into one always-on file** (c4).
   *Apply:* create `~/.config/opencode/tool_guidance.md` (or a dedicated rule file)
   carrying the loopback QA base (`127.0.0.1:8080`), sst stage env usage (`sst
   <env> --stage` / `lsp` stage `dev-lshiva`), lsp-first-then-fallback reading order,
   and headroom proxy rule; then reduce the 12 duplicate in-skill copies to "see
   tool_guidance.md". Convert 9 verify-order prose mentions into the same file's
   verification section (feeds c2).
   *Validate:* `c4-tool-guidance` dedicated-file subcondition → 1.0; duplication count
   12 → ≤ 3.
   *Paper mirror:* pseudo-tool-calls → tool-guidance edit **60→100**; tool-error rate
   **−20–37%**.

4. **Pair process guardrails with shipped check scripts** (c7 + c2).
   *Apply:* add a deterministic verify script (e.g.
   `skills/full-cycle-delivery/scripts/verify_deliverable.py` — parse artifact,
   validate required sections, emit PASS/FAIL list) and reference it from the FCD
   orchestrator/approver guardrails ("run before dispatch to plan approval"), mirroring
   harness2's rule that "a successful write does not establish usability". Replace the
   `REPO/scripts/verify-scope.sh` prose placeholder with the shipped script.
   *Validate:* `c7-scripts` unresolved-ref count → 0 concrete dangling; `c2-guardrails`
   verify-rule occurrences 9 → +3 (centralized).
   *Paper mirror:* **43→78** (no-verification → process guardrail + check script).

5. **Upgrade the lesson library to cue/lesson/evidence discipline + wire it into
   agents** (c3).
   *Apply:* in the FCD knowledge corpus, add the four-field structure behind each dated
   entry (`cue`: situation shape; `lesson`: operation naming the component;
   `evidence`: dated log row; `confidence`) — harness2's `EXPERIENCE.md` schema
   (`library.py:131-150`) — add an INDEX `cue:` column, and reference the corpus +
   `agentmemory` recall from `fcd/orchestrator.md` and `knowledge-capture.md`
   (currently 0 agent bodies mention memory MCPs though they are configured).
   *Validate:* `c3-memory` memory-MCP-in-agents count 0 → ≥ 2; dated entries stay
   ≥ 3; corpus restructure → score 0.75 → 1.0.
   *Paper mirror:* lesson-library ablation **−3.1**; "wrong premises propagate"
   failure class — evidence rows + re-verification are the designed counter.

6. **Skill-name hygiene + cap policy note** (c6, closes the audit).
   *Apply:* align `aws-diagnose-read/SKILL.md:2` frontmatter (`name:` → directory name,
   or drop the `name:` line; harness2 warns a mismatch is "dropped SILENTLY at load"
   and silently kills every trigger naming the directory) in all three mirrors; add a
   documented always-on budget policy (24k cap + "if you add, cut") in the same
   centralized guardrails/tool-guidance file from areas 2–3.
   *Validate:* `c6-skills` name≠dir list → none; `c1-systemprompt` invariant/budget
   wording → ≥ 1.
   *Paper mirror:* load-drop invariant (`tree.py:278-291`); prompt-group cost model.

---

## 3. Baseline snapshot (pre-application)

Recorded from `bench-results-20261018.json` — `run_ts 2026-10-18T20:23:47Z`, 8 checks
(one per component), **7 passed / 1 failed / 0 skipped**, **TOTAL_SCORE 0.703**.
Runner exits 0 always; a failing check is data.

| c-# | check | pass | score | headline evidence |
|---|---|---|---|---|
| c1 | c1-systemprompt | ✔ | 1.000 | root prompt 4 007 chars ≤ 24 000; 25 agent bodies all ≤ 24 000; 0 canonical trigger lines, 2 loose refs, 0 invariant/budget wording |
| c2 | c2-guardrails | ✔ | 0.750 | git push/commit deny gates in 13 agents, ask in 3; 68 static gates; 9 verify-rule occurrences; **no centralized guardrails.md**; 0 precedence wording |
| c3 | c3-memory | ✔ | 0.750 | corpus INDEX + 6 topics; 6 dated entries; 2 agents integrate corpus; **0 always-on lesson file, 0 memory-MCP mentions in agents** |
| c4 | c4-tool-guidance | ✔ | 0.750 | loopback 30× (0 conflicts); lsp 29×; sst 72×; **no dedicated tool_guidance.md; rule duplicated across 12 files** |
| c5 | c5-subagents | ✔ | 0.891 | 25 agents, 16 mode:subagent (0.64); 2/2 orchestrators thin-posture; 8 reviewers fenced; 9/16 briefs self-contained |
| c6 | c6-skills | ✔ | 0.500 | 239 SKILL.md; description coverage 100%, unique; **1 name≠dir; 0 canonical trigger lines, 0 loose mentions in rules (2 in agents)** |
| c7 | c7-scripts | ✔ | 0.734 | 54 scripts shipped; 13 refs resolve (4 prose placeholders); 22 .py compile; 22/32 .sh executable |
| c8 | c8-plugin | ✘ | 0.250 | **no plugin dir / config key / .ts anywhere**; static permission gates are the only tool-level enforcement |

Deterministic: a same-day re-run produced zero per-check delta (verified with
`compare.py`).

### Expected post-application deltas (if the top-6 land)

| area | check movement |
|---|---|
| 1 triggers | c6 0.500 → ≥ 0.750 |
| 2 plugin | c8 0.250 → ≥ 0.750 |
| 3 tool guidance | c4 0.750 → 1.000 |
| 4 verify script | c7 0.734 → ≥ 0.900 |
| 5 lesson library | c3 0.750 → 1.000 |
| 6 hygiene | c6 → ≥ 0.875 (name fixed) |

All movements are deterministic file/regex outcomes — no model calls are needed to
confirm them, which is exactly what makes this suite repeatable after each
harness2-style improvement PR.

---

## Post-application (2026-10-18, applied after this audit)

Applied, in ranked order: (1) native `skill` trigger lines + tool guidance + guardrails +
memory beats in a new global always-on surface `~/.config/opencode/AGENTS.md` (mirrored at
`~/cursor-toolkit/opencode/AGENTS.md`); (2) `~/.config/opencode/plugins/budget-guard.js` —
`tool.execute.after` middleware (WARN after 15 calls with no write, overall-call cap, repeated
error-signature hint); (3) `instructions` in `opencode.json` wired so `~/.config/opencode/rules/*.md`
actually load (they were dead files); (4) `aws-diagnose-read` name==dir fix in all skill mirrors;
(5) `~/cursor-toolkit/scripts/artifact-check.py` paired verification script, referenced from always-on.

**Delta vs baseline (results/bench-results-20261018.json → -6.json): TOTAL 0.703 → 0.955 (+0.252), 8/8 pass.**
c1 1.00 (+0.00) · c2 1.00 (+0.25) · c3 1.00 (+0.25) · c4 1.00 (+0.25) · c5 0.891 (+0.00) ·
c6 0.875 (+0.375) · c7 0.875 (+0.14) · c8 1.00 (+0.75, NOW-PASS). NEW-FAIL: none.

Check-surface note: v1 checks probed harness2's fictional `plugin/`-dir surface; checks now
target OpenCode's real conventions (global AGENTS.md, `plugins/` dir, `instructions` key,
`name==dir` across all 5 skill roots). Baseline intentionally unchanged; deltas compare
old-check-B vs new-check-B because the v1 checks could not observe the new surfaces at all.

---

## Baseline 2026-10-22 — V2-surface-corrected checks (10 checks)

Run after the OpenCode V2 port (`e2369ee` agents → `mode: all`; `f4ef9d2` plugins →
`ctx.tool.hook("execute.after")`). The 10-18 checks graded a **V1** surface, so real
capability scored as missing: `c5` counted only literal `mode: subagent` (0 of 26 after
the port) and `c8` grepped for `tool.execute.after` (the V1 hook string). That produced a
misleading 0.891 total with two false regressions.

### Check changes

| check | change |
|---|---|
| c1 | budget now measures the **total** always-on payload (global AGENTS.md + live `rules/*.md`) instead of one file: 4 436 → **8 973** of 24 000 (37%) |
| c5 | `mode: all` counts as delegable (V2: primary **or** subagent); brief self-containment measured across the whole delegable fleet (14/26); **new** sub-condition: reviewer agents that are `mode: all` are selectable as the main session agent |
| c6 | trigger-line count reads live rules only — the toolkit `rules/*.mdc` mirror is a Cursor surface and would double-count |
| c8 | accepts V1 `tool.execute.*` **and** V2 `ctx.tool.hook("execute.*")`; **new** sub-condition: the plugin must expose the loadable V2 shape (default export + `setup()`) |
| c9 | **new** — toolkit source vs live install: AGENTS.md mirror, plugin files present, plugin content, rule coverage, skill mirror |
| c10 | **new** — the opencode server log must show each installed plugin actually loading, with no load errors |

### Result (`results/bench-results-20261022-5.json`; re-run `-6` identical, `compare.py` delta 0.000)

| c-# | check | pass | score | headline evidence |
|---|---|---|---|---|
| c1 | c1-systemprompt | ✔ | 1.000 | always-on payload 8 973 / 24 000 chars (7 files) |
| c2 | c2-guardrails | ✔ | 1.000 | deny=61 ask=9 static gates; centralized guardrails section |
| c3 | c3-memory | ✔ | 1.000 | corpus INDEX + evidence schema; 4 agentmemory/recall mentions |
| c4 | c4-tool-guidance | ✔ | 1.000 | centralized tool guidance; 2 leftover duplicate loopback files |
| c5 | c5-subagents | ✔ | 0.708 | 26/26 delegable; 14/26 self-contained briefs; **8 reviewers selectable as primary** |
| c6 | c6-skills | ✔ | 0.875 | 13 canonical trigger lines; 0 name≠dir; 91 unique skills |
| c7 | c7-scripts | ✔ | 0.875 | artifact-check.py shipped, executable, runs on itself |
| c8 | c8-plugin | ✔ | 1.000 | V2 hook detected; loadable shape; 70 static gates |
| c9 | c9-install-parity | ✔ | 0.800 | **`graphify.js` in toolkit, not installed live**; **`aha-video-understanding` missing from the opencode skills mirror** |
| c10 | c10-runtime-load | ✔ | 1.000 | budget-guard.js seen loading; 0 load errors |

10/10 pass. **TOTAL_SCORE 0.926 over 10 checks — not comparable to the 0.703 / 0.955
baselines, which averaged 8.** Compare per check, not the total.

### Real findings this baseline exposed (findings, not score regressions)

1. `opencode/plugins/graphify.js` exists in the toolkit but was never copied to
   `~/.config/opencode/plugins/` → the graphify hook never loaded. `install.sh` copies
   that tree but was not re-run after `f4ef9d2`, and its verify step asserted only
   `budget-guard.js` (`install.sh:129`).
2. 8 reviewer agents were `mode: all` → each could be selected as the main session
   agent rather than only as a child. Reviewers belong in `mode: subagent`.
3. 12 of 26 agent briefs carry no self-containment marker (canonical prompt / inputs).

Finding 2 from the first draft of this section was **wrong and is retracted**: it
claimed `aha-video-understanding` was unavailable to OpenCode because it is missing
from `~/.config/opencode/skills/`. OpenCode V2 also discovers `~/.claude/skills` and
`~/.agents/skills` (global compatibility roots), where the skill is present — so it was
loadable all along. `c9` now checks the discovery roots, not one mirror.

---

## Baseline 2026-10-22 (post-fix) — 10 checks, TOTAL 0.966

Actions taken after the corrected baseline above, all verified by re-running the suite
(`results/bench-results-20261022-8.json`):

| action | effect |
|---|---|
| toolkit repo refreshed from the live owner (FCD knowledge corpus was stale: 13 vs 44 lines — a plain install would have truncated it) | no content rolled back |
| `bash install.sh` run → `opencode/plugins/graphify.js` installed live | c9 0.800 → 1.000, c10 sees 2/2 plugins loading |
| 9 reviewer-class agents → `mode: subagent` (toolkit source + live) | c5 0.708 → 0.908; 0 reviewers selectable as primary |
| `agents/opencode/README.md` moved to `agents/README.md` | a doc file can no longer land in the installed agents dir as a bogus agent |
| `install.sh --check` now asserts **every** `opencode/plugins/*` file, not just `budget-guard.js` | verified: removing `graphify.js` makes `--check` fail |
| `c9` skill parity re-aimed at the OpenCode discovery roots | false "unavailable" finding retracted |

| c-# | check | score | headline evidence |
|---|---|---|---|
| c5 | c5-subagents | 0.908 | 26/26 delegable (subagent=9, all=17); 0 reviewers selectable as primary; 14/26 self-contained briefs (remaining gap) |
| c9 | c9-install-parity | 1.000 | AGENTS.md mirror identical; 2/2 plugins installed + identical; 6/6 rules; 66/66 skills discoverable |
| c10 | c10-runtime-load | 1.000 | both plugins seen loading in the server log; 0 load errors |

TOTAL_SCORE 0.966 over 10 checks (baseline before the fixes: 0.926; first 8-check
baselines 0.703 / 0.955 — not comparable, different check count).

---

## Baseline 2026-10-22 (final) — 10 checks, TOTAL 1.000

Every tier closed. `results/bench-results-20261022-12.json` (re-run identical).

### Subagent layer (the main focus)

| change | evidence |
|---|---|
| mode policy: **8 `all` / 18 `subagent`** — `all` reserved for the coordinators (2 orchestrators, 3 loop owners, knowledge-capture, architect pair); every worker and reviewer is dispatched-only | c5 `delegable(subagent\|all)=26`, `reviewer agents selectable as primary: 0` |
| all **26 briefs** now carry a canonical prompt/skill line **and** an `## Inputs the parent provides` section (12 briefs were missing both) | c5 `delegable briefs self-contained: 26/26` → c5 **1.000** |
| reviewers (`*-reviewer`, `reviews-verifier`, root `spec`/`impact`/`code-reviewer`) are no longer selectable as the main session agent | c5 sub-condition added in this baseline |

### Remaining tiers

| tier | change | evidence |
| ---- | ------ | -------- |
| always-on | +10 canonical skill trigger lines (gitnexus, staff-engineering, headroom, ruflo, aha-crud, aha-video-understanding, opencode, handoff/recap/session-history, to-issues/to-prd, write-a-skill) and a **Harness gate** section | c6 trigger lines 13 → **20**; always-on payload 8 973 → **10 689** of 24 000 (45%) |
| enforcement | `scripts/bench-verify.sh` (gate) + `scripts/bench-gate.py` (single decision point: **every check must score exactly 1.0**, `BENCH_THRESHOLD` default 0.90 is only a floor on the average — an average threshold alone could hide a half-broken check inside a green mean, demonstrated by the gate simulation where c1=0.667 with the payload 16k over the cap still produced total 0.967 and a green exit) + `install.sh` installs a **pre-commit hook** that blocks a commit staging `agents/`, `rules/`, `opencode/`, `skills/`, `scripts/`, `install.sh`, `bench/` while the gate is red + `opencode/plugins/bench-guard.js` (always-on nudge when a check is below 1.0, the run is red, or >24h old) | gate verified red (exit 1) and green (exit 0); strict rule re-verified by the mutation test (each mutation must turn the gate red, not just dents a score); plugin verified to emit nothing when green; c10 `3/3` plugins loading, 0 errors |
| bench metrics | c6 uniqueness now measured **per skill name across mirrors** (was a ratio of unique pairs over mirrored files → 91/384 = 0.24 against a 0.9 threshold, a denominator bug that scored real consistency as broken); c7 always-on script references counted as **distinct script names** (was lines, so two names on one line counted once) | c6 **1.000**, c7 **1.000** |

### Result

| c-# | check | score | headline evidence |
|---|---|---|---|
| c1 | c1-systemprompt | 1.000 | always-on payload 10 689 / 24 000 chars (7 files); instructions wired |
| c2 | c2-guardrails | 1.000 | deny=61 ask=9 static gates; centralized guardrails section |
| c3 | c3-memory | 1.000 | corpus INDEX + evidence schema; agentmemory/recall reachable |
| c4 | c4-tool-guidance | 1.000 | centralized tool guidance; 2 leftover duplicate loopback files |
| c5 | c5-subagents | 1.000 | 26/26 delegable (subagent=18, all=8); 0 reviewers selectable as primary; 26/26 self-contained briefs |
| c6 | c6-skills | 1.000 | 20 trigger lines; 0 name≠dir; descriptions consistent across all mirrors |
| c7 | c7-scripts | 1.000 | artifact-check.py shipped + runs on itself; 5 distinct scripts referenced from always-on |
| c8 | c8-plugin | 1.000 | V2 hooks detected on all 3 plugins; loadable shape; static gates present |
| c9 | c9-install-parity | 1.000 | AGENTS.md mirror identical; 3/3 plugins installed + identical; 6/6 rules; 66/66 skills discoverable |
| c10 | c10-runtime-load | 1.000 | 3/3 plugins seen loading in the server log; 0 load errors |

10/10 pass, **TOTAL 1.000**. A green score is a contract on files, not proof of runtime
behaviour — the runtime claims (plugin loads, skill loads, agent dispatch) still need
their own check.

---

## Mutation test (2026-10-22) — proving the bench can still fail

A benchmark that cannot fail is theater. `checks/mutation-test.sh` breaks one harness
asset at a time against the live config, asserts the matching check drops, restores
from the toolkit source, and asserts green again.

| mutation | check | result |
| -------- | ----- | ------ |
| reviewer agent switched back to `mode: all` | c5 | **bit** — 1.0 → 0.833 |
| brief loses its `## Inputs the parent provides` section | c5 | **bit** — 1.0 → 0.994 |
| brief points at a prompt file that does not exist | c5 | **bit** — 1.0 → 0.994 |
| always-on trigger lines deleted | c6 | **bit** — 1.0 → 0.75 |
| one plugin stops hooking the loop | c8 | **bit** — 1.0 → 0.944 |
| a committed plugin is not installed live | c9 | **bit** — 1.0 → 0.9 |
| always-on payload pushed past the 24k cap | c1 | **bit** — 1.0 → 0.667 |

Each mutation must do **two** things to count as a pass: dent its check's score *and*
turn the ship gate red. The second assertion exposed a separate defect after the
mutation test passed: `pass` in the aggregate meant `score >= 0.5` and the gate only
thresholded the *average*, so the over-cap state (c1 = 0.667, nine checks at 1.0)
totalled 0.967 ≥ 0.90 and the gate exited **green**. `scripts/bench-gate.py` now
requires every check to score exactly 1.0; `bench-guard.js` nudges on the same rule.

Final state after the run: every check back to 1.0 and the live harness
byte-identical to the toolkit source.

**Two checks did not bite on the first run and were fixed** — that is the point of the
test:

1. `c5` accepted *either* the canonical pointer *or* the inputs section, so a brief
   missing its inputs still scored full. It now requires **both** (and separately
   checks that the named prompt/skill exists on disk — 26/26 resolve).
2. `c8` passed when **any one** plugin hooked the loop, so unhooking one plugin was
   invisible. It now scores per-plugin loop coverage (3/3 hook: 2 tool-loop,
   1 session-hook) plus the tool-loop requirement.

Known limitation, stated rather than hidden: `c10` proves a plugin was **loaded at
least once** (server log), so it cannot detect a plugin being *removed* — the log keeps
the old entry. Removal is `c9`'s job (install parity). The mutation test documents
this split instead of pretending c10 covers it.

### What the 1.000 does and does not mean

| | |
|---|---|
| **does** | every harness surface the bench measures is present, wired, consistent and in parity with the toolkit source; the mutation test shows the checks detect breakage |
| **does not** | that a skill loads when the model calls it, that a dispatched agent behaves, that the paper's own end-task metrics (+4 to +12 pts) reproduce here, or that a plugin's WARN lands in a live session — those need a behavioural test, not a file contract |

Score movement decomposition since the 2026-10-18 baseline (0.956 over 8 checks →
1.000 over 10): part is real asset work (graphify installed, 18 agents flipped to
`subagent`, 26/26 briefs made self-contained, +10 trigger lines), part is check-surface
correction (c5 mode semantics, c8 V2 hook detection), and part is metric-bug fixes
(c6 denominator, c7 line-vs-name counting). Compare per check against the same check
version; the 8-check and 10-check totals are not comparable.
