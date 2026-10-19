export default {
  id: "budget-guard",
  setup(ctx) {
    const calls = new Map()
    const errSigs = new Map()
    ctx.tool.hook("execute.after", (event) => {
      try {
        const input = event.input || {}
        const sid = event.sessionID || input.sessionID || input.callID || "session"
        const tool = String(event.tool || "")
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

        const status = String(event.status || "")
        if (status === "error") {
          const sig = tool + ":" + String((event.error && event.error.message) || "").slice(0, 120)
          const seen = errSigs.get(sid) || new Set()
          if (seen.has(sig)) {
            hint = `[retry-loop] same tool call failed twice with the same signature — change the approach instead of repeating it.`
          }
          seen.add(sig)
          errSigs.set(sid, seen)
        }

        if (hint) {
          if (status === "error") {
            if (event.error && typeof event.error === "object") {
              event.error.message = hint + "\n" + ((event.error && event.error.message) || "")
            }
          } else {
            const result = event.result
            if (result && typeof result === "object" && typeof result.content === "string") {
              event.result = { ...result, content: result.content + "\n" + hint }
            } else if (typeof result === "string") {
              event.result = result + "\n" + hint
            }
          }
          try {
            void ctx.app?.log?.({
              body: { service: "budget-guard", level: "warn", message: hint },
            })
          } catch {}
        }
      } catch {}
    })
    return () => {
      calls.clear()
      errSigs.clear()
    }
  },
}
