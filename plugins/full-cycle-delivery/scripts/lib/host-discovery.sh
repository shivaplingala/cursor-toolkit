#!/usr/bin/env bash
# Shared host-discovery helpers for FCD / FCD-V2 / global-tooling installers.
# Source only — do not execute. Linux / macOS / Windows Git Bash (not cmd.exe).
# ADR: docs/agent-host-discovery/
#
# shellcheck shell=bash
# Usage: source "$PLUGIN_ROOT/../full-cycle-delivery/scripts/lib/host-discovery.sh"
# Or:    source "$(dirname "$0")/lib/host-discovery.sh"  (from FCD plugin)

# GNU readlink -f is missing on macOS; cmd.exe has no bash. Python realpath works everywhere we have Python.
hd_realpath() {
  local p="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$p" 2>/dev/null && return 0
  fi
  if command -v python >/dev/null 2>&1; then
    python -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$p" 2>/dev/null && return 0
  fi
  if command -v py >/dev/null 2>&1; then
    py -3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$p" 2>/dev/null && return 0
  fi
  if [[ -d "$p" ]]; then
    ( cd "$p" && pwd -P )
    return 0
  fi
  echo "$(cd "$(dirname "$p")" && pwd -P)/$(basename "$p")"
}

hd_copy_skill() {
  local src="$1" dest="$2"
  # Resolve symlink loops / point at real tree
  if [[ -L "$src" ]]; then
    src="$(hd_realpath "$src" 2>/dev/null || true)"
  fi
  if [[ -z "$src" || ! -d "$src" ]]; then
    echo "skip copy (bad src): $1" >&2
    return 1
  fi
  mkdir -p "$(dirname "$dest")"
  if [[ -L "$dest" || -f "$dest" ]]; then
    rm -f "$dest"
  fi
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete \
      --exclude 'graphify-out/' \
      --exclude '*.Zone.Identifier' \
      "$src/" "$dest/"
  else
    # ponytail: macOS/Git Bash often lack rsync; cp -R is POSIX
    rm -rf "$dest"
    mkdir -p "$dest"
    cp -R "$src/." "$dest/"
  fi
  echo "copied  $dest"
}

hd_link_skill() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  local want
  want="$(hd_realpath "$src" 2>/dev/null || echo "$src")"
  # Avoid A -> B -> A loops
  if [[ -L "$dest" ]]; then
    local cur
    cur="$(hd_realpath "$dest" 2>/dev/null || true)"
    if [[ -n "$cur" && "$cur" == "$want" ]]; then
      echo "ok link  $dest"
      return 0
    fi
    rm -f "$dest"
  elif [[ -f "$dest" && ! -s "$dest" ]]; then
    rm -f "$dest"
  elif [[ -e "$dest" ]]; then
    # If dest is a real dir that IS the canonical src, do not replace with symlink
    if [[ "$(hd_realpath "$dest" 2>/dev/null || true)" == "$want" && ! -L "$dest" ]]; then
      echo "ok dir   $dest (canonical)"
      return 0
    fi
    echo "replace $dest"
    rm -rf "$dest"
  fi
  # Never link a path to itself
  if [[ "$(hd_realpath "$(dirname "$dest")" 2>/dev/null)/$(basename "$dest")" == "$want" ]]; then
    echo "skip self-link $dest"
    return 0
  fi
  if ln -s "$src" "$dest" 2>/dev/null; then
    echo "linked  $dest -> $src"
  else
    # Windows Git Bash often cannot create symlinks without Developer Mode
    hd_copy_skill "$src" "$dest"
  fi
}

hd_install_command() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" ]] && cmp -s "$src" "$dest" 2>/dev/null; then
    echo "ok cmd  $dest"
    return 0
  fi
  # If dest is a symlink to src, leave it
  if [[ -L "$dest" ]] && [[ "$(hd_realpath "$dest" 2>/dev/null || true)" == "$(hd_realpath "$src")" ]]; then
    echo "ok cmd  $dest"
    return 0
  fi
  cp -f "$src" "$dest"
  rm -f "${dest}:Zone.Identifier" 2>/dev/null || true
  echo "cmd     $dest"
}

