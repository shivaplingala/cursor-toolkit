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
    shape = "none"
    substance = 0
    shaped = []
    tool_hooks, loop_hooks = [], []
    for p in plugs:
        t = open(p, encoding="utf-8", errors="replace").read()
        # V1 hook: returned "tool.execute.after" key. V2 hook: ctx.tool.hook("execute.after").
        if re.search(r"tool\.execute\.(after|before)", t):
            hooked = True
            shape = "v1 tool.execute.*"
            tool_hooks.append(os.path.basename(p))
        elif re.search(r"\.hook\(\s*[\"']execute\.(after|before)[\"']", t):
            hooked = True
            shape = "v2 ctx.tool.hook('execute.*')"
            tool_hooks.append(os.path.basename(p))
        elif re.search(r"\.hook\(\s*[\"']", t):
            loop_hooks.append(os.path.basename(p))
        # OpenCode V2 loads a default export exposing id + setup(); anything else is a no-op.
        if re.search(r"export\s+default", t) and re.search(r"\bsetup\s*\(", t):
            shaped.append(os.path.basename(p))
        hits = sum(bool(re.search(rx, t)) for rx in
                   (r"%\s*(===|>=)\s*\d+", r"WARN|budget|retry-loop", r"error.*signature|sig", r"sessionID"))
        if hits >= 2:
            substance += 1
    score += 1.0 if plugged_against_real_api(substance) else 0.0; n += 1
    ev.append(f"hook + cap/warn logic: {substance} of {len(plugs)} plugin(s)")

    every_hooked = len(tool_hooks) + len(loop_hooks)
    score += (every_hooked / len(plugs)) if plugs else 0.0; n += 1
    ev.append(f"plugins hooking the loop: {every_hooked}/{len(plugs)}"
              + (f" (tool: {', '.join(tool_hooks) or 'none'})" if tool_hooks else "")
              + (f" (session: {', '.join(loop_hooks)})" if loop_hooks else ""))

    score += 1.0 if hooked else 0.0; n += 1
    ev.append("tool-loop hook present: " + (f"yes ({shape})" if hooked else "no"))

    score += 1.0 if len(shaped) == len(plugs) and plugs else 0.0; n += 1
    ev.append(f"loadable V2 shape (default export + setup): {len(shaped)} of {len(plugs)}"
              + (f" e.g. {shaped[0]}" if shaped else ""))

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
