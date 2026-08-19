# FCD-V2 — Phase 4 swarm protocol

Only when `escalate.md` score ≥ 2. Orchestrator = main agent. Workers = Ruflo agents and/or Cursor Task with the same board rules.

**Per-task gates are mandatory** (same as classic FCD / `$SKILL_ROOT/SKILL.md` §4b): QA-first when needed → role implementer → verify → spec-reviewer → coding+impact review-fix to 0 → progress update. This protocol adds board/claims/sidecars — it does **not** replace those gates.

## Worker roles (map to FCD agents)

| Plan work | Spawn / assign |
| --------- | -------------- |
| Serverless / host-tooling | `backend-implementer` + skill **backend** |
| Vue / `ui-vue3-app` | `frontend-implementer` + skill **frontend** |
| Catalog / gate / smoke | `qa-engineer` + **qa** / **playwright-qa** |
| Review rounds | `coding-reviewer` + `impact-reviewer` (read-only); orchestrator fixes |

## Layout (workspace-local, under docs or `.fcd-v2/`)

Prefer under the feature docs folder when one exists; else repo `.fcd-v2/<slug>/`:

```text
progress.md                # durable resume ledger (required)
memory.md                 # thin live board only (≤80 lines / 8 KiB)
briefs/
  task-<id>.md            # dense per-agent brief
sidecars/
  task-<id>.diff.md       # large diffs / logs / verify dumps
  task-<id>.round-<n>.md  # coding+impact review round
  task-<id>.verify.log
```

Optional: mirror task ids into Ruflo `task_create` / `claims_*` / `memory_store` for cross-session — **file board + progress.md remain canonical**.

On swarm start: if `progress.md` exists → resume from it; sync task statuses into `memory.md` as **pointers only**.

## 1. Orchestrator writes dense briefs

For each plan task, create `briefs/task-<id>.md`:

- Goal (1–2 lines)
- Exact file paths to read/edit (and out-of-scope paths)
- Steps (numbered, imperative)
- Acceptance checks (bullets that must pass)
- Dependencies / blocked-by
- verify command (e.g. `./scripts/verify-scope.sh <workspace>`)

**Less words, no ambiguity** — agent must not need clarifying questions.  
If something is unknown, orchestrator resolves it before assigning.

## 2. Thin shared memory (`memory.md`)

Board rows only: task id, assignee, status, locks, pointers, last delta line range.

**Hard cap:** `memory.md` must stay **≤ 80 lines** and **≤ 8 KiB**. If a write would exceed that → move detail to a sidecar and leave a one-line pointer. If the board is already over the cap → **stop**, thin it, then continue (do not keep appending).

Example shape:

```markdown
# FCD-V2 board <slug>

| task | agent | status | locks | sidecar | notes |
|------|-------|--------|-------|---------|-------|
| T3 | impl-wa | in_progress | apps/channels/whatsapp/src/handlers/x.ts | sidecars/T3.diff.md | |
| T4 | impl-sms | blocked | — | — | wait T1 shared |

## Locks
- path | agent | intent | since

## Completeness (orchestrator)
- T3 MISSING: …
```

**Never** inline large diffs, logs, or full tool dumps into `memory.md`.

## 3. Sidecars for large data

If content is large (diff, log, JSON, research dump):

1. Write `sidecars/<name>`
2. Reference path + one-line summary in `memory.md`
3. Only agents that need it open the sidecar

## 4. Headroom (read lens — keep details on disk)

- Canonical = plain files (full fidelity)
- On **read** of a large sidecar into model context → `headroom_compress`; use `headroom_retrieve` when a hash marker needs detail
- Do **not** Headroom-compress the thin board
- Do **not** replace the board with compressed-only mush

## 5. Append-only plan / brief deltas

Orchestrator **never rewrites** the whole brief.

Append:

```markdown
## Delta @ L84–L91 (<iso-time>)
MISSING / KEEP / DO:
- …
```

Tell the agent: *Read only Delta @ Lx–Ly; do not re-read the full brief unless instructed.*

## 6. Claim-before-edit (overlapping files)

Before editing a path:

1. Read `memory.md` locks for that path
2. If free → claim: `path | agent | intent | since`
3. If locked or other changes exist → **stop coding**; ask orchestrator
4. Orchestrator appends a brief delta: what to **keep** vs what to **do next**
5. Agent resumes from that delta line range only
6. On done (or handoff) → release lock; update status; optional sidecar pointer

## 7. Completeness loop (orchestrator)

For each task until `done`:

1. Compare agent report + board + AC in brief
2. Run verify command from brief (exit 0 required when in serverless-monorepo)
3. If incomplete → append MISSING delta with line numbers; re-assign; do not mark complete
4. If complete → `status=done`, release locks, optional Ruflo `task_complete`

Do not advance to Phase 5 while any assigned task is not `done` (or explicitly deferred by human).

## 8. Ruflo usage (optional glue)

When swarming:

1. `swarm_init` hierarchical, `maxAgents` ≤ 5 unless user asks more
2. `task_create` / `task_assign` aligned to brief ids
3. `agent_spawn` / `agent_execute` for implementer / tester as needed
4. `claims_board` may mirror file locks; file board still wins on conflict
5. `swarm_shutdown` when Phase 4 swarm work ends

Skip Ruflo MCP if Cursor Task workers already follow this file protocol and user prefers no swarm process.

## 9. Exit to Phase 5

When all tasks `done`:

- Hand off to FCD whole-branch **coding + impact** review-fix loop until both `FINDING_COUNT: 0`
- Keep `memory.md` + sidecars for reviewers (pointers only in prompts; Headroom large sidecars)
