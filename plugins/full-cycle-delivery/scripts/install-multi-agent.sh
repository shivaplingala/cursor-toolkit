#!/usr/bin/env bash
# Host discovery install for full-cycle-delivery across all supported editors.
# Usage: install-multi-agent.sh [--check]
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/host-discovery.sh
source "$PLUGIN_ROOT/scripts/lib/host-discovery.sh"

SKILL_SRC="$PLUGIN_ROOT/skills/full-cycle-delivery"
CMD_SRC="$PLUGIN_ROOT/commands/full-cycle-delivery.md"
RULE_SRC="$PLUGIN_ROOT/rules/full-cycle-delivery.mdc"
NAME="full-cycle-delivery"
BA_SRC="$PLUGIN_ROOT/skills/backend-architect"

[[ -f "$SKILL_SRC/SKILL.md" ]] || { echo "missing skill: $SKILL_SRC" >&2; exit 1; }
[[ -f "$CMD_SRC" ]] || { echo "missing command: $CMD_SRC" >&2; exit 1; }

MODE="${1:-install}"
if [[ "$MODE" == "--check" ]]; then
  rc=0
  echo "=== CHECK $NAME ==="
  hd_check_skill_all "$SKILL_SRC" "$NAME" || rc=1
  hd_check_command_all "$CMD_SRC" "$NAME" || rc=1
  hd_check_rule_dual "$RULE_SRC" "$NAME" || rc=1
  [[ -d "$SKILL_SRC/knowledge" ]] || { echo "CHECK FAIL missing knowledge/ in plugin"; rc=1; }
  [[ -f "$BA_SRC/SKILL.md" ]] || { echo "CHECK FAIL missing skills/backend-architect"; rc=1; }
  hd_check_skill_all "$BA_SRC" "backend-architect" || rc=1
  [[ -d "$HOME/.gemini/config/skills/$NAME/knowledge" ]] || { echo "CHECK FAIL gemini missing knowledge/"; rc=1; }
  exit $rc
fi

echo "canonical skill: $SKILL_SRC"
echo

hd_install_skill_all "$SKILL_SRC" "$NAME"
hd_install_command_all "$CMD_SRC" "$NAME"
hd_install_rule_all "$RULE_SRC" "$NAME"

# Companion skills (Phase 4). Canonical = real dirs under ~/.cursor/skills.
for companion in backend frontend qa playwright-qa grill-me grill-with-docs; do
  src="$HOME/.cursor/skills/$companion"
  if [[ -L "$src" ]]; then
    src="$(readlink -f "$src")"
  fi
  if [[ ! -d "$src" || ! -f "$src/SKILL.md" ]]; then
    echo "WARN missing companion $companion" >&2
    continue
  fi
  hd_install_skill_all "$src" "$companion"
done

if [[ -f "$BA_SRC/SKILL.md" ]]; then
  hd_install_skill_all "$BA_SRC" "backend-architect"
  echo "skill   backend-architect (Phase 2)"
else
  echo "WARN missing bundled skill: $BA_SRC" >&2
fi

AGENT_NAMES=(
  coding-reviewer impact-reviewer review-fix-loop
  backend-architect backend-implementer frontend-implementer qa-engineer
)
for a in "${AGENT_NAMES[@]}"; do
  hd_install_agent_all "$PLUGIN_ROOT/agents/$a.md" "$a"
done

echo
echo "Done. Restart each agent / IDE session to pick up skills."
echo "Hosts: Cursor, Claude Code, GLM Coding Plan (Claude paths), GLM ZCode, Codex,"
echo "  Antigravity, Zed, OpenCode, Kilo, Kimi, Qwen Code, DeepSeek Harness."
echo "Drift check: $0 --check    Doctor: scripts/fcd-doctor.sh"
echo "All plugins: scripts/install-all-hosts.sh"
