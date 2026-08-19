# Knowledge log (append-only)

## 2026-08-12

- Seeded corpus from FCD progress + Playwright QA delivery: localhost-only QA, agency path fix, BE/FE/QA agents, qa-fix-loop, FCD-V2 Phase 4 parity.
- Playwright-Automation is a nested remote-tenant framework; FCD smoke lives in `ui-vue3-app`.

- Re-run `install-multi-agent.sh` / FCD-V2 `install-symlinks.sh` after plugin updates so Gemini/Antigravity **copies** (incl. knowledge/) stay fresh; symlink hosts pick up instantly.
- Companion skills must be real dirs under `~/.cursor/skills/` — never symlink loops (qa incident 2026-08-12).
