---
name: applaud-debug
description: >-
  Debug and fix Applaud product bugs from an Aha ticket. Read description,
  comments, requirements, acceptance criteria, history, and attachments; ask if
  it reproduces on stage; reproduce on stage when yes or not checked; match that
  branch locally; fix; rerun one Playwright spec on local and on stage. Use when
  the user gives an Aha link or AC-* id, says debug this, reproduce on stage,
  check stage logs, or investigate applaud-cloud, applaud-ui-vue3, or
  applaud-serverless. Serverless: `lsp` to personal stage `dev-lshiva`, not
  `npm run dev`.
---

# Applaud debug

`agents-debug` is AgentCore, not this product. **`stage-mongo`** stays local (credentials) — not in this repo.

## Order

1. **Read the ticket** before any theory. Description, comments, requirements, acceptance criteria, history, videos, images, markdown, and other files. [references/aha.md](references/aha.md).
2. **Ask** before booting anything: "Is this reproducible on stage?"
   - **Yes**, or **no, I haven't checked** → you reproduce it on stage.
   - **No** (already checked, not on stage) → ask how to proceed. Do not guess a branch.
3. **Stage repro.** Write a Playwright spec from the ticket steps and run it against the stage URL. [references/playwright.md](references/playwright.md). Note the deployed branch (`scripts/stage_logs.sh`). Watch network, websockets, and console at the same time as stage logs (and CloudWatch when the path is AWS). [references/observe.md](references/observe.md).
4. **Reproduced on stage** → check out that same branch locally. [references/local.md](references/local.md). `graphify query "<symptom>"` before reading code.
5. **Not reproduced on stage** → stop and ask. Do not switch to another branch on your own.
6. **Fix** locally, then verify locally first (cloud / UI / `lsp` commands in [references/local.md](references/local.md)). Then run the **same** Playwright spec on local and on stage. Confirm the repro is gone, and check every other caller of the code you changed. Difficulty at any step → ask.

## Branch

- Stage repro succeeded → local checkout is the branch `stage_logs.sh` printed.
- Ticket or the user names a branch, and there is no stage branch to match → that branch.
- No branch named → `development`, or ask if two names are plausible.
- Dirty tree, or the branch is missing locally → ask. Do not stash or discard.

## Do not

- Boot local apps before the stage question is answered.
- Hypothesize or edit code before the stage repro (or the user has said it is not on stage and told you how to continue).
- Print SSH passwords, Mongo URIs, or Aha tokens.
- Leave Aha downloads or `/tmp/mcp-video-*` on disk (skill `aha-video-understanding`).
- Run `npm run dev` or `sst dev` in applaud-serverless. Deploy with `lsp` to `dev-lshiva`.
- Hand-click the repro when a Playwright spec can walk it. Re-run that same spec on local and on stage after the fix.
- Patch one caller and leave a sibling caller on the same function broken.
