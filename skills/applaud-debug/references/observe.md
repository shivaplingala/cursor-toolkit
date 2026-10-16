# Watch the failure

Stage comes first. Do this when the user says the bug is on stage, or that they have not checked. A log line without the request that caused it is incomplete.

## Deployed branch

Run this before the Playwright spec. The `BRANCH=` line is the branch you will check out locally if the bug reproduces.

```bash
# deployed branch + pm2 list
~/.cursor/skills/applaud-debug/scripts/stage_logs.sh
# one service, last 1000 lines, then exit — run again during the spec
~/.cursor/skills/applaud-debug/scripts/stage_logs.sh <pm2-name>
```

SSH is the stage-mongo host (`mgtmp@172.16.1.44`, `workspace/applaud-cloud`). The password is the stage-mongo one. Never print it. Remote command is `pm2 logs ${service} --lines 1000` with `--nostream` so the SSH call returns.

## Browser

Drive the journey with the Playwright spec ([playwright.md](playwright.md)). While it runs, keep network, websocket, and console in view (the spec records them; do not skip the log window). After the run, record:

- failing HTTP status, URL, and response body
- websocket frames around the failing step
- console errors and warnings

## Logs (same time window)

| Where the code runs | Read |
| --- | --- |
| Stage `applaud-cloud` | `scripts/stage_logs.sh` during the spec, same window as the browser. |
| AWS Lambda / API Gateway on stage | Skill `aws-diagnose-read` (read-only). Do not mutate the account. |
| Local, after the matching branch is checked out | The terminal running that process. Quote the lines from the repro, not the whole boot. |
| Personal serverless `dev-lshiva` | CloudWatch for those Lambdas, same window as the local UI spec. |

## After the fix

Boot local apps with [local.md](local.md). Confirm the fix locally first. Then run the same Playwright spec twice: `BASE_URL` = the local UI, then `BASE_URL` = the stage URL. Confirm the symptom is gone in the spec, in the browser log it captured, and in the matching process log. Grep every caller of the function or module you changed and exercise the ones that share that path. If a caller cannot be checked, say so and ask.
