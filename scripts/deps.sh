#!/usr/bin/env bash
# Check / install every CLI, library, and MCP stub that plugins + skills invoke.
# Usage: bash scripts/deps.sh [--check] [--install]
set -euo pipefail

MODE="${1:---check}"
FAIL=0
WARN=0

ok()   { printf '  OK   %s\n' "$1"; }
miss() { printf '  MISS %s\n' "$1"; FAIL=1; }
warn() { printf '  WARN %s\n' "$1"; WARN=1; }

have() { command -v "$1" >/dev/null 2>&1; }
py_mod() { python3 -c "import $1" >/dev/null 2>&1; }

pip_user() {
  echo "  pip  $1"
  python3 -m pip install --user -q "$1" \
    || python3 -m pip install --user -q --break-system-packages "$1"
}

npm_g() {
  have npm || return 1
  echo "  npm  $1"
  npm install -g "$1"
}

install_uv_tool() {
  have uv || return 1
  echo "  uv   $1"
  uv tool install --upgrade "$1" >/dev/null
}

ensure_uv() {
  have uv && return 0
  echo "  curl uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  have uv
}

try_apt() {
  local pkg="$1"
  dpkg -s "$pkg" >/dev/null 2>&1 && return 0
  sudo -n apt-get install -y "$pkg" >/dev/null 2>&1
}

mcp_keys() {
  local mcp="${HOME}/.cursor/mcp.json"
  [[ -f "$mcp" ]] || { echo ""; return; }
  python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1])).get('mcpServers',{})))" "$mcp" 2>/dev/null || true
}

mcp_has() {
  echo " $(mcp_keys) " | grep -q " $1 "
}

# Merge a server into ~/.cursor/mcp.json if missing. Never overwrites existing (tokens stay).
mcp_ensure() {
  python3 - "$1" <<'PY'
import json, os, sys
name = sys.argv[1]
path = os.path.expanduser("~/.cursor/mcp.json")
data = {"mcpServers": {}}
if os.path.isfile(path):
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data.get("mcpServers"), dict):
        data["mcpServers"] = {}
if name in data["mcpServers"]:
    print(f"  mcp  {name} (already present)")
    raise SystemExit(0)

home = os.path.expanduser("~")
whisper = os.popen("command -v whisper").read().strip()
headroom = os.popen("command -v headroom").read().strip() or "headroom"
ruflo = os.popen("command -v ruflo").read().strip() or "ruflo"
gitnexus = os.popen("command -v gitnexus").read().strip() or "gitnexus"
node = os.popen("command -v node").read().strip() or "node"

servers = {
    "headroom": {
        "command": headroom,
        "args": ["mcp", "serve"],
        "env": {"HEADROOM_TELEMETRY": "off"},
    },
    "ruflo": {
        "command": ruflo,
        "args": ["mcp", "start"],
        "cwd": os.path.join(home, ".ruflo"),
    },
    "gitnexus": {
        "command": gitnexus,
        "args": ["mcp"],
    },
    "video-analyzer": {
        "command": "npx",
        "args": ["-y", "mcp-video-analyzer"],
        "env": {
            "WHISPER_MODEL": "small",
            "WHISPER_LANGUAGE": "en",
            **({"WHISPER_BIN": whisper} if whisper else {}),
        },
    },
    "aha-mcp": {
        "command": "npx",
        "args": ["-y", "aha-mcp@latest"],
        "env": {
            "AHA_API_TOKEN": os.environ.get("AHA_API_TOKEN", ""),
            "AHA_DOMAIN": os.environ.get("AHA_DOMAIN", ""),
        },
    },
    "agentmemory": {
        "command": "npx",
        "args": ["-y", "@agentmemory/mcp"],
        "env": {
            "AGENTMEMORY_URL": os.environ.get("AGENTMEMORY_URL", "http://localhost:3111"),
            "AGENTMEMORY_TOOLS": "all",
        },
    },
}
if name not in servers:
    print(f"  skip unknown mcp {name}", file=sys.stderr)
    raise SystemExit(0)
data["mcpServers"][name] = servers[name]
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(f"  mcp  {name} added (fill env secrets if empty; reload Cursor)")
PY
}

check_core() {
  echo "=== core (file copy) ==="
  have bash || miss "bash"
  have git && ok "git" || miss "git"
  have rsync && ok "rsync" || warn "rsync (falls back to cp -a)"
  have python3 && ok "python3" || miss "python3"
  have node && ok "node            (codebase-doc-*, video-analyzer npx)" || miss "node 20+ (nvm / Node.js)"
  have npm && ok "npm" || miss "npm"
  have uv && ok "uv              (graphify, headroom)" || warn "uv (https://docs.astral.sh/uv/)"
}

check_fcd() {
  echo "=== plugin full-cycle-delivery ==="
  echo "  (skills grill-me grill-with-docs research-agent backend frontend qa playwright-qa ship in this repo)"
  have graphify && ok "graphify        (impact review)" || miss "graphify"
  mcp_has gitnexus && ok "mcp gitnexus    (impact review)" || warn "mcp gitnexus (npm i -g gitnexus; FCD impact)"
  have gh && ok "gh              (qa / to-issues)" || warn "gh (GitHub CLI)"
}

check_fcd_v2() {
  echo "=== plugin fcd-v2 ==="
  have ruflo && ok "ruflo" || miss "ruflo"
  have headroom && ok "headroom" || miss "headroom"
  mcp_has ruflo && ok "mcp ruflo" || warn "mcp ruflo"
  mcp_has headroom && ok "mcp headroom" || warn "mcp headroom"
}

