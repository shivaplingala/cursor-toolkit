#!/usr/bin/env bash
# Install staff-engineering skills (principal-level) to all host skill roots.
# Usage: install-staff-engineering.sh [--check]
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FCD_PLUGIN="${FCD_PLUGIN_ROOT:-$HOME/.cursor/plugins/local/full-cycle-delivery}"
SKILLS_SRC="$PLUGIN_ROOT/skills"
NAME="staff-engineering"

if [[ -f "$FCD_PLUGIN/scripts/lib/host-discovery.sh" ]]; then
  # shellcheck source=/dev/null
  source "$FCD_PLUGIN/scripts/lib/host-discovery.sh"
else
  echo "FAIL: host-discovery.sh missing at $FCD_PLUGIN" >&2
  exit 1
fi

[[ -d "$SKILLS_SRC/$NAME" ]] || { echo "missing router skill; run scripts/generate-skills.py" >&2; exit 1; }

SKILL_DIRS=()
while IFS= read -r d; do SKILL_DIRS+=("$d"); done < <(find "$SKILLS_SRC" -mindepth 1 -maxdepth 1 -type d | sort)

MODE="${1:-install}"
if [[ "$MODE" == "--check" ]]; then
  rc=0
  echo "=== CHECK $NAME (${#SKILL_DIRS[@]} skills) ==="
  for d in "${SKILL_DIRS[@]}"; do
    bn="$(basename "$d")"
    hd_check_skill_all "$d" "$bn" || rc=1
  done
  exit $rc
fi

echo "Installing ${#SKILL_DIRS[@]} staff/principal skills from $SKILLS_SRC"
for d in "${SKILL_DIRS[@]}"; do
  bn="$(basename "$d")"
  hd_install_skill_all "$d" "$bn"
done

hd_install_agent_all "$PLUGIN_ROOT/agents/staff-engineering.md" "staff-engineering"

echo "Done. Router: ~/.cursor/skills/staff-engineering/SKILL.md"
echo "Check: $0 --check"
