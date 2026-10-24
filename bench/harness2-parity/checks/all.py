"""Run every harness2-parity check in-process and print one summary JSON line.

Used by scripts/bench-verify.sh and the bench-guard plugin: one process, no
result files written (runner.sh owns the recorded runs).
"""
import contextlib
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def collect():
    recs = []
    for f in sorted(os.listdir(HERE)):
        if not (f.startswith("c") and f.endswith(".py") and f[1:2].isdigit()):
            continue
        spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(HERE, f))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod.main()
        lines = [x for x in buf.getvalue().splitlines() if x.strip()]
        if lines:
            recs.append(json.loads(lines[-1]))
    return recs


def main():
    recs = collect()
    scores = [r["score"] for r in recs if r["score"] is not None]
    failed = [r["id"] for r in recs if not r["pass"]]
    weak = [r["id"] for r in recs if r["score"] is not None and r["score"] < 1.0]
    print(json.dumps({
        "total_score": round(sum(scores) / len(scores), 3) if scores else 0.0,
        "passed": len([r for r in recs if r["pass"]]),
        "failed": len(failed),
        "failed_ids": failed,
        "weak_ids": weak,
        "skipped": len(recs) - len(scores),
        "scores": scores,
        "n_checks": len(recs),
    }))


if __name__ == "__main__":
    main()
