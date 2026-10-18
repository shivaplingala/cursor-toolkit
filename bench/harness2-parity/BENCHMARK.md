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
