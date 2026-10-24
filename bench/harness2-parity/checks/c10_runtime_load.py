"""c10 runtime load — OpenCode must actually LOAD each installed plugin.

A plugin file on disk proves nothing; the server log proves the runtime picked it up.
Skips (score null) when no log exists, per the bench convention of never crashing.
"""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B

LOADED = re.compile(r'msg="loading plugin"[^\n]*?entrypoint=file://([^\s"]+)')


def main():
    plugs = []
    if os.path.isdir(B.PLUGINS):
        plugs = [os.path.join(B.PLUGINS, f) for f in sorted(os.listdir(B.PLUGINS))
                 if f.endswith((".js", ".ts"))]
    if not plugs:
        B.emit("c10-runtime-load", "c10", "plugins are loaded by the opencode runtime",
               None, ["skipped: no installed plugins"])
        return
    if not os.path.isfile(B.LOG):
        B.emit("c10-runtime-load", "c10", "plugins are loaded by the opencode runtime",
               None, [f"skipped: no log at {B.LOG}"])
        return

    loaded, errors = set(), []
    with open(B.LOG, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            loaded.update(LOADED.findall(line))
            if "level=ERROR" in line and any(os.path.basename(p) in line for p in plugs):
                errors.append(line.strip()[:110])

    ev = []
    seen = [p for p in plugs if p in loaded]
    score = 1.0 if len(seen) == len(plugs) else (0.5 if seen else 0.0)
    n = 1
    ev.append(f"plugins seen loading in the runtime log: {len(seen)}/{len(plugs)}"
              + (f" e.g. {os.path.basename(seen[0])}" if seen else ""))

    score += 1.0 if not errors else 0.0; n += 1
    ev.append(f"plugin load errors in log: {len(errors)}"
              + (f" e.g. {errors[0]}" if errors else ""))

    B.emit("c10-runtime-load", "c10", "plugins are loaded by the opencode runtime",
           score / n, ev)


if __name__ == "__main__":
    main()
