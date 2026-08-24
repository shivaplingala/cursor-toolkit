# Full-Cycle Delivery

**Global** gated delivery pipeline
(intake → research → grill → plan coding+impact to 0 → plan approval → implement → dual review →
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

```bash
~/.cursor/plugins/local/full-cycle-delivery/scripts/install-all-hosts.sh
```

One catalog in `scripts/lib/host-discovery.sh` (ADR 0003). Per-plugin scripts still work.

| Host | Skill discovery | Slash / command | Rule |
| ---- | --------------- | --------------- | ---- |
| **Cursor** | `~/.cursor/skills/` (symlink) + plugin | `~/.cursor/commands/` | plugin + `~/.cursor/rules/*.mdc` |
| **Claude Code** | `~/.claude/skills/` | `~/.claude/commands/` | stripped `~/.claude/rules/*.md` |
| **GLM Coding Plan** | Claude Code paths | same as Claude | same |
| **GLM ZCode** | `~/.zcode/skills/` | skill name as `/name` | — |
| **Codex** | `~/.codex/skills/` | `~/.codex/prompts/` | stripped `~/.codex/rules/*.md` |
| **Antigravity / Gemini** | **real copy** both Gemini skill roots | both command roots | dual `.mdc` + stripped `.md` |
| **Zed** | `~/.agents/skills/` | `~/.agents/commands/` | — |
| **OpenCode** | `~/.config/opencode/skills/` | `~/.config/opencode/command/` | — |
| **Kilo Code** | `~/.kilo/skills/` | `~/.config/kilo/command/` | — |
| **Kimi Code** | `~/.kimi-code/skills/` | `~/.kimi-code/commands/` | — |
| **Qwen Code** | `~/.qwen/skills/` | `~/.qwen/commands/` | — |
| **DeepSeek Harness** | `~/.dsh/skills/` **and** `~/.agents/skills/` | — | — |

Antigravity gets a **copy** (not a symlink). Re-run the installer after plugin updates (**copy freshness**). Glossary/ADRs: `docs/agent-host-discovery/` in the workspace.

Health:

```bash
~/.cursor/plugins/local/full-cycle-delivery/scripts/fcd-doctor.sh
~/.cursor/plugins/local/full-cycle-delivery/scripts/install-all-hosts.sh --check
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
2. Impact reviewer (GitNexus **and** graphify — both required) — read-only  
3. Main agent fixes → re-verify → re-review until both `FINDING_COUNT: 0` (max 10)

## Related

- Repo spec (when open): `skills-agents-autos-plans/FULL-CYCLE-DELIVERY-PLAN.md`
- Cursor rule: Settings → Rules → **Full-cycle delivery (global)**
