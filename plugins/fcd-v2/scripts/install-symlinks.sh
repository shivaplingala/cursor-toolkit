#!/usr/bin/env bash
# Host discovery for FCD-V2. Does NOT touch full-cycle-delivery tree.
# Antigravity: real skill copies + dual-shape rules. Zed: ~/.agents/skills symlink.
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
  hd_check_skill_copy "$SKILL_SRC" "$HOME/.gemini/config/skills/$NAME" || rc=1
  hd_check_skill_copy "$SKILL_SRC" "$HOME/.gemini/antigravity/skills/$NAME" || rc=1
  hd_check_file "$CMD_SRC" "$HOME/.gemini/config/commands/$NAME.md" || rc=1
  hd_check_file "$CMD_SRC" "$HOME/.claude/commands/$NAME.md" || rc=1
  hd_check_rule_dual "$RULE_SRC" "$NAME" || rc=1
  for dest in "$HOME/.cursor/skills/$NAME" "$HOME/.agents/skills/$NAME" "$HOME/.claude/skills/$NAME"; do
    hd_check_skill_link "$SKILL_SRC" "$dest" || rc=1
  done
  exit $rc
fi

hd_link_skill "$SKILL_SRC" "$HOME/.cursor/skills/$NAME"
hd_link_skill "$SKILL_SRC" "$HOME/.claude/skills/$NAME"
hd_link_skill "$SKILL_SRC" "$HOME/.agents/skills/$NAME"  # Zed + hub

[[ -d "$HOME/.codex/skills" ]] || mkdir -p "$HOME/.codex/skills"
hd_link_skill "$SKILL_SRC" "$HOME/.codex/skills/$NAME"
[[ -d "$HOME/.kilo/skills" ]] || mkdir -p "$HOME/.kilo/skills"
hd_link_skill "$SKILL_SRC" "$HOME/.kilo/skills/$NAME"
[[ -d "$HOME/.kimi-code/skills" ]] || mkdir -p "$HOME/.kimi-code/skills"
hd_link_skill "$SKILL_SRC" "$HOME/.kimi-code/skills/$NAME"
[[ -d "$HOME/.config/opencode/skills" ]] || mkdir -p "$HOME/.config/opencode/skills"
hd_link_skill "$SKILL_SRC" "$HOME/.config/opencode/skills/$NAME"

mkdir -p "$HOME/.cursor/commands" "$HOME/.claude/commands" "$HOME/.agents/commands"
hd_install_command "$CMD_SRC" "$HOME/.cursor/commands/$NAME.md"
hd_install_command "$CMD_SRC" "$HOME/.claude/commands/$NAME.md"
hd_install_command "$CMD_SRC" "$HOME/.agents/commands/$NAME.md"

mkdir -p "$HOME/.codex/prompts"
hd_install_command "$CMD_SRC" "$HOME/.codex/prompts/$NAME.md"
mkdir -p "$HOME/.config/opencode/command"
hd_install_command "$CMD_SRC" "$HOME/.config/opencode/command/$NAME.md"
mkdir -p "$HOME/.config/kilo/command"
hd_install_command "$CMD_SRC" "$HOME/.config/kilo/command/$NAME.md"
mkdir -p "$HOME/.kimi-code/commands"
hd_install_command "$CMD_SRC" "$HOME/.kimi-code/commands/$NAME.md"

hd_copy_skill "$SKILL_SRC" "$HOME/.gemini/config/skills/$NAME"
mkdir -p "$HOME/.gemini/antigravity/skills"
hd_copy_skill "$SKILL_SRC" "$HOME/.gemini/antigravity/skills/$NAME"
hd_install_command "$CMD_SRC" "$HOME/.gemini/config/commands/$NAME.md"
mkdir -p "$HOME/.gemini/antigravity/commands"
hd_install_command "$CMD_SRC" "$HOME/.gemini/antigravity/commands/$NAME.md"
hd_install_antigravity_rules "$RULE_SRC" "$NAME"

# FCD-V2 agents (orchestrator + shared implementers if present on this plugin)
AGENT_NAMES=(
  fcd-v2-orchestrator
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

echo "FCD-V2 install done. Classic FCD was not modified."
echo "Zed: ~/.agents/skills/$NAME. Antigravity: re-run after updates. Check: $0 --check"
echo "Also run FCD install-multi-agent.sh so \$FCD_ROOT knowledge/ + companions stay fresh on Gemini copies."
