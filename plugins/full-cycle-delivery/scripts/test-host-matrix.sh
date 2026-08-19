#!/usr/bin/env bash
# Host matrix smoke: install into a fake HOME and assert layout.
# Does not touch the real ~/.gemini or ~/.agents.
set -euo pipefail

FCD_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
V2_ROOT="${FCD_V2_ROOT:-$HOME/.cursor/plugins/local/fcd-v2}"
GT_ROOT="${GLOBAL_TOOLING_ROOT:-$HOME/.cursor/plugins/local/global-tooling}"

FAKE="$(mktemp -d "${TMPDIR:-/tmp}/fcd-host-matrix.XXXXXX")"
cleanup() { rm -rf "$FAKE"; }
trap cleanup EXIT

export HOME="$FAKE"
export FCD_PLUGIN_ROOT="$FCD_ROOT"
mkdir -p "$HOME/.cursor/skills" "$HOME/.claude/skills" "$HOME/.agents/skills" \
  "$HOME/.codex/skills" "$HOME/.kilo/skills" "$HOME/.kimi-code/skills" \
  "$HOME/.config/opencode/skills" "$HOME/.gemini/config/skills" \
  "$HOME/.gemini/antigravity/skills" "$HOME/.cursor/commands"

echo "FAKE HOME=$HOME"
bash "$FCD_ROOT/scripts/install-multi-agent.sh"
bash "$V2_ROOT/scripts/install-symlinks.sh"
bash "$GT_ROOT/scripts/install-multi-agent.sh"

fail=0
assert() {
  if [[ -e "$1" ]]; then echo "OK  $1"; else echo "MISSING $1"; fail=1; fi
}

# Zed / agents hub
for n in full-cycle-delivery fcd-v2 headroom ruflo cursor-global-tooling; do
  assert "$HOME/.agents/skills/$n/SKILL.md"
done

# Antigravity dual roots
for n in full-cycle-delivery fcd-v2 headroom ruflo cursor-global-tooling; do
  assert "$HOME/.gemini/config/skills/$n/SKILL.md"
  assert "$HOME/.gemini/antigravity/skills/$n/SKILL.md"
done

# Dual rules
for n in full-cycle-delivery fcd-v2 headroom ruflo cursor-global-tooling; do
  assert "$HOME/.gemini/config/rules/$n.mdc"
  assert "$HOME/.gemini/config/rules/$n.md"
done

assert "$HOME/.gemini/config/commands/fcd-v2.md"
assert "$HOME/.gemini/config/commands/full-cycle-delivery.md"

# --check against fake home should pass
bash "$FCD_ROOT/scripts/install-multi-agent.sh" --check
bash "$V2_ROOT/scripts/install-symlinks.sh" --check
bash "$GT_ROOT/scripts/install-multi-agent.sh" --check

if [[ $fail -ne 0 ]]; then
  echo "host-matrix FAIL"
  exit 1
fi
echo "host-matrix PASS"
