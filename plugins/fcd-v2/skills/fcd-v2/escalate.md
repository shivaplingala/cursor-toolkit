# FCD-V2 — Ruflo escalate check

Run once after the plan is **human-approved**, before Phase 4 work starts.  
Announce the score and mode: `FCD-V2 Phase 4: classic` or `FCD-V2 Phase 4: swarm`.

## Stay classic (Cursor Task / single implementer)

Most of these true → **do not** open Ruflo:

- ≤ ~3 plan tasks, or tasks strictly sequential
- One workspace / few files / one hotspot
- No need for cross-session shared board
- Roles are just implement → review (FCD prompts enough)
- User did not ask for swarm / Ruflo / FCD-V2 swarm

## Escalate to swarm (≥2 required)

Count how many are true; need **≥ 2**:

1. Many **independent** tasks that can run in parallel without always sharing the same files
2. Need a **shared board** (status / locks / gaps) across agents or sessions
3. Need **cross-session** continuity (resume tomorrow from board + sidecars)
4. Multiple **live roles at once** (architect + implementer + tester coordinating)
5. User explicitly asked for swarm / Ruflo / multi-agent Phase 4

**One-liner:** If TodoWrite + Cursor Task can finish the plan, stay classic.

### Annotated examples

| Plan shape | Score signals | Mode |
| ---------- | ------------- | ---- |
| Fix one installer bug; 2 sequential tasks; smoke `--check` | (none of 1–5) | **classic** |
| Antigravity rules for 3 plugins, same helper file, sequential | sequential / shared file → not independent | **classic** |
| WhatsApp + SMS outbound in parallel after shared foundation done; board for locks | 1 + 2 (+ maybe 4) | **swarm** |
| Resume tomorrow on multi-app channel work; user said “use Ruflo swarm” | 3 + 5 | **swarm** |
| User said swarm but plan is one file rename | only 5 → score 1 | **classic** (need ≥2) |

## Hard exclusions (never swarm-only)

Even when escalate ≥ 2:

- Do not skip grill / plan approval / verify (verify-scope **or** host-tooling doctor/matrix) / coding+impact to 0
- Do not `ruflo init` in the open repo unless user asks
- Do not use Ruflo for token savings (use Headroom)
- Serial shared foundations first when later tasks depend on them (e.g. `channels/shared` before WA∥SMS apps)

## Planning assumption (tokens)

- Classic Phase 4 ≈ **1×**
- Swarm Phase 4 (protocol followed) ≈ **1.3–2.5×**
- Fat board / file fights ≈ **3×+** → stop, thin the board, re-serialize hotspots
