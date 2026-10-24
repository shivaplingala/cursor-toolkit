
# FCD-V2 (agent-requestable)

If the user invokes **`/fcd-v2`** or asks for **FCD-V2** / FCD+Ruflo orchestration:

1. Load skill **`fcd-v2`**
2. Keep classic **`/full-cycle-delivery`** untouched — user decides which command to use
3. Phase 4: escalate check → classic or swarm protocol
4. Always preserve FCD iron laws (grill, plan-review-fix-loop to 0, plan approval, dual review to 0, no autonomous prod)
5. Phase 2 backend design: dispatch **`backend-architect`** from FCD plugin
6. Phase 2 staff/principal: **`staff-engineering`** router + domain skill

Do not treat this rule as a reason to change FCD v1 behavior.
