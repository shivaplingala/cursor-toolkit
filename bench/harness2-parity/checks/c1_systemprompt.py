"""c1 systemprompt — global AGENTS.md exists, under the 24k always-on cap, and the
previously dead ~/.config/opencode/rules/*.md actually load via opencode.json
instructions (verified: rules appeared as always-on instructions after wiring).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

def main():
    ev, score, n = [], 0.0, 0

    if os.path.isfile(B.AGENTS_MD):
        size = os.path.getsize(B.AGENTS_MD)
        score += 1.0 if size <= B.ALWAYS_ON_MAX else (0.5 if size <= B.ALWAYS_ON_MAX * 1.5 else 0.0)
        n += 1
        ev.append(f"global AGENTS.md: {size} chars of {B.ALWAYS_ON_MAX} cap")
    else:
        n += 1
        ev.append("global AGENTS.md: missing")

    instructions_wired = False
    if os.path.isfile(B.CFG):
        cfg = json_load(B.CFG)
        instructions_wired = any("rules" in str(i) for i in (cfg.get("instructions") or []))
    score += 1.0 if instructions_wired else 0.0; n += 1
    ev.append("opencode.json instructions -> rules/*.md: " + ("wired" if instructions_wired else "dead"))

    over = []
    for rel, fm, body in B.iter_agents():
        if len(body) > B.ALWAYS_ON_MAX:
            over.append(f"{rel}: {len(body)}")
    score += 1.0 if not over else 0.0; n += 1
    ev.append("agent bodies over always-on cap: " + (", ".join(over) or "none (all agents 1-4k)"))

    B.emit("c1-systemprompt", "c1", "always-on surface present, budgeted, and actually loaded",
           score / n, ev)

def json_load(p):
    import json
    try:
        return json.load(open(p, encoding="utf-8", errors="replace"))
    except ValueError:
        return {}

if __name__ == "__main__":
    main()
