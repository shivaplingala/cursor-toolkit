## 2026-09-04

- LoopBack embeds: `_.has(parameter, 'defaultValue')` is always false (`__data`). Use getter (`!== undefined`). Catch-null of `validateValueForProperty` must rethrow for new required-number operators (`olderThanNDays`).
- OOB date params skip `buildConditionNode`; ParameterResolver must emit execution `lessThan` + `YYYY-MM-DD`, not UI `before`. Dual-path: nested filters vs parameters.
- `verify-scope.sh` may be absent in applaud-serverless (only `scripts/check-test-coverage.mjs`). Use app `npm test` + Cloud/Vue scoped suites as the work-type verify.
- Vue `PARAM_TYPE_TO_DYNAMIC_DATA_TYPE.user` is `'foreignKey'` (User picker); do not expect `'user'`.


- Phase 3: after research + grill + complete plan, run `plan-review-fix-loop` (coding + impact of planned files/callers) to `FINDING_COUNT: 0` before asking plan approval. Same for `/fcd-v2`. Fixes go in the plan, not product code.

## 2026-08-12

- Seeded corpus from FCD progress + Playwright QA delivery: localhost-only QA, agency path fix, BE/FE/QA agents, qa-fix-loop, FCD-V2 Phase 4 parity.
- Playwright-Automation is a nested remote-tenant framework; FCD smoke lives in `ui-vue3-app`.

- Re-run `install-multi-agent.sh` / FCD-V2 `install-symlinks.sh` after plugin updates so Gemini/Antigravity **copies** (incl. knowledge/) stay fresh; symlink hosts pick up instantly.
- Companion skills must be real dirs under `~/.cursor/skills/` — never symlink loops (qa incident 2026-08-12).

## 2026-09-21

- Mirror prod wait/timeout semantics exactly in throwaway harness probes (same env name, default, clamp, remaining-budget math) so host measurements stay honest as prod evolves; divergent harness env names drift silently (context: mcp-timeout-harness ask_question_wait mirrors MCP_CHAT_SYNC_WAIT_SECONDS).
- Branch-cover probe tools with env-forced fast paths (`JOB_TIMEOUT_SECONDS=0` → done branch; long timeout + short wait → processing branch) when the tool body has no unit harness; document both in README smoke (context: mcp-timeout-harness).
- Impact review without GitNexus/graphify MCP in-session: full-file reads of every touched file + grep caller trace + green suite is the fallback; record `EVIDENCE: gitnexus=no` and let the human waive the tooling finding explicitly instead of silently passing (context: hybrid-chat-job-polling FCD-V2).
- Subagent review-fix loop (classic): dispatch coding + impact reviewers in parallel with verbatim file lists, AC, and strict output shape; monitor task ids to completion, merge by path/symbol, fix only merged code findings — converged in 1 round here (coding PASS 0, impact 1 protocol-tooling finding) (context: hybrid-chat-job-polling FCD-V2).

## 2026-10-18

- Ported the 12+ FCD/FCD-V2 agents to OpenCode V2 as global markdown agents at `~/.config/opencode/agents/fcd/*.md`; nested dir becomes the agent ID namespace (`fcd/orchestrator`, `fcd/coding-reviewer`, …), which is what lets an orchestrator allowlist subagents via `subagent` resource `fcd/*` (context: opencode-agents fcd-v2).
- OpenCode V2 agent discovery is loaded by the background service at config load; newly dropped agent .md files only appear after `opencode service restart`. Verify via `opencode api get /api/agent` → `data[].id` (context: opencode-agents).
- V2 markdown agent frontmatter that loads cleanly: `description`, `mode` (`subagent`/`all` — custom agents default to `primary`, so always set it), `color` (hex), `permissions` as ordered `{action, resource, effect}` rules; YAML body after `---` becomes the system prompt. Read-only reviewers: deny `edit` + `shell` (with targeted shell allows like `graphify *` after the deny — last-match-wins). (context: opencode-agents)
- OpenCode agents cannot load Cursor skills; for reviewers/implementers add read allows for `~/.cursor/**` + `~/.agents/**` and also inline the distilled prompt rules in the agent body so they work without external files. The user's global `agent.build/plan.prompt` uses the legacy V1 `prompt` field — V2 equivalent is `agents.<id>.system`.

## 2026-10-18 (applaud agents, later same day)

