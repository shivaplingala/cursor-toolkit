#!/usr/bin/env bash
# Host discovery install for full-cycle-delivery (Claude, Codex, Antigravity,
# OpenCode, Kilo, Kimi, Agents hub / Zed, …). GLM Coding Plan → Claude paths.
# Usage: install-multi-agent.sh [--check]
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/host-discovery.sh
source "$PLUGIN_ROOT/scripts/lib/host-discovery.sh"

SKILL_SRC="$PLUGIN_ROOT/skills/full-cycle-delivery"
CMD_SRC="$PLUGIN_ROOT/commands/full-cycle-delivery.md"
RULE_SRC="$PLUGIN_ROOT/rules/full-cycle-delivery.mdc"
NAME="full-cycle-delivery"

[[ -f "$SKILL_SRC/SKILL.md" ]] || { echo "missing skill: $SKILL_SRC" >&2; exit 1; }
[[ -f "$CMD_SRC" ]] || { echo "missing command: $CMD_SRC" >&2; exit 1; }

MODE="${1:-install}"
if [[ "$MODE" == "--check" ]]; then
  rc=0
  echo "=== CHECK $NAME ==="
  hd_check_skill_copy "$SKILL_SRC" "$HOME/.gemini/config/skills/$NAME" || rc=1
  hd_check_skill_copy "$SKILL_SRC" "$HOME/.gemini/antigravity/skills/$NAME" || rc=1
  hd_check_file "$CMD_SRC" "$HOME/.gemini/config/commands/$NAME.md" || rc=1
  hd_check_file "$CMD_SRC" "$HOME/.claude/commands/$NAME.md" || rc=1
  hd_check_rule_dual "$RULE_SRC" "$NAME" || rc=1
  # Symlink hosts (Zed uses agents hub)
  for dest in \
    "$HOME/.cursor/skills/$NAME" \
    "$HOME/.agents/skills/$NAME" \
    "$HOME/.claude/skills/$NAME" \
    "$HOME/.codex/skills/$NAME"
  do
    hd_check_skill_link "$SKILL_SRC" "$dest" || rc=1
  done
  [[ -d "$SKILL_SRC/knowledge" ]] || { echo "CHECK FAIL missing knowledge/ in plugin"; rc=1; }
  [[ -d "$HOME/.gemini/config/skills/$NAME/knowledge" ]] || { echo "CHECK FAIL gemini missing knowledge/"; rc=1; }
  exit $rc
fi

echo "canonical skill: $SKILL_SRC"
echo

hd_link_skill "$SKILL_SRC" "$HOME/.cursor/skills/$NAME"
mkdir -p "$HOME/.cursor/commands"
hd_install_command "$CMD_SRC" "$HOME/.cursor/commands/$NAME.md"

# Companion skills (global, used by Phase 4 agents). Canonical = ~/.cursor/skills/<name> real dirs.
for companion in backend frontend qa playwright-qa; do
  src="$HOME/.cursor/skills/$companion"
  if [[ -L "$src" ]]; then
    echo "WARN companion $companion is symlink — expected real dir under ~/.cursor/skills; skipping distribute" >&2
    continue
  fi
  if [[ ! -d "$src" || ! -f "$src/SKILL.md" ]]; then
    echo "WARN missing companion $src" >&2
    continue
  fi
  for hub in "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.codex/skills" \
    "$HOME/.config/opencode/skills" "$HOME/.kilo/skills" "$HOME/.kimi-code/skills"
  do
    mkdir -p "$hub"
    hd_link_skill "$src" "$hub/$companion"
  done
  if [[ -d "$HOME/.gemini/config/skills" ]]; then
    hd_copy_skill "$src" "$HOME/.gemini/config/skills/$companion" || true
  fi
  if [[ -d "$HOME/.gemini/antigravity/skills" ]]; then
    hd_copy_skill "$src" "$HOME/.gemini/antigravity/skills/$companion" || true
  fi
done

# Agents hub = Claude compat + **Zed global skills** (~/.agents/skills)
hd_link_skill "$SKILL_SRC" "$HOME/.agents/skills/$NAME"
hd_install_command "$CMD_SRC" "$HOME/.agents/commands/$NAME.md"

hd_link_skill "$SKILL_SRC" "$HOME/.claude/skills/$NAME"
hd_install_command "$CMD_SRC" "$HOME/.claude/commands/$NAME.md"
hd_install_rule_md "$RULE_SRC" "$HOME/.claude/rules/$NAME.md"

hd_link_skill "$SKILL_SRC" "$HOME/.codex/skills/$NAME"
hd_install_command "$CMD_SRC" "$HOME/.codex/prompts/$NAME.md"
hd_install_rule_md "$RULE_SRC" "$HOME/.codex/rules/$NAME.md"

# Antigravity / Gemini (real copies — includes knowledge/)
hd_copy_skill "$SKILL_SRC" "$HOME/.gemini/config/skills/$NAME"
mkdir -p "$HOME/.gemini/antigravity/skills"
hd_copy_skill "$SKILL_SRC" "$HOME/.gemini/antigravity/skills/$NAME"
hd_install_command "$CMD_SRC" "$HOME/.gemini/config/commands/$NAME.md"
mkdir -p "$HOME/.gemini/antigravity/commands"
hd_install_command "$CMD_SRC" "$HOME/.gemini/antigravity/commands/$NAME.md"
hd_install_antigravity_rules "$RULE_SRC" "$NAME"

hd_link_skill "$SKILL_SRC" "$HOME/.config/opencode/skills/$NAME"
hd_install_command "$CMD_SRC" "$HOME/.config/opencode/command/$NAME.md"

hd_link_skill "$SKILL_SRC" "$HOME/.kilo/skills/$NAME"
mkdir -p "$HOME/.config/kilo/command" "$HOME/.config/kilo/agent"
hd_install_command "$CMD_SRC" "$HOME/.config/kilo/command/$NAME.md"

# All FCD agents → common agent roots
AGENT_NAMES=(
  coding-reviewer impact-reviewer review-fix-loop
  backend-implementer frontend-implementer qa-engineer
)
for a in "${AGENT_NAMES[@]}"; do
  if [[ -f "$PLUGIN_ROOT/agents/$a.md" ]]; then
    for adir in \
      "$HOME/.config/kilo/agent" \
      "$HOME/.claude/agents" \
      "$HOME/.agents/agents" \
      "$HOME/.cursor/agents"
    do
      mkdir -p "$adir"
      cp -f "$PLUGIN_ROOT/agents/$a.md" "$adir/$a.md"
      echo "agent   $adir/$a.md"
    done
  fi
done

hd_link_skill "$SKILL_SRC" "$HOME/.kimi-code/skills/$NAME"
hd_install_command "$CMD_SRC" "$HOME/.kimi-code/commands/$NAME.md"

echo
echo "Done. Restart each agent / IDE session to pick up skills."
echo "Zed: uses ~/.agents/skills (symlink). Antigravity: re-run after plugin updates (copy freshness)."
echo "Drift check: $0 --check"
echo "GLM 5.x Coding Plan: Claude Code paths. Doctor: scripts/fcd-doctor.sh"
