# Agent host discovery install

## Purpose

Glossary and ADRs for publishing Cursor local-plugin skills/commands/rules into other agent hosts (especially Antigravity).

## Ownership

Workspace docs under `docs/agent-host-discovery/`. Canonical plugin trees remain under `~/.cursor/plugins/local/applaud-*`.

## Local Contracts

- Terms: see `CONTEXT.md`
- ADRs: `docs/adr/0001-antigravity-skill-copies.md`, `docs/adr/0002-antigravity-dual-rule-shapes.md`, `docs/adr/0003-host-matrix.md`
- Plan: `docs/plans/2026-08-07-antigravity-host-discovery-install.md`

## Work Guidance

- Prefer existing installer helpers (`copy_skill`, dual-rule install) over new sync machinery
- After editing a canonical plugin skill/rule, re-run `scripts/install-all-hosts.sh` (or that plugin’s installer)
- Sharing FCD + FCD-V2 with another Cursor user: `fcd-cursor-share/` (`bash install.sh`; refresh snapshot with `bash install.sh --pack`)

## Verification

```bash
~/.cursor/plugins/local/full-cycle-delivery/scripts/fcd-doctor.sh
~/.cursor/plugins/local/full-cycle-delivery/scripts/test-host-matrix.sh
```

- Re-run the three install scripts and assert Antigravity skill/command/rule paths exist
- `install-*.sh --check` after plugin edits (copy freshness)

## Child DOX Index

- (none)
