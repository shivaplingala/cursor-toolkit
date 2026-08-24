#!/usr/bin/env bash
# Host discovery for FCD-V2. Does NOT touch full-cycle-delivery tree.
# Usage: install-symlinks.sh [--check]
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FCD_PLUGIN="${FCD_PLUGIN_ROOT:-$HOME/.cursor/plugins/local/full-cycle-delivery}"
# shellcheck source=/dev/null
source "$FCD_PLUGIN/scripts/lib/host-discovery.sh"

SKILL_SRC="$PLUGIN_ROOT/skills/fcd-v2"
CMD_SRC="$PLUGIN_ROOT/commands/fcd-v2.md"
RULE_SRC="$PLUGIN_ROOT/rules/fcd-v2.mdc"
NAME="fcd-v2"

[[ -f "$SKILL_SRC/SKILL.md" ]] || { echo "missing skill: $SKILL_SRC" >&2; exit 1; }
[[ -f "$CMD_SRC" ]] || { echo "missing command: $CMD_SRC" >&2; exit 1; }
[[ -f "$RULE_SRC" ]] || { echo "missing rule: $RULE_SRC" >&2; exit 1; }

MODE="${1:-install}"
if [[ "$MODE" == "--check" ]]; then
  rc=0
  echo "=== CHECK $NAME ==="
  hd_check_skill_all "$SKILL_SRC" "$NAME" || rc=1
  hd_check_command_all "$CMD_SRC" "$NAME" || rc=1
  hd_check_rule_dual "$RULE_SRC" "$NAME" || rc=1
  exit $rc
fi

hd_install_skill_all "$SKILL_SRC" "$NAME"
hd_install_command_all "$CMD_SRC" "$NAME"
hd_install_rule_all "$RULE_SRC" "$NAME"

AGENT_NAMES=(
  fcd-v2-orchestrator backend-architect
  coding-reviewer impact-reviewer review-fix-loop
  backend-implementer frontend-implementer qa-engineer
)
for a in "${AGENT_NAMES[@]}"; do
  hd_install_agent_all "$PLUGIN_ROOT/agents/$a.md" "$a"
done

echo "FCD-V2 install done. Classic FCD was not modified."
echo "Check: $0 --check. Also run FCD install-multi-agent.sh for \$FCD_ROOT copies."
