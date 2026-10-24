#!/usr/bin/env bash
# Shared host-discovery helpers for FCD / FCD-V2 / global-tooling installers.
# Source only — do not execute. ADR: docs/agent-host-discovery/
#
# shellcheck shell=bash
# Usage: source "$PLUGIN_ROOT/../full-cycle-delivery/scripts/lib/host-discovery.sh"
# Or:    source "$(dirname "$0")/lib/host-discovery.sh"  (from FCD plugin)

hd_copy_skill() {
  local src="$1" dest="$2"
  # Resolve symlink loops / point at real tree
  if [[ -L "$src" ]]; then
    src="$(readlink -f "$src" 2>/dev/null || true)"
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
  rsync -a --delete \
    --exclude 'graphify-out/' \
    --exclude '*.Zone.Identifier' \
    "$src/" "$dest/"
  echo "copied  $dest"
}

hd_link_skill() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  local want
  want="$(readlink -f "$src" 2>/dev/null || echo "$src")"
  # Avoid A -> B -> A loops
  if [[ -L "$dest" ]]; then
    local cur
    cur="$(readlink -f "$dest" 2>/dev/null || true)"
    if [[ -n "$cur" && "$cur" == "$want" ]]; then
      echo "ok link  $dest"
      return 0
    fi
    rm -f "$dest"
  elif [[ -f "$dest" && ! -s "$dest" ]]; then
    rm -f "$dest"
  elif [[ -e "$dest" ]]; then
    # If dest is a real dir that IS the canonical src, do not replace with symlink
    if [[ "$(readlink -f "$dest" 2>/dev/null || true)" == "$want" && ! -L "$dest" ]]; then
      echo "ok dir   $dest (canonical)"
      return 0
    fi
    echo "replace $dest"
    rm -rf "$dest"
  fi
  # Never link a path to itself
  if [[ "$(readlink -f "$(dirname "$dest")" 2>/dev/null)/$(basename "$dest")" == "$want" ]]; then
    echo "skip self-link $dest"
    return 0
  fi
  ln -s "$src" "$dest"
  echo "linked  $dest -> $src"
}

hd_install_command() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" ]] && cmp -s "$src" "$dest" 2>/dev/null; then
    echo "ok cmd  $dest"
    return 0
  fi
  # If dest is a symlink to src, leave it
  if [[ -L "$dest" ]] && [[ "$(readlink -f "$dest" 2>/dev/null || true)" == "$(readlink -f "$src")" ]]; then
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
  elif head -1 "$dest_dir/${name}.md" | grep -q '^---$'; then
    echo "CHECK FAIL stripped rule still has frontmatter: rules/${name}.md"
    rc=1
  else
    echo "CHECK ok   rules/${name}.md (stripped)"
  fi
  return $rc
}

# Dest must resolve to the same tree as src (symlink OR the canonical directory itself),
# or hold a content-identical copy of it (install.sh stages repo -> ~/.cursor/plugins/local
# and relinks hosts to the staged copy; both entrances must verify green).
hd_check_skill_link() {
  local src="$1"
  local dest="$2"
  local src_r dest_r
  src_r="$(readlink -f "$src")"
  dest_r="$(readlink -f "$dest" 2>/dev/null || true)"
  if [[ -n "$dest_r" && "$dest_r" == "$src_r" ]]; then
    echo "CHECK ok   link $dest"
    return 0
  fi
  if [[ -d "$dest" ]] \
    && diff -rq -x 'graphify-out' -x '*.Zone.Identifier' "$src" "$dest" >/dev/null 2>&1; then
    echo "CHECK ok   link $dest (equal copy)"
    return 0
  fi
  if [[ -d "$dest" && ! -L "$dest" ]]; then
    echo "CHECK FAIL dir (want symlink or same tree): $dest"
    return 1
  fi
  echo "CHECK FAIL link $dest"
  return 1
}

# ---------------------------------------------------------------------------
# Host catalog (user-global). ADR: docs/agent-host-discovery/docs/adr/0003-host-matrix.md
# GLM Coding Plan uses Claude Code paths. GLM ZCode uses ~/.zcode/skills.
# DeepSeek Harness also reads ~/.agents/skills (already in link roots).
# ---------------------------------------------------------------------------

