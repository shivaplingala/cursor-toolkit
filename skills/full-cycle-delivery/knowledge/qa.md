# QA — delivery craft

- Local FCD QA baseURL: **`http://127.0.0.1:8080`** only (`ui-vue3-app`).
- Do not use `Playwright-Automation` remote defaults for FCD local loops (`docs/FCD_LOCALHOST_POLICY.md`).
- Config rejects non-loopback `PLAYWRIGHT_BASE_URL` unless `CI=1` or `ALLOW_REMOTE_E2E=1`.
- Emit `sidecars/qa-round-<n>.md` with FAIL_LIST for the orchestrator every round.
- Gate + sign-off: skills **qa** / **playwright-qa** + agent **qa-engineer**.
