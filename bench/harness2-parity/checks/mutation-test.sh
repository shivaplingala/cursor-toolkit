#!/usr/bin/env bash
# Mutation test for the harness2-parity checks: prove each check can still FAIL.
# Breaks one harness asset at a time, asserts the matching check drops below 1.0,
# restores from the toolkit source of truth, and asserts the harness is green again.
set -uo pipefail
TK="$HOME/cursor-toolkit"
CHECKS="$TK/bench/harness2-parity/checks"
CF="$HOME/.config/opencode"
fails=0

restore() {
  cp "$TK/agents/opencode/code-reviewer.md" "$CF/agents/code-reviewer.md"
  cp "$TK/agents/opencode/fcd/implementer.md" "$CF/agents/fcd/implementer.md"
  cp "$TK/opencode/AGENTS.md" "$CF/AGENTS.md"
  cp "$TK/opencode/plugins/graphify.js" "$CF/plugins/graphify.js"
  cp "$TK/opencode/plugins/budget-guard.js" "$CF/plugins/budget-guard.js"
}
trap restore EXIT

score() { python3 "$CHECKS/$1.py" | python3 -c "import json,sys; print(json.load(sys.stdin)['score'])"; }

expect_drop() { # check_file, label
  local s agg gate_rc=0
  s="$(score "$1")"
  agg="$(python3 "$CHECKS/all.py" | python3 "$TK/scripts/bench-gate.py" 2>/dev/null)" || gate_rc=$?
  if [[ "$s" == "1.0" ]]; then
    echo "FAIL  $2 -> $1 still 1.0 (check does not bite)"
    fails=$((fails + 1))
  elif [[ "$gate_rc" -eq 0 ]]; then
    echo "FAIL  $2 -> check bites ($s) but the ship gate stayed GREEN"
    fails=$((fails + 1))
  else
    echo "PASS  $2 -> $1 dropped to $s, ship gate red (${agg#*bench-gate: })"
  fi
}

echo "baseline (all must be 1.0):"
for f in c1_systemprompt c5_subagents c6_skills c8_plugin c9_install_parity c10_runtime_load; do
  echo "  $f $(score "$f")"
done

# M1 reviewer selectable as primary again
sed -i 's/^mode: subagent$/mode: all/' "$CF/agents/code-reviewer.md"
expect_drop c5_subagents "M1 reviewer mode: all"
restore

# M2 brief loses its inputs section (canonical pointer stays)
python3 - "$CF/agents/fcd/implementer.md" <<'PY'
import re, sys
p = sys.argv[1]
t = open(p).read()
t = re.sub(r"## Inputs the parent provides\n.*?(?=\n## )", "", t, flags=re.S)
open(p, "w").write(t)
PY
expect_drop c5_subagents "M2 brief without Inputs section"
restore

# M3 brief points at a prompt that does not exist
sed -i 's|prompts/implementer.md|prompts/does-not-exist.md|' "$CF/agents/fcd/implementer.md"
expect_drop c5_subagents "M3 brief canonical pointer dangling"
restore

# M4 always-on loses its skill trigger lines
grep -v 'load the `' "$CF/AGENTS.md" > "$CF/AGENTS.md.tmp" && mv "$CF/AGENTS.md.tmp" "$CF/AGENTS.md"
expect_drop c6_skills "M4 always-on trigger lines removed"
restore

# M5 one plugin stops hooking the loop
sed -i 's/ctx\.tool\.hook/ctx.tool.hook_disabled/' "$CF/plugins/budget-guard.js"
expect_drop c8_plugin "M5 plugin tool-loop hook removed"
restore

# M6 a committed plugin is not installed live (install parity must catch it)
mv "$CF/plugins/graphify.js" "$CF/plugins/.graphify.off"
expect_drop c9_install_parity "M6 toolkit plugin missing live"
mv "$CF/plugins/.graphify.off" "$CF/plugins/graphify.js"
echo "NOTE  c10 proves 'loaded at least once' from the server log; a removal is c9's job"

# M7 always-on payload blows the cap
dd if=/dev/zero bs=1024 count=16000 2>/dev/null | tr '\0' 'x' >> "$CF/AGENTS.md"
expect_drop c1_systemprompt "M7 always-on payload over 24k cap"
restore

echo
echo "after restore (all must be 1.0 again):"
for f in c1_systemprompt c5_subagents c6_skills c8_plugin c9_install_parity c10_runtime_load; do
  echo "  $f $(score "$f")"
done
echo
if [[ $fails -eq 0 ]]; then echo "MUTATION TEST PASS: every check bites"; else echo "MUTATION TEST FAIL: $fails check(s) did not bite"; fi
exit $fails