hd_skill_link_roots() {
  printf '%s\n' \
    "$HOME/.cursor/skills" \
    "$HOME/.claude/skills" \
    "$HOME/.agents/skills" \
    "$HOME/.codex/skills" \
    "$HOME/.config/opencode/skills" \
    "$HOME/.kilo/skills" \
    "$HOME/.kimi-code/skills" \
    "$HOME/.qwen/skills" \
    "$HOME/.dsh/skills" \
    "$HOME/.zcode/skills" \
    "$HOME/.hermes/skills"
}

hd_skill_copy_roots() {
  printf '%s\n' \
    "$HOME/.gemini/config/skills" \
    "$HOME/.gemini/antigravity/skills"
}

hd_command_dests() {
  local name="$1"
  printf '%s\n' \
    "$HOME/.cursor/commands/${name}.md" \
    "$HOME/.claude/commands/${name}.md" \
    "$HOME/.agents/commands/${name}.md" \
    "$HOME/.codex/prompts/${name}.md" \
    "$HOME/.config/opencode/command/${name}.md" \
    "$HOME/.config/kilo/command/${name}.md" \
    "$HOME/.kimi-code/commands/${name}.md" \
    "$HOME/.qwen/commands/${name}.md" \
    "$HOME/.gemini/config/commands/${name}.md" \
    "$HOME/.gemini/antigravity/commands/${name}.md"
}

hd_rule_md_dests() {
  local name="$1"
  printf '%s\n' \
    "$HOME/.claude/rules/${name}.md" \
    "$HOME/.codex/rules/${name}.md"
}

hd_agent_dirs() {
  printf '%s\n' \
    "$HOME/.cursor/agents" \
    "$HOME/.claude/agents" \
    "$HOME/.agents/agents" \
    "$HOME/.config/kilo/agent"
}

hd_install_skill_all() {
  local src="$1" name="$2" root
  while IFS= read -r root; do
    [[ -n "$root" ]] || continue
    mkdir -p "$root"
    hd_link_skill "$src" "$root/$name"
  done <<EOF
$(hd_skill_link_roots)
EOF
  while IFS= read -r root; do
    [[ -n "$root" ]] || continue
    mkdir -p "$root"
    hd_copy_skill "$src" "$root/$name"
  done <<EOF
$(hd_skill_copy_roots)
EOF
}

hd_check_skill_all() {
  local src="$1" name="$2" root rc=0
  while IFS= read -r root; do
    [[ -n "$root" ]] || continue
    hd_check_skill_link "$src" "$root/$name" || rc=1
  done <<EOF
$(hd_skill_link_roots)
EOF
  while IFS= read -r root; do
    [[ -n "$root" ]] || continue
    hd_check_skill_copy "$src" "$root/$name" || rc=1
  done <<EOF
$(hd_skill_copy_roots)
EOF
  return $rc
}

hd_install_command_all() {
  local src="$1" name="$2" dest
  while IFS= read -r dest; do
    [[ -n "$dest" ]] || continue
    mkdir -p "$(dirname "$dest")"
    hd_install_command "$src" "$dest"
  done <<EOF
$(hd_command_dests "$name")
EOF
}

hd_check_command_all() {
  local src="$1" name="$2" dest rc=0
  while IFS= read -r dest; do
    [[ -n "$dest" ]] || continue
    hd_check_file "$src" "$dest" || rc=1
  done <<EOF
$(hd_command_dests "$name")
EOF
  return $rc
}

hd_install_rule_all() {
  local src="$1" name="$2" dest
  while IFS= read -r dest; do
    [[ -n "$dest" ]] || continue
    hd_install_rule_md "$src" "$dest"
  done <<EOF
$(hd_rule_md_dests "$name")
EOF
  mkdir -p "$HOME/.cursor/rules"
  cp -f "$src" "$HOME/.cursor/rules/${name}.mdc"
  echo "rule    $HOME/.cursor/rules/${name}.mdc"
  hd_install_antigravity_rules "$src" "$name"
}

hd_install_agent_all() {
  local src="$1" name="$2" dir
  [[ -f "$src" ]] || return 0
  while IFS= read -r dir; do
    [[ -n "$dir" ]] || continue
    mkdir -p "$dir"
    cp -f "$src" "$dir/${name}.md"
    echo "agent   $dir/${name}.md"
  done <<EOF
$(hd_agent_dirs)
EOF
}

