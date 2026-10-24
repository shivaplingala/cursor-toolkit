# Debug — delivery craft

- No “done” without fresh verify output (`verify-scope`, doctor/`--check`, or `npm run test:e2e`).
- Playwright remote `baseURL` (example / example-learn) is **not** the local FCD target — if tests hit the wrong host, check `PLAYWRIGHT_BASE_URL` / `ALLOW_REMOTE_E2E`.
- EBS/SSO Vue shell: no local password form — auth smokes need `E2E_STORAGE_STATE` or stay skipped.
- graphify worker pool can warn on some markdown files while AST still finishes — re-run `graphify update <path>` if nodes look stale.
- applaud-serverless may lack `scripts/verify-scope.sh`; fall back to `apps/<app> npm test` plus the plan’s Cloud/Vue file list.
- Vue `PARAM_TYPE_TO_DYNAMIC_DATA_TYPE.user` maps to `'foreignKey'` (User model picker), not `'user'`.

