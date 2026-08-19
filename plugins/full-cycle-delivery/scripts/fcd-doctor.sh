#!/usr/bin/env bash
# fcd-doctor — drift / presence check for FCD + FCD-V2 + global-tooling hosts.
# Exit 0 = healthy; 1 = drift or missing.
set -euo pipefail

FCD_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
V2_ROOT="${FCD_V2_ROOT:-$HOME/.cursor/plugins/local/fcd-v2}"
GT_ROOT="${GLOBAL_TOOLING_ROOT:-$HOME/.cursor/plugins/local/global-tooling}"

rc=0

run_check() {
  local label="$1" script="$2"
  if [[ ! -x "$script" && ! -f "$script" ]]; then
    echo "DOCTOR SKIP $label (no script: $script)"
    return 0
  fi
  echo
  echo "######## $label ########"
  if bash "$script" --check; then
    echo "DOCTOR PASS $label"
  else
    echo "DOCTOR FAIL $label"
    rc=1
  fi
}

echo "fcd-doctor — host discovery health"
run_check "full-cycle-delivery" "$FCD_ROOT/scripts/install-multi-agent.sh"
run_check "fcd-v2" "$V2_ROOT/scripts/install-symlinks.sh"
run_check "global-tooling" "$GT_ROOT/scripts/install-multi-agent.sh"

# FCD-V2 compatibility pin (files V2 expects under FCD skill)
echo
echo "######## FCD-V2 compat pin ########"
FCD_SKILL="$FCD_ROOT/skills/full-cycle-delivery"
for rel in SKILL.md playbooks/bugfix-minimal.md prompts/implementer.md prompts/coding-reviewer.md prompts/impact-reviewer.md prompts/review-fix-loop.md; do
  if [[ -f "$FCD_SKILL/$rel" ]]; then
    echo "COMPAT ok   $rel"
  else
    echo "COMPAT FAIL missing $FCD_SKILL/$rel"
    rc=1
  fi
done

echo
if [[ $rc -eq 0 ]]; then
  echo "fcd-doctor: ALL PASS"
else
  echo "fcd-doctor: FAILURES — re-run installers after updating canonical plugins"
fi
exit $rc
