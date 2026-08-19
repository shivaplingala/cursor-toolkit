#!/usr/bin/env bash
# Install Cursor Toolkit: plugins + skills + rules.
# Linux / macOS / Windows Git Bash or WSL. Not cmd.exe or PowerShell.
# Usage: bash install.sh | bash install.sh --check | bash install.sh --deps | bash install.sh --pack
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="${CURSOR_PLUGINS:-$HOME/.cursor/plugins/local}"
SKILLS="${CURSOR_SKILLS:-$HOME/.cursor/skills}"
RULES="${CURSOR_RULES:-$HOME/.cursor/rules}"

PLUGINS=(aws-diagnose fcd-v2 full-cycle-delivery global-tooling)

sync_tree() {
  local src="$1" dest="$2"
  [[ -d "$src" ]] || { echo "missing: $src" >&2; exit 1; }
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude '*.Zone.Identifier' --exclude 'graphify-out/' "$src/" "$dest/"
  else
    rm -rf "$dest"
    mkdir -p "$dest"
    cp -R "$src/." "$dest/"
  fi
}

usage() {
  cat <<EOF
Cursor Toolkit installer

  bash install.sh              install plugins, skills, rules + host links
  bash install.sh --deps       install CLIs (boto3, whisper, graphify, headroom, ruflo)
  bash install.sh --check      verify files + CLIs/MCP
  bash install.sh --pack       refresh this repo from ~/.cursor (owner)

Then reload Cursor.
EOF
}

install_plugins() {
  local name
  for name in "${PLUGINS[@]}"; do
    sync_tree "$ROOT/plugins/$name" "$DEST/$name"
    echo "plugin  $DEST/$name"
  done
}

install_skills() {
  local name src dest
  mkdir -p "$SKILLS"
  shopt -s nullglob
  for src in "$ROOT/skills"/*; do
    [[ -d "$src" ]] || continue
    name=$(basename "$src")
    [[ "$name" == "stage-mongo" ]] && continue
    dest="$SKILLS/$name"
    if [[ -L "$dest" ]]; then rm -f "$dest"; fi
    sync_tree "$src" "$dest"
    echo "skill   $dest"
  done
  shopt -u nullglob
}

install_rules() {
  mkdir -p "$RULES"
  local f
  for f in "$ROOT/rules"/*.mdc; do
    [[ -f "$f" ]] || continue
    cp -R "$f" "$RULES/$(basename "$f")"
    echo "rule    $RULES/$(basename "$f")"
  done
}

run_host_installers() {
  local fcd="$DEST/full-cycle-delivery"
  local v2="$DEST/fcd-v2"
  local gt="$DEST/global-tooling"
  [[ -f "$fcd/scripts/install-multi-agent.sh" ]] && bash "$fcd/scripts/install-multi-agent.sh"
  [[ -f "$v2/scripts/install-symlinks.sh" ]] && bash "$v2/scripts/install-symlinks.sh"
  [[ -f "$gt/scripts/install-multi-agent.sh" ]] && bash "$gt/scripts/install-multi-agent.sh"
}

run_deps() {
  bash "$ROOT/scripts/deps.sh" "$1"
}

check_install() {
  local ok=0 name
  for name in "${PLUGINS[@]}"; do
    [[ -f "$DEST/$name/.cursor-plugin/plugin.json" ]] || { echo "FAIL plugin $name"; ok=1; }
  done
  for name in grill-me grill-with-docs research-agent backend frontend qa playwright-qa; do
    [[ -f "$SKILLS/$name/SKILL.md" ]] || { echo "FAIL skill $name"; ok=1; }
  done
  [[ -f "$RULES/headroom.mdc" || -f "$RULES/cursor-global-tooling.mdc" ]] || {
    echo "WARN rules may be incomplete"
  }
  echo
  bash "$ROOT/scripts/deps.sh" --check || ok=1
  return "$ok"
}

pack_from_local() {
  local name
  mkdir -p "$ROOT/plugins" "$ROOT/skills" "$ROOT/rules"
  for name in "${PLUGINS[@]}"; do
    sync_tree "$DEST/$name" "$ROOT/plugins/$name"
  done
  for name in "$SKILLS"/*; do
    [[ -d "$name" ]] || continue
    [[ "$(basename "$name")" == "stage-mongo" ]] && continue
    if [[ -L "$name" ]]; then
      if [[ -d "$name" ]]; then
        target=$(cd "$name" && pwd -P)
      else
        target="$name"
      fi
      sync_tree "$target" "$ROOT/skills/$(basename "$name")"
    else
      sync_tree "$name" "$ROOT/skills/$(basename "$name")"
    fi
  done
  cp -R "$RULES"/*.mdc "$ROOT/rules/" 2>/dev/null || true
  echo "packed into $ROOT"
}

case "${1:-}" in
  --check) check_install ;;
  --deps)  run_deps --install ;;
  --pack)  pack_from_local ;;
  -h|--help) usage ;;
  "")
    install_plugins
    install_skills
    install_rules
    run_host_installers
    echo
    bash "$ROOT/scripts/deps.sh" --check || true
    echo
    echo "Done. Install missing CLIs with: bash install.sh --deps"
    echo "Then reload Cursor."
    ;;
  *) echo "unknown: $1" >&2; usage; exit 1 ;;
esac
