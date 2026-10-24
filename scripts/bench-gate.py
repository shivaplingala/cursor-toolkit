#!/usr/bin/env python3
"""Single decision point for the harness2-parity gate.

Exit 0 only when the bench is shippable: every check scored exactly 1.0, every
check ran, and the average cleared BENCH_THRESHOLD (env, default 0.90). A
0.667-only-over-cap state must be exit 1, not a green average. Accepts either
the full runner result doc ({checks}) or the in-process aggregate printed by
bench/harness2-parity/checks/all.py ({scores, n_checks, skipped}).

  bench-gate.py results/latest.json   # decide on a recorded run
  python3 checks/all.py | bench-gate.py   # decide without writing a result file
"""
import json
import os
import sys

THRESHOLD = float(os.environ.get("BENCH_THRESHOLD", "0.90"))

doc = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else json.load(sys.stdin)
s = doc.get("summary") or {k: doc[k] for k in ("n_checks", "skipped") if k in doc}
scores = [c.get("score") for c in doc.get("checks", [])] if "checks" in doc \
    else doc.get("scores", [])
ran = [x for x in scores if x is not None]
n_checks = s.get("n_checks") or len(ran)
skipped = s.get("skipped", len(scores) - len(ran))
weak = sorted(r["id"] for r in doc.get("checks", []) if r.get("score") != 1.0) \
    if "checks" in doc else sorted(doc.get("weak_ids", []))
total = s.get("total_score", round(sum(ran) / len(ran), 3) if ran else 0.0)
ok = bool(ran) and len(ran) == n_checks and not weak and not skipped \
    and total >= THRESHOLD
why = []
if len(ran) != n_checks:
    why.append("checks missing/crashed")
if weak:
    why.append("below 1.0: " + ", ".join(weak))
if skipped:
    why.append("skipped")
if total < THRESHOLD:
    why.append(f"total {total} < {THRESHOLD}")
print(f"bench-gate: check-min {min(ran) if ran else 0} · total {total} · "
      + ("SHIPPABLE" if ok else "NOT shippable — " + "; ".join(why)))
sys.exit(0 if ok else 1)
