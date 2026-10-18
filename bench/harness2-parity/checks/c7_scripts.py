"""c7 scripts — deterministic helpers ship and are referenced: the paired
artifact-check.py (paper case studies pair guards/skills with shipped check scripts,
43->78 and 64->100) executable + working, referenced from always-on, plus skill helpers.
"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

def main():
    ev, score, n = [], 0.0, 0

    ac = os.path.join(B.TK, "scripts", "artifact-check.py")
    ok = os.path.isfile(ac) and os.access(ac, os.X_OK)
    score += 1.0 if ok else 0.0; n += 1
    ev.append(f"artifact-check.py shipped+executable: {ac if ok else 'missing'}")

    works = False
    if ok:
        r = subprocess.run([sys.executable, ac, ac], capture_output=True, text=True, timeout=30)
        works = r.returncode == 0 and "OK" in r.stdout
    score += 1.0 if works else 0.0; n += 1
    ev.append("artifact-check runs on itself: " + ("yes" if works else "no"))

    refs = B.grep_count(r"artifact-check|fcd-doctor|stage_logs|verify-scope", roots=(B.AGENTS_MD,))[0]
    score += 1.0 if refs >= 2 else (0.5 if refs >= 1 else 0.0); n += 1
    ev.append(f"always-on references shipped scripts: {refs}")

    helpers = B.grep_count(r"#!/usr/bin/env", roots=(os.path.join(B.CS, "applaud-debug"), os.path.join(B.TK, "scripts")))[0]
    score += 1.0 if helpers >= 3 else (0.5 if helpers >= 1 else 0.0); n += 1
    ev.append(f"skill/toolkit helper scripts: {helpers}")

    B.emit("c7-scripts", "c7", "deterministic check scripts shipped, executable, referenced",
           score / n, ev)

if __name__ == "__main__":
    main()
