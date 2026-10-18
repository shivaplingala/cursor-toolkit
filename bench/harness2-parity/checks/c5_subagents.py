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
    n_all = sum(1 for _r, fm, _b in agents if re.search(r"^mode:\s*(all|build|plan)\s*$",
                                                        fm, re.M))
    # 1) majority of the fleet is delegable (harness2 ratio sanity)
    ratio = n_sub / max(1, len(agents))
    score += 1.0 if ratio >= 0.5 else 0.5
    n += 1
    ev.append(f"agents={len(agents)} mode:subagent={n_sub} mode:all={n_all} "
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

    # 4) subagent briefs self-contained (canonical prompt ref or explicit inputs section)
    selfc = [(rel, body) for rel, _fm, body in agents
             if re.search(r"^mode:\s*subagent\s*$", _fm, re.M)]
    sc_ok = [rel for rel, body in selfc
             if re.search(r"(?i)(canonical (prompt|skill)|inputs (the parent|provided))",
                          body)]
    score += len(sc_ok) / max(1, len(selfc))
    n += 1
    ev.append(f"mode:subagent bodies self-contained: {len(sc_ok)}/{len(selfc)} "
              + (f"e.g. {sc_ok[0]}" if sc_ok else
                 "(missing: no canonical-prompt or inputs marker)"))

    B.emit("c5-subagents", "c5",
           "subagent fleet share, thin orchestrator context, fenced read-only roles, "
           "self-contained briefs", score / n if n else None, ev)


if __name__ == "__main__":
    main()
