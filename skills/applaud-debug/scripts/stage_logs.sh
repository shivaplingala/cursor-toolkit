#!/usr/bin/env bash
# Stage applaud-cloud branch + pm2 logs. Password comes from stage-mongo. Never echo it.
# Usage: stage_logs.sh [pm2-name] [lines]
set -euo pipefail

SERVICE="${1:-}"
LINES="${2:-1000}"
HOST="${STAGE_MONGO_SSH_HOST:-172.16.1.44}"
USER_NAME="${STAGE_MONGO_SSH_USER:-mgtmp}"
PASS="${STAGE_MONGO_SSH_PASSWORD:-}"

if [[ -n "$SERVICE" && ! "$SERVICE" =~ ^[A-Za-z0-9_.:-]+$ ]]; then
  echo "pm2 name must match [A-Za-z0-9_.:-]+" >&2
  exit 2
fi
if [[ ! "$LINES" =~ ^[0-9]+$ ]]; then
  echo "lines must be a number" >&2
  exit 2
fi

if [[ -z "$PASS" ]]; then
  QUERY_SH="${HOME}/.cursor/skills/stage-mongo/scripts/query.sh"
  PASS=$(python3 -c '
import re, sys
text = open(sys.argv[1]).read()
match = re.search(r"STAGE_MONGO_SSH_PASSWORD:-([^}\"]+)", text)
print(match.group(1) if match else "", end="")
' "$QUERY_SH")
fi
if [[ -z "$PASS" ]]; then
  echo "set STAGE_MONGO_SSH_PASSWORD or install stage-mongo" >&2
  exit 2
fi

ASKPASS=$(mktemp)
chmod 700 "$ASKPASS"
trap 'rm -f "$ASKPASS"' EXIT
cat >"$ASKPASS" <<'EOF'
#!/bin/sh
printf '%s\n' "$STAGE_MONGO_SSH_PASSWORD"
EOF

export STAGE_MONGO_SSH_PASSWORD="$PASS"
export SSH_ASKPASS="$ASKPASS"
export SSH_ASKPASS_REQUIRE=force
export DISPLAY="${DISPLAY:-:0}"

# ponytail: password auth via SSH_ASKPASS; switch to a key and drop PASS when one exists
exec setsid -w ssh \
  -o StrictHostKeyChecking=accept-new \
  -o ConnectTimeout=15 \
  -o PreferredAuthentications=password,keyboard-interactive \
  -o KbdInteractiveAuthentication=yes \
  -o PubkeyAuthentication=no \
  "${USER_NAME}@${HOST}" \
  "SERVICE=$(printf '%q' "$SERVICE") LINES=$(printf '%q' "$LINES") bash -s" <<'REMOTE'
set -eu
cd workspace/applaud-cloud
echo "BRANCH=$(git rev-parse --abbrev-ref HEAD)"
git log -1 --oneline
pm2 list
if [ -n "$SERVICE" ]; then
  pm2 logs "$SERVICE" --lines "$LINES" --nostream
fi
REMOTE
