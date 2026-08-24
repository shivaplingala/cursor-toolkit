#!/usr/bin/env bash
# Publish FCD + FCD-V2 + staff-engineering + global-tooling to all host editors.
# Usage: install-all-hosts.sh [--check]
set -euo pipefail

FCD_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
V2_ROOT="${FCD_V2_ROOT:-$HOME/.cursor/plugins/local/fcd-v2}"
STAFF_ROOT="${STAFF_ENGINEERING_ROOT:-$HOME/.cursor/plugins/local/staff-engineering}"
GT_ROOT="${GLOBAL_TOOLING_ROOT:-$HOME/.cursor/plugins/local/global-tooling}"

MODE="${1:-install}"

run_one() {
  local label="$1" script="$2"
  if [[ ! -f "$script" ]]; then
    echo "SKIP $label (missing $script)" >&2
    return 0
  fi
  echo "######## $label ########"
  bash "$script" $MODE
}

export FCD_PLUGIN_ROOT="$FCD_ROOT"
run_one "full-cycle-delivery" "$FCD_ROOT/scripts/install-multi-agent.sh"
run_one "fcd-v2" "$V2_ROOT/scripts/install-symlinks.sh"
run_one "staff-engineering" "$STAFF_ROOT/scripts/install-staff-engineering.sh"
run_one "global-tooling" "$GT_ROOT/scripts/install-multi-agent.sh"

echo
echo "All-hosts $MODE done. Reload each editor session."
