#!/usr/bin/env bash
# Host discovery for headroom + ruflo + cursor-global-tooling.
# Usage: install-multi-agent.sh [--check]
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FCD_PLUGIN="${FCD_PLUGIN_ROOT:-$HOME/.cursor/plugins/local/full-cycle-delivery}"
# shellcheck source=/dev/null
source "$FCD_PLUGIN/scripts/lib/host-discovery.sh"

SKILLS=(headroom ruflo cursor-global-tooling)

skill_src() {
  local name="$1"
  local p="$PLUGIN_ROOT/skills/$name"
  if [[ -L "$p" || -d "$p" ]]; then
    readlink -f "$p"
    return
  fi
  readlink -f "$HOME/.cursor/skills/$name"
}

MODE="${1:-install}"
if [[ "$MODE" == "--check" ]]; then
  rc=0
  for name in "${SKILLS[@]}"; do
    SRC="$(skill_src "$name")"
    echo "=== CHECK $name ==="
    hd_check_skill_all "$SRC" "$name" || rc=1
    RULE="$PLUGIN_ROOT/rules/$name.mdc"
    [[ -f "$RULE" ]] && hd_check_rule_dual "$RULE" "$name" || rc=1
  done
  for name in headroom ruflo; do
    CMD="$PLUGIN_ROOT/commands/$name.md"
    hd_check_command_all "$CMD" "$name" || rc=1
  done
  exit $rc
fi

echo "plugin: $PLUGIN_ROOT"
echo

for name in "${SKILLS[@]}"; do
  SRC="$(skill_src "$name")"
  [[ -f "$SRC/SKILL.md" ]] || { echo "missing skill: $name ($SRC)" >&2; exit 1; }
  echo "=== $name ($SRC) ==="
  hd_install_skill_all "$SRC" "$name"
  echo
done

for name in headroom ruflo; do
  CMD="$PLUGIN_ROOT/commands/$name.md"
  RULE="$PLUGIN_ROOT/rules/$name.mdc"
  hd_install_command_all "$CMD" "$name"
  [[ -f "$RULE" ]] && hd_install_rule_all "$RULE" "$name"
done

for name in cursor-global-tooling; do
  RULE="$PLUGIN_ROOT/rules/$name.mdc"
  [[ -f "$RULE" ]] || { echo "missing rule: $RULE" >&2; exit 1; }
  hd_install_rule_all "$RULE" "$name"
done

echo
echo "Done. All hosts (Cursor, Claude, Codex, Antigravity, Zed, Kilo, Kimi, Qwen, DeepSeek, ZCode, OpenCode)."
echo "Check: $0 --check"