check_global() {
  echo "=== plugin global-tooling ==="
  have headroom && ok "headroom" || miss "headroom (uv tool install headroom-ai)"
  have ruflo && ok "ruflo" || miss "ruflo (npm i -g ruflo)"
}

check_aws() {
  echo "=== plugin aws-diagnose + agents-* ==="
  py_mod boto3 && ok "boto3" || miss "boto3 (aws_read.py WRAP)"
  have aws && ok "aws cli" || warn "aws cli v2"
  have jq && ok "jq              (agentcore JSON)" || warn "jq"
  have agentcore && ok "agentcore >=0.9" || warn "agentcore (pip: bedrock-agentcore-starter-toolkit)"
}

check_aha() {
  echo "=== skill aha-video-understanding ==="
  have ffmpeg && ok "ffmpeg" || miss "ffmpeg"
  py_mod whisper && ok "openai-whisper" || miss "openai-whisper"
  have whisper && ok "whisper CLI" || warn "whisper on PATH (same pip package)"
  have yt-dlp && ok "yt-dlp          (video-analyzer remote URLs)" || warn "yt-dlp"
  have tesseract && ok "tesseract       (video-analyzer OCR)" || warn "tesseract-ocr"
  mcp_has aha-mcp && ok "mcp aha-mcp" || warn "mcp aha-mcp (needs AHA_API_TOKEN)"
  mcp_has video-analyzer && ok "mcp video-analyzer" || warn "mcp video-analyzer (npx mcp-video-analyzer)"
}

check_graphify() {
  echo "=== skill graphify ==="
  have graphify && ok "graphify CLI" || miss "graphify (uv tool install graphifyy)"
}

check_agentmemory() {
  echo "=== skills agentmemory-* / remember / recall / recap / forget / handoff ==="
  mcp_has agentmemory && ok "mcp agentmemory" || warn "mcp agentmemory (npx @agentmemory/mcp; optional local server :3111)"
}

check_prompt_only() {
  echo "=== prompt-only skills (no extra install; files already copied) ==="
  echo "  ponytail caveman tdd review grill-me grill-with-docs research-agent"
  echo "  backend frontend qa playwright-qa diagnose design-an-interface prototype"
  echo "  to-prd to-issues triage teach write-a-skill write-agentmemory-skill"
  echo "  request-refactor-plan improve-codebase-architecture migrate-to-shoehorn"
  echo "  ubiquitous-language zoom-out edit-article writing-* scaffold-exercises"
  echo "  setup-pre-commit (uses npx husky in the target repo, not global)"
  echo "  codebase-doc-* (need node — checked above)"
  echo "  git-guardrails-claude-code (copies a bundled hook; needs ~/.claude)"
  echo "  obsidian-vault (filesystem only)"
}

check_mcp_block() {
  echo "=== MCP registry ~/.cursor/mcp.json ==="
  if [[ ! -f "${HOME}/.cursor/mcp.json" ]]; then
    warn "no mcp.json — --deps will create stubs"
    return
  fi
  ok "mcp.json exists"
}

do_check() {
  check_core
  check_fcd
  check_fcd_v2
  check_global
  check_aws
  check_aha
  check_graphify
  check_agentmemory
  check_prompt_only
  check_mcp_block
  echo
  if [[ "$FAIL" -ne 0 ]]; then
    echo "deps: missing required items. Fix with:  bash install.sh --deps"
    return 1
  fi
  if [[ "$WARN" -ne 0 ]]; then
    echo "deps: required OK; optional WARN items above."
    return 0
  fi
  echo "deps: ALL OK"
  return 0
}

do_install() {
  echo "=== install (idempotent) ==="
  have python3 || { echo "install python3 first" >&2; exit 1; }
  ensure_uv || warn "uv install failed; pip fallback for graphify/headroom"

  have ffmpeg || try_apt ffmpeg || warn "install ffmpeg (sudo apt install ffmpeg)"
  have tesseract || try_apt tesseract-ocr || warn "install tesseract-ocr"
  have jq || try_apt jq || warn "install jq"
  have git || try_apt git || true

  py_mod boto3 || pip_user boto3
  py_mod whisper || pip_user openai-whisper
  have yt-dlp || pip_user yt-dlp || install_uv_tool yt-dlp || true
  have graphify || install_uv_tool graphifyy || pip_user graphifyy
  have headroom || install_uv_tool headroom-ai || pip_user headroom-ai
  have agentcore || pip_user bedrock-agentcore-starter-toolkit || true

  if have npm; then
    have ruflo || npm_g ruflo
    have gitnexus || npm_g gitnexus
  else
    warn "no npm — cannot install ruflo / gitnexus"
  fi

  mkdir -p "${HOME}/.ruflo"

  if have headroom; then
    headroom mcp install --force >/dev/null 2>&1 || true
  fi
  mcp_ensure headroom
  mcp_ensure ruflo
  mcp_ensure gitnexus
  mcp_ensure video-analyzer
  mcp_ensure aha-mcp
  mcp_ensure agentmemory

  echo "Install pass done. Set AHA_API_TOKEN / AHA_DOMAIN if aha-mcp env is empty."
  echo "Reload Cursor so MCP servers load."
}

case "$MODE" in
  --check) do_check ;;
  --install|--deps) do_install; echo; do_check ;;
  -h|--help) echo "bash scripts/deps.sh --check | --install" ;;
  *) echo "unknown: $MODE" >&2; exit 1 ;;
esac
