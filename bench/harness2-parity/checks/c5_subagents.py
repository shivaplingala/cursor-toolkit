"""c5 subagents — delegation structure: mode:subagent share, orchestrators keep thin
context, reviewer roles read-only, subagent briefs self-contained (harness2 c5:
sub_agents/<n>/AGENT.md needs mode: subagent + description; runs in its OWN context).
"""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchlib as B


def main():
    ev = []
    score, n = 0.0, 0
    agents = B.iter_agents()
    if not agents:
        B.emit("c5-subagents", "c5", "delegation structure", None,
               [f"missing: no agents under {B.AG}"])
        return
    n_sub = sum(1 for _r, fm, _b in agents if re.search(r"^mode:\s*subagent\s*$", fm, re.M))
    n_all = sum(1 for _r, fm, _b in agents if re.search(r"^mode:\s*all\s*$", fm, re.M))
    # delegable = can run as a child session. OpenCode V2: mode all = primary OR subagent,
    # so 'all' is delegable too (harness2's ratio lever counts delegability, not the literal word).
    delegable = [(rel, fm, body) for rel, fm, body in agents
                 if re.search(r"^mode:\s*(subagent|all)\s*$", fm, re.M)]
    # 1) majority of the fleet is delegable (harness2 ratio sanity)
    ratio = len(delegable) / max(1, len(agents))
    score += 1.0 if ratio >= 0.5 else 0.5
    n += 1
    ev.append(f"agents={len(agents)} delegable(subagent|all)={len(delegable)} "
              f"(subagent={n_sub} all={n_all}) primary-only={len(agents) - len(delegable)} "
              f"(ratio {ratio:.2f})")

    # 2) orchestrators declare thin/delegation posture (never full context)
    orch = [(rel, body) for rel, _fm, body in agents
            if rel.endswith("orchestrator.md")]
    thin = [rel for rel, body in orch if re.search(
        r"(?i)(you coordinate|delegate|dense briefs|keep .{0,20}thin|not a parallel "
        r"code monkey)", body)]
    score += 1.0 if orch and len(thin) == len(orch) else (0.5 if thin else 0.0)
    n += 1
    ev.append(f"orchestrators={len(orch)} thin-posture declarations={len(thin)} "
              + (f"e.g. {thin[0]}" if thin else
                 "(missing: none declares delegate/thin-context posture)"))

    # 3) reviewer roles read-only: edit/shell deny + no subagent spawn by default
    ro = [(rel, fm) for rel, fm, _b in agents
          if re.search(r"reviewer|spec|impact|quality|pre-ship|code-review", rel)
          and re.search(r"effect:\s*deny", fm)]
    score += 1.0 if len(ro) >= 3 else (0.5 if ro else 0.0)
    n += 1
    ev.append(f"reviewer-named agents with deny gates: {len(ro)} "
              + (f"e.g. {ro[0][0]}" if ro else "(missing: reviewers not fenced)"))

    # 4) subagent briefs self-contained: a canonical prompt/skill source AND an explicit
    #    inputs section — either one alone leaves the child session guessing.
    selfc = [(rel, body) for rel, _fm, body in delegable]
    sc_ok = [rel for rel, body in selfc
             if re.search(r"(?i)canonical (prompt|skill)", body)
             and re.search(r"(?i)inputs (the parent|provided)", body)]
    score += len(sc_ok) / max(1, len(selfc))
    n += 1
    ev.append(f"delegable briefs self-contained (canonical + inputs): "
              f"{len(sc_ok)}/{len(selfc)} "
              + (f"e.g. {sc_ok[0]}" if sc_ok else
                 "(missing: no canonical-prompt and inputs marker)"))

    # 5) the canonical pointer each brief names must actually exist — a brief pointing at
    #    a missing prompt/skill is not self-contained, it is misleading
    resolved, dangling = 0, []
    for rel, _fm, body in delegable:
        m = re.search(r"(?im)^.*canonical (prompt|skill).*$", body)
        # the path may sit on the line after the "Canonical prompt:" label
        seg = body[m.start():m.start() + 300] if m else ""
        paths = [p for p in re.findall(r"`([^`]+)`", seg) if p.startswith(("~", "/"))]
        miss = [p for p in paths if not os.path.exists(os.path.expanduser(p))]
        if m and paths and not miss:
            resolved += 1
        else:
            dangling.append(rel)
    score += resolved / max(1, len(delegable)); n += 1
    ev.append(f"brief canonical pointers resolve on disk: {resolved}/{len(delegable)}"
              + (f" dangling {dangling}" if dangling else ""))

    # 6) reviewer roles must not be selectable as the main session agent (mode: all is
    # primary-capable in OpenCode V2 — a reviewer must be mode: subagent)
    prim_rev = [rel for rel, fm, _b in agents
                if re.search(r"reviewer|spec|impact|quality|pre-ship|code-review", rel)
                and re.search(r"^mode:\s*all\s*$", fm, re.M)]
    score += 1.0 if not prim_rev else 0.0
    n += 1
    ev.append(f"reviewer agents selectable as primary (mode: all): {len(prim_rev)} "
              + (f"e.g. {prim_rev[0]}" if prim_rev else "none"))

    B.emit("c5-subagents", "c5",
           "subagent fleet share, thin orchestrator context, fenced read-only roles, "
           "self-contained briefs", score / n if n else None, ev)


if __name__ == "__main__":
    main()
