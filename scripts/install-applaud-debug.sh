#!/usr/bin/env bash
# Publish applaud-debug skill + /applaud-debug command to all host editors.
# Usage: install-applaud-debug.sh [--check]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FCD_LIB="$ROOT/plugins/full-cycle-delivery/scripts/lib/host-discovery.sh"
[[ -f "$FCD_LIB" ]] || FCD_LIB="$HOME/.cursor/plugins/local/full-cycle-delivery/scripts/lib/host-discovery.sh"
# shellcheck source=/dev/null
source "$FCD_LIB"

SKILL_SRC="$ROOT/skills/applaud-debug"
CMD_SRC="$ROOT/commands/applaud-debug.md"
NAME="applaud-debug"

[[ -f "$SKILL_SRC/SKILL.md" ]] || { echo "missing skill: $SKILL_SRC" >&2; exit 1; }
[[ -f "$CMD_SRC" ]] || { echo "missing command: $CMD_SRC" >&2; exit 1; }

MODE="${1:-install}"
if [[ "$MODE" == "--check" ]]; then
  rc=0
  echo "=== CHECK $NAME ==="
  hd_check_skill_all "$SKILL_SRC" "$NAME" || rc=1
  hd_check_command_all "$CMD_SRC" "$NAME" || rc=1
  exit $rc
fi

echo "canonical skill: $SKILL_SRC"
hd_install_skill_all "$SKILL_SRC" "$NAME"
hd_install_command_all "$CMD_SRC" "$NAME"
echo "Done. Reload each editor session to pick up /$NAME."
