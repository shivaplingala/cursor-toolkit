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
    hd_check_skill_copy "$SRC" "$HOME/.gemini/config/skills/$name" || rc=1
    hd_check_skill_copy "$SRC" "$HOME/.gemini/antigravity/skills/$name" || rc=1
    RULE="$PLUGIN_ROOT/rules/$name.mdc"
    [[ -f "$RULE" ]] && hd_check_rule_dual "$RULE" "$name" || rc=1
    for dest in "$HOME/.cursor/skills/$name" "$HOME/.agents/skills/$name" "$HOME/.claude/skills/$name"; do
      hd_check_skill_link "$SRC" "$dest" || rc=1
    done
  done
  for name in headroom ruflo; do
    CMD="$PLUGIN_ROOT/commands/$name.md"
    hd_check_file "$CMD" "$HOME/.gemini/config/commands/$name.md" || rc=1
  done
  exit $rc
fi

echo "plugin: $PLUGIN_ROOT"
echo

for name in "${SKILLS[@]}"; do
  SRC="$(skill_src "$name")"
  [[ -f "$SRC/SKILL.md" ]] || { echo "missing skill: $name ($SRC)" >&2; exit 1; }
  echo "=== $name ($SRC) ==="

  if [[ "$(readlink -f "$HOME/.cursor/skills/$name" 2>/dev/null || true)" != "$SRC" ]]; then
    hd_link_skill "$SRC" "$HOME/.cursor/skills/$name"
  else
    echo "ok link  $HOME/.cursor/skills/$name"
  fi

  hd_link_skill "$SRC" "$HOME/.agents/skills/$name"   # Zed + hub
  hd_link_skill "$SRC" "$HOME/.claude/skills/$name"
  hd_link_skill "$SRC" "$HOME/.codex/skills/$name"
  hd_link_skill "$SRC" "$HOME/.config/opencode/skills/$name"
  hd_link_skill "$SRC" "$HOME/.kilo/skills/$name"
  hd_link_skill "$SRC" "$HOME/.kimi-code/skills/$name"

  hd_copy_skill "$SRC" "$HOME/.gemini/config/skills/$name"
  mkdir -p "$HOME/.gemini/antigravity/skills"
  hd_copy_skill "$SRC" "$HOME/.gemini/antigravity/skills/$name"
  echo
done

for name in headroom ruflo; do
  CMD="$PLUGIN_ROOT/commands/$name.md"
  RULE="$PLUGIN_ROOT/rules/$name.mdc"
  hd_install_command "$CMD" "$HOME/.agents/commands/$name.md"
  hd_install_command "$CMD" "$HOME/.claude/commands/$name.md"
  hd_install_command "$CMD" "$HOME/.codex/prompts/$name.md"
  hd_install_command "$CMD" "$HOME/.gemini/config/commands/$name.md"
  hd_install_command "$CMD" "$HOME/.config/opencode/command/$name.md"
  mkdir -p "$HOME/.config/kilo/command"
  hd_install_command "$CMD" "$HOME/.config/kilo/command/$name.md"
  hd_install_command "$CMD" "$HOME/.kimi-code/commands/$name.md"
  if [[ -f "$RULE" ]]; then
    hd_install_rule_md "$RULE" "$HOME/.claude/rules/$name.md"
    hd_install_rule_md "$RULE" "$HOME/.codex/rules/$name.md"
  fi
done

for name in headroom ruflo cursor-global-tooling; do
  RULE="$PLUGIN_ROOT/rules/$name.mdc"
  [[ -f "$RULE" ]] || { echo "missing rule: $RULE" >&2; exit 1; }
  hd_install_antigravity_rules "$RULE" "$name"
done

echo
echo "Done. Zed: ~/.agents/skills. Check: $0 --check"
echo "Next: wire MCP where possible (see README)."
