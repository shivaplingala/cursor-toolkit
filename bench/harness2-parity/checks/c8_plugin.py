"""c8 plugin enforcement — OpenCode conventions: ~/.config/opencode/plugins/*.js|.ts
auto-loaded at startup (docs/plugins). Substance matters: the file must hook the tool
loop (tool.execute.after/before) and implement a cap/warn rule (paper case 72->100).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

def main():
    ev, score, n = [], 0.0, 0

    plugs = []
    for base in (B.PLUGINS, os.path.join(B.CF, "plugin")):
        if os.path.isdir(base):
            plugs += [os.path.join(base, f) for f in sorted(os.listdir(base))
                      if f.endswith((".ts", ".js"))]
    score += 1.0 if plugs else 0.0; n += 1
    ev.append("plugin files: " + (", ".join(plugs) or "missing"))

    hooked = False
    substance = 0
    for p in plugs:
        t = open(p, encoding="utf-8", errors="replace").read()
        if re.search(r"tool\.execute\.(after|before)", t):
            hooked = True
        hits = sum(bool(re.search(rx, t)) for rx in
                   (r"%\s*(===|>=)\s*\d+", r"WARN|budget|retry-loop", r"error.*signature|sig", r"sessionID"))
        if hits >= 2:
            substance += 1
    score += 1.0 if plugged_against_real_api(substance) else 0.0; n += 1
    ev.append(f"hook + cap/warn logic: {substance} of {len(plugs)} plugin(s)")

    score += 1.0 if hooked else 0.0; n += 1
    ev.append("tool-loop hook present: " + ("yes" if hooked else "no"))

    gates = 0
    for _rel, fm, _body in B.iter_agents():
        gates += len(re.findall(r"effect:\s*(?:deny|ask)", fm))
    score += 1.0 if gates >= 25 else (0.5 if gates >= 10 else 0.0); n += 1
    ev.append(f"static permission gates (fallback): {gates}")

    B.emit("c8-plugin", "c8", "in-loop middleware enforcement exists and is substantive",
           score / n, ev)

def plugged_against_real_api(substance):
    return substance > 0

if __name__ == "__main__":
    main()
