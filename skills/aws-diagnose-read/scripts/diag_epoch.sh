#!/usr/bin/env bash
# Print epoch milliseconds for CloudWatch Logs time windows.
# Usage:
#   diag_epoch.sh --hours-ago N [--hours-window N]
#   diag_epoch.sh --iso-start ISO --iso-end ISO
#
# ponytail: ceiling = non-GNU date (BSD/macOS date lacks -d); upgrade path = install
# coreutils and use gdate, or set DATE_CMD=gdate.

set -euo pipefail

DATE_CMD="${DATE_CMD:-}"
if [[ -z "$DATE_CMD" ]]; then
  if command -v gdate >/dev/null 2>&1; then
    DATE_CMD=gdate
  elif date --version >/dev/null 2>&1; then
    DATE_CMD=date
  else
    echo "error: GNU date required (install coreutils / use gdate on macOS)" >&2
    exit 2
  fi
fi

hours_ago=""
hours_window="1.0"
iso_start=""
iso_end=""

usage() {
  echo "Usage: $0 --hours-ago N [--hours-window N] | --iso-start ISO --iso-end ISO" >&2
  exit 2
}

need_arg() {
  local flag="$1" value="${2:-}"
  if [[ -z "$value" ]]; then
    echo "error: ${flag} requires a value" >&2
    exit 2
  fi
  if [[ "$value" == --* ]] || [[ "$value" == -* && ! "$value" =~ ^-[0-9]+([.][0-9]+)?$ ]]; then
    echo "error: ${flag} requires a value" >&2
    exit 2
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hours-ago) need_arg "$1" "${2:-}"; hours_ago="$2"; shift 2 ;;
    --hours-window) need_arg "$1" "${2:-}"; hours_window="$2"; shift 2 ;;
    --iso-start) need_arg "$1" "${2:-}"; iso_start="$2"; shift 2 ;;
    --iso-end) need_arg "$1" "${2:-}"; iso_end="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "error: unknown arg: $1" >&2; usage ;;
  esac
done

to_epoch() {
  # Accepts ISO-8601; normalizes trailing Z for GNU date.
  local s="$1"
  if [[ "$s" == *Z ]]; then
    s="${s%Z}+00:00"
  fi
  "$DATE_CMD" -u -d "$s" +%s
}

if [[ -n "$iso_start" && -n "$iso_end" ]]; then
  start_s=$(to_epoch "$iso_start")
  end_s=$(to_epoch "$iso_end")
elif [[ -n "$hours_ago" ]]; then
  # Reject non-numeric hours (awk would coerce badly).
  if ! [[ "$hours_ago" =~ ^[0-9]+([.][0-9]+)?$ && "$hours_window" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    echo "error: --hours-ago and --hours-window must be non-negative numbers" >&2
    exit 2
  fi
  now_s=$("$DATE_CMD" -u +%s)
  secs_ago=$(awk -v h="$hours_ago" 'BEGIN { printf "%d", h * 3600 }')
  secs_win=$(awk -v h="$hours_window" 'BEGIN { printf "%d", h * 3600 }')
  end_s=$((now_s - secs_ago))
  start_s=$((end_s - secs_win))
else
  echo "error: Provide --iso-start/--iso-end or --hours-ago" >&2
  exit 2
fi

if [[ "$start_s" -gt "$end_s" ]]; then
  echo "error: start is after end (${start_s} > ${end_s})" >&2
  exit 2
fi

start_ms=$((start_s * 1000))
end_ms=$((end_s * 1000))
start_iso=$("$DATE_CMD" -u -d "@$start_s" +%Y-%m-%dT%H:%M:%S+00:00)
end_iso=$("$DATE_CMD" -u -d "@$end_s" +%Y-%m-%dT%H:%M:%S+00:00)

echo "EPOCH_START_MS=$start_ms"
echo "EPOCH_END_MS=$end_ms"
echo "# UTC ${start_iso} .. ${end_iso}"