- 6 applaud-debug agents created at `~/.config/opencode/agents/applaud/` (orchestrator `all`; ticket-reader / stage-repro / local-matcher / fixer / repro-runner `subagent`). Sibling review reuses `fcd/coding-reviewer` + `fcd/impact-reviewer`; applaud Playwright specs stay separate from FCD `playwright-qa` suites (context: applaud-debug SKILL.md + references).
- Permission-rule shape is strict: a rule missing one key (`effect` omitted after a botched edit) is not a partial match — the whole agent silently disappears from `/api/agent` discovery. Always verify with the 3-key checker + dupe check after edits (context: applaud/local-matcher recovery).
- Last-match-wins ordering burn: `npm run dev*` initial `ask` followed later by a blanket re-`deny` flips it back to blocked — place broad rules first, specific refinements last. Shell `resource` is raw command text: cwd is invisible, so repo-scoped deny (e.g. `npm run dev` forbidden only in applaud-serverless but required in applaud-ui-vue3) is impossible — use `ask` and enforce repo scope in the body rules.
- `lsp` is an interactive alias; subagents are non-interactive — agents must fall back to the full command `SST_TELEMETRY_DISABLED=1 sst deploy --stage dev-lshiva --print-logs --verbose` (both shell-allowlisted) (context: applaud-debug references/local.md).

## 2026-10-18 (cursor-toolkit push, later same day)

- Commit identity ≠ push auth: `git -c user.name/-c user.email` authors the commit, but the https credential helper resolves from the ACTIVE `gh` account — a 403 on push to `shivaplingala/cool-repo` while logged in as `shiva-applaud` is solved with `gh auth switch --user shivaplingala` → push → `gh auth switch` back (never echo tokens) (context: cursor-toolkit 49be2ea).
- OpenCode's always-on surfaces are (a) global `~/.config/opencode/AGENTS.md`, (b) the `instructions[]` globs in opencode.json, (c) native skills from `~/.config/opencode/skills` + `.claude/skills` compat — a `rules/*.md` directory is NOT auto-loaded: 6 rule files sat dead until wired through `instructions[]`; after wiring they demonstrably appear as session instructions (context: harness2-parity application, 2026-10-18).
- Bench checks must pivot with the config surface they measure: harness2-parity c1/c8 checks probing `plugin/` npm-style and `plugin/` dir scored 0.25/1.0 against a fictional surface while the real `plugins/budget-guard.js` was live; re-aiming checks at OpenCode's documented conventions is benchmark maintenance, not gaming — the substantive implementation checks stayed (hook + cap logic verified by content, artifact-check executed on itself).

## 2026-10-22

- A score drop in a regex-based bench is not proof of a regression: after the OpenCode V2 port (`mode: all`, `ctx.tool.hook("execute.after")`), two harness2-parity checks still graded the V1 surface and failed live capability. Verify the check against the docs for the *installed* version before changing any asset (evidence: c5 0.891→0.625 and c8 1.000→0.750 on 2026-10-22, both false).
- Skill availability must be checked against the discovery roots, not one mirror: OpenCode V2 searches `~/.config/opencode/skills` plus the global compatibility roots `~/.claude/skills` and `~/.agents/skills`. A skill absent from the opencode mirror can still be loadable — a parity check over one mirror reports a false "unavailable" (evidence: `aha-video-understanding` is loadable via `~/.agents/skills`).
- `install.sh` copies toolkit→live with `rsync --delete`, and the repo can be OLDER than the live owner. Refresh the repo from the live owner first, then install; installing from a stale repo rolls the newer content back (evidence: FCD knowledge `log.md` 44 live lines vs 13 repo lines — a plain install would have truncated the lesson corpus).
- A committed artifact is not an installed artifact: `opencode/plugins/graphify.js` sat in the repo for 3 days while never being copied to `~/.config/opencode/plugins/`, so the hook never loaded. `install.sh --check` must assert EVERY plugin file, not one named file (evidence: harness2-parity c9-install-parity).
- A bench sub-condition can be wrong while the asset is fine: c6 scored "descriptions unique" as unique-pairs-over-mirrored-files (91/384 = 0.24 against a 0.9 threshold) and c7 counted always-on script references per line — both reported real consistency as broken. Check the DENOMINATOR of every ratio before treating a low score as a missing asset (evidence: harness2-parity c6/c7 → 1.000 on 2026-10-22 after the metric fix).
- A benchmark that cannot fail is theater: mutation-test it. Breaking one asset at a time (reviewer `mode: all`, brief missing its inputs section, canonical pointer to a missing file, always-on trigger lines deleted, one plugin unhooked, plugin committed but not installed, always-on over the cap) exposed two checks that scored green on real breakage — c5 accepted either marker instead of both, c8 passed when any one plugin hooked the loop (evidence: harness2-parity mutation-test, 2026-10-22: 7/7 mutations now bite).
- A ship gate must be per-check strict, not an average threshold: with `pass := score >= 0.5` and the gate only thresholding the mean, an always-on payload 16k chars over the cap (c1 = 0.667, nine checks green) still totalled 0.967 ≥ 0.90 and the gate exited green (evidence: harness2-parity gate simulation on the recorded result doc, 2026-10-22; fixed by scripts/bench-gate.py requiring every check == 1.0 and by making the mutation test assert gate-red per mutation).
