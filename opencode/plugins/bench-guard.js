// bench-guard — tells the agent when the harness2-parity bench is red or stale.
//
// Read-only: it never writes and never blocks. It only appends one line to the
// system context so a session cannot ship harness changes against a broken
// contract unnoticed. Enforcement lives in scripts/bench-verify.sh + the
// pre-commit hook; this is the always-on prompt-independent nudge.
import { readdirSync, readFileSync, statSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"

const RESULTS = join(homedir(), "cursor-toolkit", "bench", "harness2-parity", "results")
const MIN_SCORE = 0.9
const MAX_AGE_MS = 24 * 60 * 60 * 1000

export default {
  id: "bench-guard",
  async setup(ctx) {
    const seen = new Set()
    try {
      await ctx.session.hook("context", (event) => {
        try {
          if (!event || !Array.isArray(event.system)) return
          const sid = event.sessionID || `anon-${Math.floor(Date.now() / 300000)}`
          if (seen.has(sid)) return
          seen.add(sid)
          const note = readState()
          if (note) event.system.push({ type: "text", text: note })
        } catch {}
      })
    } catch {}
  },
}

function readState() {
  let files
  try {
    files = readdirSync(RESULTS).filter((f) => f.startsWith("bench-results-") && f.endsWith(".json"))
  } catch {
    return "[bench-guard] harness2-parity has no results yet — run bash ~/cursor-toolkit/bench/harness2-parity/runner.sh before shipping harness changes."
  }
  if (!files.length) {
    return "[bench-guard] harness2-parity has never been run — run bash ~/cursor-toolkit/bench/harness2-parity/runner.sh before shipping harness changes."
  }
  const newest = files
    .map((f) => join(RESULTS, f))
    .sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs)[0]
  let doc
  try {
    doc = JSON.parse(readFileSync(newest, "utf-8"))
  } catch {
    return ""
  }
  const s = doc.summary || {}
  const ageH = Math.round((Date.now() - statSync(newest).mtimeMs) / 3600000)
  const avgs = Object.values(s.per_component_avg || {}).filter((v) => typeof v === "number")
  const red = (s.failed || 0) > 0
  const weak = avgs.length > 0 && Math.min(...avgs) < 1
  const low = typeof s.total_score === "number" && s.total_score < MIN_SCORE
  const stale = ageH * 3600000 > MAX_AGE_MS
  if (!red && !weak && !low && !stale) return ""
  const why = red
    ? `${s.failed} failed check(s) (${(s.failed_ids || []).join(", ")})`
    : weak
      ? `a check below 1.0 (weakest ${Math.min(...avgs)})`
      : low
        ? `total ${s.total_score} below ${MIN_SCORE}`
        : `last run is ${ageH}h old`
  return `[bench-guard] harness2-parity not green: ${why}. Run bash ~/cursor-toolkit/bench/harness2-parity/runner.sh and diff with compare.py before shipping harness changes.`
}
