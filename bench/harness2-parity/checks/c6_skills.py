"""c6 skills — trigger lines in the always-on surface (AGENTS.md + rules), name==dir
hygiene in every mirror, unique descriptions. harness2 prompts.py:151 calls missing
trigger lines "the most violated rule"; skills ablation is the largest paper lever (-5.3).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

def main():
    ev, score, n = [], 0.0, 0

    trig, hits = B.grep_count(r"load the `\S+` skill", roots=(B.AGENTS_MD,) + B.RULES)
    score += 1.0 if trig >= 8 else (0.5 if trig >= 3 else 0.0); n += 1
    ev.append(f"canonical trigger lines in always-on: {trig} ({hits[0][0] if hits else 'none'})")

    bad = []
    unique = {}
    for i, name, fm, body, t in B.skill_files():
        m = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not m or m.group(1).strip() != name:
            bad.append(f"root{i}/{name}: name={m.group(1).strip() if m else '(none)'}")
        d = re.search(r"^description:\s*(.+)", fm, re.M)
        unique[i * 10000 + abs(hash(name)) % 10000] = (d.group(1).strip()[:40] if d else "")
    score += 1.0 if not bad else 0.0; n += 1
    ev.append("name==dir mismatches: " + (", ".join(bad) or "none"))

    descs = {(name, d.group(1)[:60]) for i, name, fm, body, t in B.skill_files()
             for d in [re.search(r"^description:\s*(.+)", fm, re.M)] if d}
    score += 1.0 if len(descs) * 1.0 / max(1, len(list(B.skill_files()))) > 0.9 else (0.5 if descs else 0.0)
    n += 1
    ev.append(f"description+name pairs unique: {len(descs)} over {len(list(B.skill_files()))} file(s)")

    wires = B.grep_count(r"skill", roots=(B.AGENTS_MD,))[0]
    score += 1.0 if wires >= 5 else 0.0; n += 1
    ev.append(f"AGENTS.md advertises native `skill` tool usage: {wires} mentions")

    B.emit("c6-skills", "c6", "skills exist, names valid, and trigger lines advertise them",
           score / n, ev)

if __name__ == "__main__":
    main()
