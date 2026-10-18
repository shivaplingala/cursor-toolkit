"""c2 guardrails — centralized always-on guardrails file (verify-before-dispatch,
read-only inputs, git safety, permission precedence) + the 68 static permission gates.
Paper case study: verify guardrail + check script lifted 43->78.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

SECTIONS = (
    (r"verify before reporting done|[Vv]erify before", "verify-before-dispatch"),
    (r"read[- ]only", "read-only input rule"),
    (r"git (safety|push|commit)", "git safety rule"),
    (r"precedence|last-?[wW]ins", "permission precedence documented"),
)

def main():
    ev, score, n = [], 0.0, 0

    txt = open(B.AGENTS_MD, encoding="utf-8", errors="replace").read() \
        if os.path.isfile(B.AGENTS_MD) else ""
    guard = ""
    if txt:
        m = re.search(r"##\s*Guardrails\n(.*?)(\n## |\\Z)", txt, re.S)
        guard = m.group(1) if m else ""
    score += 1.0 if guard else 0.0; n += 1
    ev.append("centralized Guardrails section: " + ("present" if guard else "missing"))

    got = [(name := rx) for rx, label in SECTIONS if re.search(rx, guard, re.I)]
    labels = [label for rx, label in SECTIONS if re.search(rx, guard, re.I)]
    score += 1.0 if len(labels) >= 3 else (0.5 if labels else 0.0); n += 1
    ev.append("guardrail rules matched: " + (", ".join(labels) or "none"))

    n_deny, n_ask = 0, 0
    for _rel, fm, _body in B.iter_agents():
        n_deny += len(re.findall(r"effect:\s*deny", fm))
        n_ask += len(re.findall(r"effect:\s*ask", fm))
    score += 1.0 if (n_deny + n_ask) >= 60 else (0.5 if (n_deny + n_ask) >= 25 else 0.0); n += 1
    ev.append(f"static gates: deny={n_deny}, ask={n_ask}")

    B.emit("c2-guardrails", "c2", "always-on guardrails centralize process rules and are backed by gates",
           score / n, ev)

if __name__ == "__main__":
    main()
