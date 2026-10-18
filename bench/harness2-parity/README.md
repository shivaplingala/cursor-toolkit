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

## Layout

- `checks/benchlib.py` — shared helpers (frontmatter split, grep-scan, JSON emit)
- `checks/c1…c8_*.py` — one check per lever family; each is importable AND executable
  and prints one JSON line:
  `{"id", "component", "desc", "pass" (bool), "score" (0..1 or null when skipped), "evidence"}`
  Scoring: each sub-condition contributes equally; pass = score >= 0.5.
- `runner.sh` — runs all checks, writes `results/bench-results-<YYYYMMDD>.json`
  (`{run_ts, checks, summary:{per_component_avg, total_score, passed, failed, skipped,
  failed_ids}}`), prints a table. **Exit 0 always** — a failing check is data.
- `compare.py` — diff two result files.
- `BENCHMARK.md` — the ranked improvement-area report + recorded baseline.

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
