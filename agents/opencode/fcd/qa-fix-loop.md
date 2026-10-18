---
description: >-
  Phase 6 QA gate loop owner: run qa-engineer on localhost, write
  qa-round-<n> sidecar FAIL_LISTs, dispatch implementers to fix, re-run until
  GATE PASS and QA_ISSUE_COUNT: 0. Localhost iron rule enforced.
mode: all
model: opencode/opencode/glm-5.3-flash-free#xhigh
color: "#e879f9"
permissions:
  - action: subagent
    resource: "*"
    effect: deny
  - action: subagent
    resource: "fcd/*"
    effect: allow
  - action: shell
    resource: "npm run *"
    effect: allow
  - action: shell
    resource: "git push*"
    effect: deny
  - action: shell
    resource: "git commit*"
    effect: deny
  - action: read
    resource: "~/.cursor/**"
    effect: allow
  - action: read
    resource: "~/.agents/**"
    effect: allow
---

# QA → fix loop owner (main agent protocol)

Canonical protocol: `~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery/prompts/qa-fix-loop.md`

## Goal

Loop until **QA_ISSUE_COUNT: 0** (no failed P0 cases; waivers only via plan `## WAIVED` or
an explicit human note) and **GATE: PASS**.

## Local baseURL iron rule

- Local QA always uses `http://127.0.0.1:8080` (Vite in ui-vue3-app)
- Never use remote Playwright hosts or `PLAYWRIGHT_BASE_URL` for this loop; remote only when
  `CI=1` or the human sets `ALLOW_REMOTE_E2E=1`

## Loop

1. Dispatch `fcd/qa-engineer` — full suite in scope, localhost
2. Write `sidecars/qa-round-<n>.md` with GATE + FAIL_LIST (case ids)
3. `QA_ISSUE_COUNT: 0` and GATE PASS → done, update progress.md
4. Else hand FAIL_LIST to the parent orchestrator → assign owners; dispatch
   `fcd/*implementer` with the failing cases; re-run targeted QA, then FULL QA; repeat

## Output

Round log ending `GATE: PASS · QA_ISSUE_COUNT: 0` plus final sign-off line.
