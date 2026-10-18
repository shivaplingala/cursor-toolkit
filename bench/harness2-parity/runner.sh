#!/usr/bin/env bash
# harness2-parity runner: executes every deterministic check (checks/c*.py), aggregates
# the one-line JSON records into results/bench-results-<date>.json, prints a readable
# table. Exit code is ALWAYS 0 — a failing check is data, not an error.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DATE="$(date -u +%Y%m%d)"
RES_DIR="$HERE/results"
mkdir -p "$RES_DIR"

OUT="$RES_DIR/bench-results-$DATE.json"
SUFFIX=2
while [ -e "$OUT" ]; do
  OUT="$RES_DIR/bench-results-$DATE-$SUFFIX.json"
  SUFFIX=$((SUFFIX + 1))
done

LINES=$(mktemp)
trap 'rm -f "$LINES"' EXIT
: > "$LINES"

for f in "$HERE"/checks/c[0-9]*.py; do
  [ -f "$f" ] || continue
  id="$(basename "$f" .py)"
  if out="$(python3 "$f" 2>"$LINES.err")"; then
    printf '%s\n' "$out" | tail -1 >> "$LINES"
  else
    # a crashed check is still data; keep the slot with a low-fidelity record
    msg="$(tail -1 "$LINES.err" | cut -c1-120)"
    printf '{"id":"%s","component":"%s","desc":"check crashed","pass":false,"score":null,"evidence":["crash: %s"]}\n' \
      "$id" "${id:0:2}" "$msg" >> "$LINES"
    echo "check crashed: $id — $msg" >&2
  fi
  rm -f "$LINES.err"
done

COMPACT_OUT="$OUT" RUN_TS="$TS" python3 - "$LINES" <<'PYEOF'
import json, os, sys

lines_path, res_path = sys.argv[1], os.environ["COMPACT_OUT"]
recs = []
for line in open(lines_path, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    try:
        rec = json.loads(line)
        if isinstance(rec, dict) and "id" in rec:
            recs.append(rec)
    except json.JSONDecodeError:
        recs.append({"id": "unparseable", "component": "?", "desc": "bad json",
                     "pass": False, "score": None, "evidence": [line[:120]]})
recs.sort(key=lambda r: r["id"])

comps = sorted({r["component"] for r in recs})
scores = [r["score"] for r in recs if r["score"] is not None]
comp_avg = {c: round(sum(r["score"] for r in recs
                         if r["component"] == c and r["score"] is not None)
                     / max(1, len([r for r in recs
                                   if r["component"] == c and r["score"] is not None])), 3)
            for c in comps}
failed = [r["id"] for r in recs if not r["pass"]]
skipped = [r["id"] for r in recs if r["score"] is None]
summary = {
    "per_component_avg": comp_avg,
    "total_score": round(sum(scores) / len(scores), 3) if scores else 0.0,
    "passed": len([r for r in recs if r["pass"]]),
    "failed": len(failed),
    "skipped": len(skipped),
    "n_checks": len(recs),
    "failed_ids": failed,
    "skipped_ids": skipped,
}
doc = {"run_ts": os.environ["RUN_TS"], "runner": "harness2-parity",
       "checks": recs, "summary": summary}
with open(res_path, "w", encoding="utf-8") as fh:
    json.dump(doc, fh, indent=2)

print(f"{'COMP':4} {'CHECK':24} {'PASS':5} {'SCORE':6}")
print("-" * 44)
for r in recs:
    print(f"{r['component']:4} {r['id']:24} {str(r['pass']):5} "
          f"{'SKIP' if r['score'] is None else r['score']:6}")
print("-" * 44)
print(f"passed {summary['passed']}/{summary['n_checks']}  "
      f"failed {summary['failed']} {failed}  skipped {summary['skipped']} {skipped}")
print(f"per-component avg: {json.dumps(comp_avg)}")
print(f"TOTAL_SCORE {summary['total_score']}")
print(f"results -> {res_path}")
PYEOF
exit 0
