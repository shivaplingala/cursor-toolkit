"""c3 memory — always-on memory beats (read before work, evidence-schema lessons,
knowledge-capture at closeout), corpus INDEX referenced, agentmemory skills reachable.
Paper: lesson-library ablation -3.1; wrong-premises failure class blocked by evidence rows.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

def main():
    ev, score, n = [], 0.0, 0

    txt = open(B.AGENTS_MD, encoding="utf-8", errors="replace").read() \
        if os.path.isfile(B.AGENTS_MD) else ""
    mem = ""
    if txt:
        m = re.search(r"##\s*Memory\n(.*?)(?=\n## |\Z)", txt, re.S)
        mem = m.group(1) if m else ""
    score += 1.0 if mem else 0.0; n += 1
    ev.append("Memory section in always-on: " + ("present" if mem else "missing"))

    has_index = "INDEX" in mem and "knowledge" in mem.lower()
    has_schema = bool(re.search(r"cue\s*/\s*lesson\s*/\s*evidence|evidence\s*/\s*confidence", mem, re.I))
    has_closeout = bool(re.search(r"knowledge-capture|closeout", mem, re.I))
    pts = sum((has_index, has_schema, has_closeout))
    score += pts / 3.0; n += 1
    ev.append(f"memory beats: index_ref={has_index}, evidence_schema={has_schema}, "
              f"closeout_cap={has_closeout}")

    index = os.path.join(B.FCD, "knowledge", "INDEX.md")
    score += 1.0 if os.path.isfile(index) else 0.0; n += 1
    ev.append(f"corpus INDEX exists: {index if os.path.isfile(index) else 'missing'}")

    refs = B.grep_count(r"agentmemory|recall|mem0", roots=(B.CF,))[0]
    score += 1.0 if refs > 0 else 0.0; n += 1
    ev.append(f"agentmemory/recall reachable from config surface: {refs} mentions")

    B.emit("c3-memory", "c3", "memory is always-on, evidence-schema'd, and wired to agents",
           score / n, ev)

if __name__ == "__main__":
    main()
