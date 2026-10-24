#!/usr/bin/env bash
# harness2-parity gate — run the bench, record a fresh result, and exit non-zero
# unless the bench is shippable. scripts/bench-gate.py is the single decision
# point: EVERY check must score 1.0 (the BENCH_THRESHOLD env, default 0.90, is a
# floor on the average on top of that). Used by the pre-commit hook and by CI.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)/bench/harness2-parity"

bash "$ROOT/runner.sh" >/dev/null || { echo "bench: runner crashed"; exit 1; }

LATEST="$(python3 - "$ROOT/results" <<'PY'
import os, sys
res_dir = sys.argv[1]
files = [os.path.join(res_dir, f) for f in os.listdir(res_dir)
         if f.startswith("bench-results-") and f.endswith(".json")]
print(max(files, key=os.path.getmtime) if files else "")
PY
)" || { echo "bench: cannot read result file"; exit 1; }
[ -n "$LATEST" ] || { echo "bench: no result file written"; exit 1; }

if python3 "$HERE/bench-gate.py" "$LATEST"; then
  exit 0
else
  echo "bench FAILED: run bash bench/harness2-parity/runner.sh and fix the weak checks"
  exit 1
fi
