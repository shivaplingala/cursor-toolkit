# Debug — delivery craft

- No “done” without fresh verify output (`verify-scope`, doctor/`--check`, or `npm run test:e2e`).
- Playwright remote `baseURL` (example / example-learn) is **not** the local FCD target — if tests hit the wrong host, check `PLAYWRIGHT_BASE_URL` / `ALLOW_REMOTE_E2E`.
- EBS/SSO Vue shell: no local password form — auth smokes need `E2E_STORAGE_STATE` or stay skipped.
- graphify worker pool can warn on some markdown files while AST still finishes — re-run `graphify update <path>` if nodes look stale.
- FCD-V2: if `$FCD_ROOT` prompts missing, fail closed (compatibility pin) — do not freestyle gates.
