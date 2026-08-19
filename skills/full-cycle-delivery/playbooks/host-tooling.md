# Playbook: host-tooling

**Work type:** `host-tooling`  
**When:** User-global Cursor plugins, install scripts, skill/command/rule discovery, FCD/FCD-V2 process docs under `~/.cursor/plugins/local/` — not serverless-monorepo app code.

## Fast lane (still gated)

- Still need **grill-me** then **grill-with-docs**, but keep grill short (≤3 questions each) focused on scope, verify command, and risk to other hosts.
- Still need **explicit plan approval** before Phase 4.
- Prefer Ponytail; no agency architect unless structural ADR.

## Order

1. Edit canonical plugin trees only (`~/.cursor/plugins/local/*`)
2. Re-run that plugin’s install script (and `fcd-doctor.sh` / `--check`)
3. Update `docs/agent-host-discovery/` CONTEXT/ADRs when terms or Antigravity contracts change
4. After plan approval: create/update `*.progress.md` from FCD `templates/progress.md`

## Verify (N/A for verify-scope)

Do **not** require `./scripts/verify-scope.sh` unless an serverless-monorepo workspace was also touched.

Minimum verify:

```bash
bash -n ~/.cursor/plugins/local/full-cycle-delivery/scripts/*.sh
bash -n ~/.cursor/plugins/local/full-cycle-delivery/scripts/lib/*.sh
~/.cursor/plugins/local/full-cycle-delivery/scripts/test-host-matrix.sh
~/.cursor/plugins/local/full-cycle-delivery/scripts/fcd-doctor.sh
```

(Or scoped: that plugin’s `install-*.sh --check` after install.)

## Skip

- research-agent (unless new host path docs required — e.g. Zed/Antigravity official docs)
- Personal SST / `npm run quality` unless serverless also changed