# Strip Cursor YAML frontmatter → plain markdown
hd_install_rule_md() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  awk '
    BEGIN { skip=0 }
    NR==1 && /^---$/ { skip=1; next }
    skip && /^---$/ { skip=0; next }
    !skip { print }
  ' "$src" > "$dest"
  echo "rule    $dest"
}

# Antigravity dual shapes: .mdc (keep frontmatter) + stripped .md (ADR 0002)
hd_install_antigravity_rules() {
  local src="$1" name="$2"
  local dest_dir="${HD_GEMINI_RULES:-$HOME/.gemini/config/rules}"
  mkdir -p "$dest_dir"
  cp -f "$src" "$dest_dir/${name}.mdc"
  rm -f "${dest_dir}/${name}.mdc:Zone.Identifier" 2>/dev/null || true
  echo "rule    $dest_dir/${name}.mdc"
  hd_install_rule_md "$src" "$dest_dir/${name}.md"
}

# Exit 0 if skill copy matches src; 1 if drift/missing. Prints status lines.
hd_check_skill_copy() {
  local src="$1"
  local dest="$2"
  local label="${3:-$2}"
  if [[ ! -d "$src" ]]; then
    echo "CHECK FAIL missing src: $src"
    return 1
  fi
  if [[ ! -d "$dest" ]]; then
    echo "CHECK FAIL missing copy: $label"
    return 1
  fi
  if diff -rq -x 'graphify-out' -x '*.Zone.Identifier' "$src" "$dest" >/dev/null 2>&1; then
    echo "CHECK ok   skill $label"
    return 0
  fi
  echo "CHECK DRIFT skill $label"
  diff -rq -x 'graphify-out' -x '*.Zone.Identifier' "$src" "$dest" || true
  return 1
}

hd_check_file() {
  local src="$1"
  local dest="$2"
  local label="${3:-$2}"
  if [[ ! -f "$src" ]]; then
    echo "CHECK FAIL missing src: $src"
    return 1
  fi
  if [[ ! -f "$dest" ]]; then
    echo "CHECK FAIL missing: $label"
    return 1
  fi
  if cmp -s "$src" "$dest" 2>/dev/null; then
    echo "CHECK ok   file $label"
    return 0
  fi
  # Commands may be copies that should match; rules .mdc should match src
  echo "CHECK DRIFT file $label"
  return 1
}

hd_check_rule_dual() {
  local src="$1" name="$2"
  local dest_dir="${HD_GEMINI_RULES:-$HOME/.gemini/config/rules}"
  local rc=0
  hd_check_file "$src" "$dest_dir/${name}.mdc" "rules/${name}.mdc" || rc=1
  if [[ ! -f "$dest_dir/${name}.md" ]]; then
    echo "CHECK FAIL missing: rules/${name}.md"
    rc=1
  elif head -n 1 "$dest_dir/${name}.md" | grep -q '^---$'; then
    echo "CHECK FAIL stripped rule still has frontmatter: rules/${name}.md"
    rc=1
  else
    echo "CHECK ok   rules/${name}.md (stripped)"
  fi
  return $rc
}

# Dest must resolve to the same tree as src (symlink OR the canonical directory itself).
hd_check_skill_link() {
  local src="$1"
  local dest="$2"
  local src_r dest_r
  src_r="$(hd_realpath "$src")"
  dest_r="$(hd_realpath "$dest" 2>/dev/null || true)"
  if [[ -n "$dest_r" && "$dest_r" == "$src_r" ]]; then
    echo "CHECK ok   link $dest"
    return 0
  fi
  if [[ -d "$dest" ]] && diff -rq -x 'graphify-out' -x '*.Zone.Identifier' "$src" "$dest" >/dev/null 2>&1; then
    echo "CHECK ok   copy $dest"
    return 0
  fi
  if [[ -d "$dest" && ! -L "$dest" ]]; then
    echo "CHECK FAIL dir (want symlink or same tree): $dest"
    return 1
  fi
  echo "CHECK FAIL link $dest"
  return 1
}
