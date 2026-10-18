"""compare.py — diff two harness2-parity result files.

Usage: python3 compare.py results/bench-results-AAA.json results/bench-results-BBB.json
Prints the summary delta and, per check, the score movement (Sxx when None),
plus NEW-FAIL and NOW-PASS lists.
"""
import json
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    a = json.load(open(sys.argv[1], encoding="utf-8"))
    b = json.load(open(sys.argv[2], encoding="utf-8"))
    A = {r["id"]: r for r in a["checks"]}
    B = {r["id"]: r for r in b["checks"]}

    print(f"A = {sys.argv[1]}  ({a['summary']['total_score']})")
    print(f"B = {sys.argv[2]}  ({b['summary']['total_score']})")
    da = a["summary"]["per_component_avg"]
    db = b["summary"]["per_component_avg"]
    print("\ntotal  %.3f -> %.3f  (%+.3f)" % (
        a["summary"]["total_score"], b["summary"]["total_score"],
        b["summary"]["total_score"] - a["summary"]["total_score"]))
    print(f"{'comp':4} {'delta':8}")
    for c in sorted(set(da) | set(db)):
        print(f"{c:4} {db.get(c, 0):.3f} ({db.get(c, 0) - da.get(c, 0):+.3f})")

    def s(r):
        return "SKIP" if r["score"] is None else f"{r['score']:.3f}"

    print("\nper-check delta")
    print(f"{'check':26} {'A':7} {'B':7} {'delta':8} note")
    for cid in sorted(set(A) | set(B)):
        ra, rb = A.get(cid), B.get(cid)
        if ra is None:
            print(f"{cid:26} {'-':7} {s(rb):7} new")
            continue
        if rb is None:
            print(f"{cid:26} {s(ra):7} {'-':7} removed")
            continue
        va = ra["score"] if ra["score"] is not None else 0.0
        vb = rb["score"] if rb["score"] is not None else 0.0
        d = vb - va
        if abs(d) < 1e-9:
            continue
        note = ""
        if not ra["pass"] and rb["pass"]:
            note = "NOW-PASS"
        if ra["pass"] and not rb["pass"]:
            note = "NEW-FAIL"
        print(f"{cid:26} {s(ra):7} {s(rb):7} {d:+8.3f} {note}")

    nf = [f"{n}" for n, ra, rb in [(cid, A.get(cid), B.get(cid))
                                   for cid in sorted(A)]
          if ra and rb and ra["pass"] and not rb["pass"]]
    np_ = [f"{n}" for n, ra, rb in [(cid, A.get(cid), B.get(cid))
                                    for cid in sorted(A)]
           if ra and rb and not ra["pass"] and rb["pass"]]
    print(f"\nNEW-FAIL : {nf or 'none'}")
    print(f"NOW-PASS : {np_ or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
