# Full-Cycle Delivery

**Global** gated delivery pipeline
(intake → research → grill → plan approval → implement → dual review →
fix-until-0 → verify → ship).

## Canonical install (source of truth)

```
~/.cursor/plugins/local/full-cycle-delivery/
```

Skill tree lives at:

```
…/skills/full-cycle-delivery/
```

Cursor also discovers it via:

```
~/.cursor/skills/full-cycle-delivery → …/skills/full-cycle-delivery
```

## Multi-agent install (same skill, other hosts)

Same pattern as Cursor’s “plugin + discovery path”: one canonical tree, then
per-agent skill + `/full-cycle-delivery` command.

```bash
~/.cursor/plugins/local/full-cycle-delivery/scripts/install-multi-agent.sh
```

| Host | Skill discovery | Slash / command | Rule |
| ---- | --------------- | --------------- | ---- |
| **Cursor** | `~/.cursor/skills/…` (symlink) + plugin | `/full-cycle-delivery` | plugin rule |
| **Claude Code** | `~/.claude/skills/…` (symlink) | `~/.claude/commands/…` | stripped `.md` |
| **GLM Coding Plan** | Uses Claude Code paths (Z.AI → Claude Code) | same as Claude | same |
| **Codex** | `~/.codex/skills/…` (symlink) | `~/.codex/prompts/…` + rule | stripped `.md` |
| **Antigravity / Gemini** | `~/.gemini/config/skills/…` + `~/.gemini/antigravity/skills/…` (**real copy**) | `~/.gemini/config/commands/…` | dual `.mdc` + stripped `.md` |
| **OpenCode** | `~/.config/opencode/skills/…` (symlink) | `~/.config/opencode/command/…` | — |
| **Kilo Code** | `~/.kilo/skills/…` (symlink) | `~/.config/kilo/command/…` | — |
| **Kimi Code** | `~/.kimi-code/skills/…` (symlink) | `~/.kimi-code/commands/…` | — |
| **Agents hub / Zed** | `~/.agents/skills/…` (symlink; **Zed global skills root**) | `~/.agents/commands/…` | — |

Antigravity gets a **copy** (not a symlink) because Antigravity IDE has known
gaps following symlinked skills under some roots. Re-run the install script
after updating the plugin skill (**copy freshness**). Glossary/ADRs:
`docs/agent-host-discovery/` in the workspace.

**Zed** loads global skills from `~/.agents/skills/` (official); install already
symlinks there — no separate Zed tree.

Health:

```bash
~/.cursor/plugins/local/full-cycle-delivery/scripts/fcd-doctor.sh
~/.cursor/plugins/local/full-cycle-delivery/scripts/install-multi-agent.sh --check
~/.cursor/plugins/local/full-cycle-delivery/scripts/test-host-matrix.sh
```

Dependencies (global; already linked for Cursor/Claude):

- `grill-me`
- `grill-with-docs`
- `research-agent`

Reload / restart each agent session after install.

## Components

| Component | Purpose |
| --------- | ------- |
| Skill `full-cycle-delivery` | Pipeline + playbooks + prompts |
| `/full-cycle-delivery` | Slash / prompt command |
| Agents `coding-reviewer`, `impact-reviewer`, `review-fix-loop` | Dual review + fix-until-zero (Cursor + Kilo agent briefs) |
| Rule (agent-requestable) | Steer agents onto the skill for delivery work |

## Sync from repo (optional)

If `serverless-monorepo` skill drifts ahead of the plugin copy:

```bash
rsync -a --delete \
  /path/to/serverless-monorepo/.claude/skills/full-cycle-delivery/ \
  ~/.cursor/plugins/local/full-cycle-delivery/skills/full-cycle-delivery/
~/.cursor/plugins/local/full-cycle-delivery/scripts/install-multi-agent.sh
```

## Review → fix loop (Phase 4–5)

1. Coding reviewer (diff bugs / edge cases) — read-only  
2. Impact reviewer (GitNexus + graphify) — read-only  
3. Main agent fixes → re-verify → re-review until both `FINDING_COUNT: 0` (max 10)

## Related

- Repo spec (when open): `skills-agents-autos-plans/FULL-CYCLE-DELIVERY-PLAN.md`
- Cursor rule: Settings → Rules → **Full-cycle delivery (global)**
