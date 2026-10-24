"""c9 install parity — the toolkit's opencode/ mirror must actually be installed live.

A plugin committed to the toolkit but never copied into ~/.config/opencode/plugins/
never loads; c8 only sees the live dir, so this check compares source against install.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B


def _listdir(path):
    return sorted(os.listdir(path)) if os.path.isdir(path) else []


def _same(a, b):
    try:
        return open(a, "rb").read() == open(b, "rb").read()
    except OSError:
        return False


def main():
    ev, score, n = [], 0.0, 0

    tk_ag = os.path.join(B.TOOLKIT_OC, "AGENTS.md")
    if os.path.isfile(tk_ag) and os.path.isfile(B.AGENTS_MD):
        same = _same(tk_ag, B.AGENTS_MD)
        score += 1.0 if same else 0.5
        ev.append("AGENTS.md mirror identical: " + ("yes" if same else "no (live differs)"))
    else:
        score += 0.0
        ev.append("AGENTS.md mirror: missing on one side")
    n += 1

    tk_plug_dir = os.path.join(B.TOOLKIT_OC, "plugins")
    tk_plugs = [f for f in _listdir(tk_plug_dir) if f.endswith((".js", ".ts"))]
    missing = [f for f in tk_plugs if not os.path.isfile(os.path.join(B.PLUGINS, f))]
    score += 1.0 if tk_plugs and not missing else (0.5 if tk_plugs else 0.0); n += 1
    ev.append(f"toolkit plugins installed live: {len(tk_plugs) - len(missing)}/{len(tk_plugs)}"
              + (f" MISSING {missing}" if missing else ""))

    present = [f for f in tk_plugs if os.path.isfile(os.path.join(B.PLUGINS, f))]
    drift = [f for f in present
             if not _same(os.path.join(tk_plug_dir, f), os.path.join(B.PLUGINS, f))]
    score += 1.0 if present and not drift else 0.0; n += 1
    ev.append(f"plugin content identical live: {len(present) - len(drift)}/{len(present)}"
              + (f" DRIFT {drift}" if drift else ""))

    tk_stems = {os.path.splitext(f)[0] for f in _listdir(os.path.join(B.TK, "rules"))}
    live_stems = {os.path.splitext(f)[0] for f in _listdir(B.LIVE_RULES[0])}
    gap = sorted(tk_stems - live_stems)
    score += 1.0 if tk_stems and not gap else (0.5 if tk_stems else 0.0); n += 1
    ev.append(f"toolkit rules live in opencode: {len(tk_stems) - len(gap)}/{len(tk_stems)}"
              + (f" MISSING {gap}" if gap else ""))

    tk_skills = _listdir(os.path.join(B.TK, "skills"))
    gap_s = [s for s in tk_skills
             if not any(os.path.isdir(os.path.join(root, s)) for root in B.OPENCODE_SKILL_ROOTS)]
    score += 1.0 if tk_skills and not gap_s else (0.5 if tk_skills else 0.0); n += 1
    ev.append(f"toolkit skills discoverable by opencode: "
              f"{len(tk_skills) - len(gap_s)}/{len(tk_skills)}"
              + (f" MISSING {gap_s}" if gap_s else ""))

    B.emit("c9-install-parity", "c9",
           "toolkit source and live opencode install agree", score / n, ev)


if __name__ == "__main__":
    main()
