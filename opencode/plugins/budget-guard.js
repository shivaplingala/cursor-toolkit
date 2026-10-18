export const BudgetGuard = async ({ client }) => {
  const calls = new Map()
  const errSigs = new Map()
  return {
    "tool.execute.after": async (input, output) => {
      try {
        const sid = (input && (input.sessionID || input.callID)) || "session"
        const tool = String((input && input.tool) || "")
        const c = calls.get(sid) || { sinceWrite: 0, total: 0 }
        c.total++
        if (tool === "write" || tool === "edit") c.sinceWrite = 0
        else c.sinceWrite++
        calls.set(sid, c)

        let hint = null
        if (tool !== "write" && tool !== "edit" && c.sinceWrite > 0 && c.sinceWrite % 15 === 0) {
          hint = `[budget] ${c.sinceWrite} tool calls in a row with no file written. Either produce the artifact now or stop deliberating.`
        }
        if (c.total === 81 || (c.total > 80 && c.total % 40 === 0)) {
          hint = `[budget] ${c.total} total tool calls this session. Cap the loop: write the deliverable, run the paired check script, report.`
        }

        const state = (output && output.state) || null
        const status = state ? String(state.status || "") : ""
        if (status === "error") {
          const sig = tool + ":" + String((state && state.error) || "").slice(0, 120)
          const seen = errSigs.get(sid) || new Set()
          if (seen.has(sig)) {
            hint = `[retry-loop] same tool call failed twice with the same signature — change the approach instead of repeating it.`
          }
          seen.add(sig)
          errSigs.set(sid, seen)
        }

        if (hint) {
          const cur =
            (output && typeof output.output === "string" && output.output) ||
            (output && typeof output.result === "string" && output.result) ||
            ""
          if (output && typeof output.output === "string") output.output = cur + "\n" + hint
          if (output && typeof output.result === "string") output.result = cur + "\n" + hint
          try {
            await client.app.log({
              body: { service: "budget-guard", level: "warn", message: hint },
            })
          } catch {}
        }
      } catch {}
    },
  }
}
