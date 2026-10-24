"""Shared helpers for the harness2-parity checks. Mirrors harness2's OPENCODE_SURFACE
names (always_on_max 24k, skills name-must-match, trigger lines, subagent mode, plugin dir).

Read-only: this module never writes or mutates anything.
"""
import json
import os
import re

HOME = os.path.expanduser("~")
CF = os.path.join(HOME, ".config/opencode")          # live opencode config
AG = os.path.join(CF, "agents")                      # live agents (c1/c5/c2)
CFG = os.path.join(CF, "opencode.json")              # service config (c8/gates)
TK = os.path.join(HOME, "cursor-toolkit")            # toolkit repo
CS = os.path.join(HOME, ".cursor")                   # cursor dir (skills mirror)
SKILL_ROOTS = (
    os.path.join(HOME, ".config/opencode/skills"),
    os.path.join(HOME, ".cursor/skills"),
    os.path.join(HOME, ".claude/skills"),
    os.path.join(HOME, ".agents/skills"),
    os.path.join(TK, "skills"),
)
PLUGINS = os.path.join(CF, "plugins")                # global opencode plugins dir
AGENTS_MD = os.path.join(CF, "AGENTS.md")            # global always-on rules file
FCD = os.path.join(HOME, ".cursor/plugins/local/full-cycle-delivery/"
                   "skills/full-cycle-delivery")
RULES = (os.path.join(CF, "rules"), os.path.join(TK, "rules"))
LIVE_RULES = (os.path.join(CF, "rules"),)            # the rules OpenCode actually loads
TOOLKIT_OC = os.path.join(TK, "opencode")            # toolkit source of the opencode mirror
LIVE_SKILLS = os.path.join(CF, "skills")             # opencode skill mirror
# OpenCode V2 discovery: ~/.config/opencode/skills + global compatibility roots.
OPENCODE_SKILL_ROOTS = (
    os.path.join(CF, "skills"),
    os.path.join(HOME, ".claude/skills"),
    os.path.join(HOME, ".agents/skills"),
)
LOG = os.path.join(HOME, ".local/share/opencode/log/opencode.log")
ALWAYS_ON_MAX = 24_000  # harness2 OPENCODE_SURFACE.always_on_max


def always_on_paths():
    """Files OpenCode actually loads always-on: global AGENTS.md + live rules/*.md.

    The toolkit rules/ mirror is a Cursor-flavored (.mdc) source copy, not a
    second always-on surface, so it is excluded here on purpose.
    """
    out = []
    if os.path.isfile(AGENTS_MD):
        out.append(AGENTS_MD)
    for root in LIVE_RULES:
        if os.path.isdir(root):
            out += [os.path.join(root, f) for f in sorted(os.listdir(root))
                    if f.endswith(".md")]
    return out


def fm_body(text):
    """Split markdown into (frontmatter str, body str); either may be ''. Deterministic."""
    m = re.match(r"\A\s*---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def iter_agents():
    """Yields (rel_path, frontmatter, body) for every live agent .md, deterministic order."""
    out = []
    if os.path.isdir(AG):
        for root, dirs, files in os.walk(AG):
            dirs.sort()
            for f in sorted(files):
                if not f.endswith(".md"):
                    continue
                p = os.path.join(root, f)
                t = open(p, encoding="utf-8", errors="replace").read()
                fm, body = fm_body(t)
                out.append((os.path.relpath(p, AG), fm, body))
    return out


def skill_files():
    """Yields (root_index, dir_name, frontmatter, body, text) for each SKILL.md found."""
    out = []
    for i, root in enumerate(SKILL_ROOTS):
        if not os.path.isdir(root):
            continue
        for e in sorted(os.listdir(root)):
            p = os.path.join(root, e, "SKILL.md")
            if os.path.isfile(p):
                t = open(p, encoding="utf-8", errors="replace").read()
                fm, body = fm_body(t)
                out.append((i, e, fm, body, t))
    return out


def grep_count(pattern, roots=(), flags=re.I):
    """Total count of regex matches over text files under each root dir (one pass each).
    Non-recursive file paths are allowed too. Returns (count, [(file:line, sample)]).
    """
    rx = re.compile(pattern, flags)
    total, hits = 0, []
    seen_dirs = set()
    for item in roots:
        if os.path.isfile(item):
            items = [item]
        elif os.path.isdir(item):
            if item in seen_dirs:
                continue
            seen_dirs.add(item)
            items = []
            for r, dirs, files in os.walk(item):
                if "node_modules" in r or "__pycache__" in r:
                    dirs[:] = []
                    continue
                dirs.sort()
                items += [os.path.join(r, f) for f in sorted(files)]
        else:
            continue
        for p in items:
            if not p.endswith((".md", ".mdc", ".txt", ".py", ".json", ".sh", ".ts")):
                continue
            try:
                for ln, line in enumerate(open(p, encoding="utf-8",
                                               errors="replace"), 1):
                    if rx.search(line):
                        total += 1
                        if len(hits) < 12:
                            hits.append((f"{p}:{ln}", line.strip()[:110]))
            except OSError:
                continue
    return total, hits


def emit(cid, component, desc, score, evidence):
    """Print the one-line result JSON. pass := score not None and score >= 0.5."""
    rec = {
        "id": cid,
        "component": component,
        "desc": desc,
        "pass": score is not None and score >= 0.5,
        "score": None if score is None else round(min(1.0, max(0.0, score)), 3),
        "evidence": evidence,
    }
    print(json.dumps(rec, ensure_ascii=False))
