"""c4 tool guidance — a single centralized always-on tool-guidance surface instead of
rules duplicated across 12+ files (loopback base, serverless deploy form, no-pseudo-calls,
retry-on-error). Paper: tool-guidance edit scored 60->100; tool-error rate -20-37%.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

def main():
    ev, score, n = [], 0.0, 0

    txt = open(B.AGENTS_MD, encoding="utf-8", errors="replace").read() \
        if os.path.isfile(B.AGENTS_MD) else ""
    tg = ""
    if txt:
        m = re.search(r"##\s*Tool guidance\n(.*?)(\n## |\\Z)", txt, re.S)
        tg = m.group(1) if m else ""
    score += 1.0 if tg else 0.0; n += 1
    ev.append("centralized Tool guidance section: " + ("present" if tg else "missing"))

    rules = (r"127\.0\.0\.1:8080", r"never emit a tool call as text|pseudo", r"sst deploy --stage", r"fails twice .* change|same error", r"graphify|gitnexus")
    got = [lbl for rx, lbl in zip(rules, ("loopback-base", "no-pseudo-calls", "staged-deploy", "retry-on-error", "code-indexes")) if re.search(rx, tg, re.I)]
    score += 1.0 if len(got) >= 4 else (0.5 if got else 0.0); n += 1
    ev.append("guidance rules present: " + (", ".join(got) or "none"))

    dupes = []
    for root in (B.AG,):
        if os.path.isdir(root):
            for r, _dirs, files in os.walk(root):
                for f in files:
                    p = os.path.join(r, f)
                    if p.endswith(".md") and "127.0.0.1:8080" in open(p, encoding="utf-8", errors="replace").read():
                        dupes.append(p)
    score += 1.0 if len(dupes) <= 2 else (0.5 if len(dupes) <= 12 else 0.0); n += 1
    ev.append(f"agent files still carrying duplicated loopback prose: {len(dupes)}")

    B.emit("c4-tool-guidance", "c4", "tool rules centralized in always-on surface, deduplicated",
           score / n, ev)

if __name__ == "__main__":
    main()
