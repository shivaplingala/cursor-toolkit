# Local debug and test

After the stage question is answered. If the bug reproduced on stage, check out the branch `stage_logs.sh` printed (`BRANCH=...`) in each repo you boot. If the user said it is not on stage and told you to continue, use the ticket branch, else `development`, else ask. If `git status` is dirty, stop and ask. Do not stash or discard.

The code fix is verified locally first, with the commands below. The same Playwright spec ([playwright.md](playwright.md)) then runs against this UI and against the stage URL.

Boot only the apps the ticket needs. If the surface is unclear, ask. Check the terminals folder before starting a second copy.

While you re-run the repro, keep the browser network, websocket, and console capture up, and read the local process log for the same time window. [observe.md](observe.md). Repeat that after the fix, including other callers of the code you changed.

## applaud-cloud

`/home/shiva/applaud/applaud-cloud`

API, LoopBack models, seed data, server behavior.

```bash
cd /home/shiva/applaud/applaud-cloud
git fetch --prune
git checkout <stage-deployed-branch>
yarn
yarn seed
yarn server:api
```

## applaud-ui-vue3

`/home/shiva/applaud/applaud-ui-vue3`

Screens, Vue, client network calls.

```bash
cd /home/shiva/applaud/applaud-ui-vue3
git fetch --prune
git checkout <stage-deployed-branch>
npm install   # only when node_modules is missing
npm run dev
```

## applaud-serverless

`/home/shiva/applaud/applaud-serverless`

Do not run `npm run dev` or `sst dev` in this repo. From the repo root, `lsp` deploys the Lambda functions to personal stage `dev-lshiva`.

```bash
cd /home/shiva/applaud/applaud-serverless
git fetch --prune
git checkout <stage-deployed-branch>
lsp
```

`lsp` is the shell alias `SST_TELEMETRY_DISABLED=1 sst deploy --stage dev-lshiva --print-logs --verbose`. If the alias is missing, run that command. Personal stage is `dev-lshiva`. Do not deploy to shared `dev` or to the stage box.

After `lsp` succeeds, point local cloud and UI at that stage before `yarn server:api` and `npm run dev`:

- `applaud-cloud/env.json`: `SST_STAGE` and `PERSONAL_DEV_STAGE` are both `dev-lshiva`. Cloud uses `SST_STAGE` for Lambda, EventBridge, and connectors. `PERSONAL_DEV_STAGE` is what the UI reads as `root.meta.personalDevStage`.
- Any other local URL, websocket, or connector stage that still targets `dev` or shared stage points at `dev-lshiva`. If the knob is unclear, ask.
- Restart `yarn server:api` after the env change. Do not commit `env.json`.

Lambda logs for this test are CloudWatch for stage `dev-lshiva` (skill `aws-diagnose-read`, read-only), read in the same window as the local browser. They are not pm2 logs on the shared stage box.

Stage data checks use skill `stage-mongo`, not a guess from local seed.
