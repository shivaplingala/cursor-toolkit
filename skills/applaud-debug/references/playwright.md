# Playwright repro

Turn the ticket steps into one Playwright spec. Run that same file on stage to reproduce, then again after the fix on local and on stage.

This is not the FCD `playwright-qa` suite and not `Playwright-Automation`. Specs stay in this skill folder. Do not commit them into applaud-cloud, applaud-ui-vue3, or applaud-serverless.

## Write it before the first click

File: `~/.cursor/skills/applaud-debug/repros/<REF>.spec.ts`

- Steps come from the ticket (description, comments, video). One journey, the failing one.
- `baseURL` is `process.env.BASE_URL`. No hardcoded host.
- Assert the bug. A failing assertion means the bug is present. A pass means it is gone.
- Record console errors, failed HTTP responses, and websocket frames on the page (`page.on('console')`, `page.on('response')`, `page.on('websocket')`).
- Role or label locators. No secrets in the file. Sign-in uses env the user gave you. If the stage URL or login is missing, ask before writing a guessed journey.

## Run

From `~/.cursor/skills/applaud-debug`. Install `@playwright/test` there once if `npx playwright test` cannot start.

```bash
# stage repro — expect the bug assertion to fail
BASE_URL="<stage-url>" npx playwright test repros/<REF>.spec.ts

# after the fix, local apps already booted (local.md)
BASE_URL="<local-ui-url>" npx playwright test repros/<REF>.spec.ts

# same spec, stage again
BASE_URL="<stage-url>" npx playwright test repros/<REF>.spec.ts
```

While a run is in flight, read logs for that target: stage pm2 or CloudWatch during the stage run, the local process log during the local run. Lambda checks on personal stage `dev-lshiva` stay on CloudWatch.

## After the fix

Verify the code change locally first (the local spec must pass). Then run the same spec on stage. Local pass means the fix works on the branch you booted. Stage pass means that deployed branch has the fix too. If stage still fails and `stage_logs.sh` shows the old branch, say that. Do not treat it as the local fix being wrong. If you cannot log in or the URL is unknown, ask.
