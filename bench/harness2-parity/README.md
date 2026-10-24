# harness2-parity bench

Deterministic (no model calls) test suite that grades our OpenCode + cursor-toolkit
setup against the eight improvement levers harness2 (Google Research's recursive
agent harnessing framework, `~/harness2`) exposes on the OpenCode substrate:

| c-# | lever | harness2 surface |
|---|---|---|
| c1 | systemprompt | `systemprompt.md` (+ agent bodies), always-on cap 24 000 chars |
| c2 | guardrails | `guardrails.md` — standing deny/ask gates, verify-before-dispatch order |
| c3 | memory | `LongTermMEMORY.md` + per-domain lesson library (`EXPERIENCE.md`: cue/lesson/evidence) |
| c4 | tool guidance | `tool_descriptions/tool_guidance.md` — one centralized tool-prose surface |
| c5 | subagents | `sub_agents/<n>/AGENT.md`, `mode: subagent`, own-context briefs |
| c6 | skills | `skills/<n>/SKILL.md`, `name == dir`, description, **trigger lines in always-on text** |
| c7 | scripts | `scripts/*.py` deterministic helpers; validated (compile) + shipped with callers |
| c8 | plugins | `plugin/<name>.ts` — the in-tool-loop enforcement lever (cannot be skipped by the model) |
| c9 | install parity | *local check, not a paper lever* — toolkit source vs the live `~/.config/opencode` install |
| c10 | runtime load | *local check, not a paper lever* — the server log proves each installed plugin actually loaded |

## Layout

- `checks/benchlib.py` — shared helpers (frontmatter split, grep-scan, JSON emit)
- `checks/c1…c10_*.py` — one check per lever family; each is importable AND executable
  and prints one JSON line:
  `{"id", "component", "desc", "pass" (bool), "score" (0..1 or null when skipped), "evidence"}`
  Scoring: each sub-condition contributes equally; pass = score >= 0.5.
- `checks/all.py` — runs every check in one process and prints a summary JSON line
  (no result file written; used by the gate and the plugin)
- `runner.sh` — runs all checks, writes `results/bench-results-<YYYYMMDD>.json`
  (`{run_ts, checks, summary:{per_component_avg, total_score, passed, failed, skipped,
  failed_ids}}`), prints a table. **Exit 0 always** — a failing check is data.
- `compare.py` — diff two result files.
- `BENCHMARK.md` — the ranked improvement-area report + recorded baseline.

## Enforcement (where the score actually bites)

| Where | What |
| ----- | ---- |
| `~/cursor-toolkit/scripts/bench-gate.py` | gate decision point — non-zero unless **every** check scored 1.0 (`BENCH_THRESHOLD` is only a floor on the average, so no check can hide inside the mean) |
| `~/cursor-toolkit/scripts/bench-verify.sh` | runs the bench, writes a fresh result, exits non-zero unless the gate is shippable |
| `~/cursor-toolkit/.git/hooks/pre-commit` (installed by `install.sh`) | blocks a commit that stages `agents/`, `rules/`, `opencode/`, `skills/`, `scripts/`, `install.sh`, or `bench/` when the gate is red |
| `~/.config/opencode/plugins/bench-guard.js` | always-on nudge: appends one line to the system context when the last bench run was red or older than 24h |
| `~/.config/opencode/AGENTS.md` (Harness gate section) | tells every agent to run the bench after harness changes |

## Proving the bench can fail

```bash
bash checks/mutation-test.sh
```

Breaks one harness asset at a time against the live config, asserts the matching check
drops below 1.0, restores from the toolkit source of truth, and asserts the harness is
green again. A benchmark that cannot fail is theater — this is the test for the tests.
It mutates live files for milliseconds at a time and restores them; run it only when no
other process is editing the harness.

## Re-run after applying harness2-style changes

```bash
bash /home/shiva/cursor-toolkit/bench/harness2-parity/runner.sh
```

Every check is deterministic (file existence, grep/dir scans, frontmatter regex;
stdlib-only) so repeated runs on an unchanged tree must be line-for-line identical.

## Diff two recorded runs

```bash
python3 /home/shiva/cursor-toolkit/bench/harness2-parity/compare.py \
  /home/shiva/cursor-toolkit/bench/harness2-parity/results/bench-results-A.json \
  /home/shiva/cursor-toolkit/bench/harness2-parity/results/bench-results-B.json
```

It prints the component-average deltas, per-check score movement, and NEW-FAIL /
NOW-PASS lists.

## Conventions for future checks

- Never call models or network; degrade to `score: null` (skipped) rather than crash
  when a root path is absent.
- If a check must be edited, append a new baseline line in `BENCHMARK.md` noting the
  date and reason, so historical JSON stays interpretable.
- Match the **installed** OpenCode API, not a remembered one: the 2026-10-22 run
  caught two checks that graded a V1 surface (`tool.execute.after`, `mode: subagent`
  only) after the setup moved to V2 (`ctx.tool.hook("execute.after")`, `mode: all`).
  Verify against the docs for the installed version before trusting a score.
- `c10` reads the live server log, so it is the one check whose evidence can change
  without a tree change (new errors, rotated log). Everything else is tree-deterministic.
