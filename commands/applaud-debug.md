---
name: applaud-debug
description: >-
  Debug and fix Applaud product bugs from an Aha ticket. Use when the user
  gives an Aha link or AC-* id, says debug this, reproduce on stage, check
  stage logs, or investigate applaud-cloud, applaud-ui-vue3, or
  applaud-serverless.
---

# /applaud-debug

Resolve `$SKILL_ROOT` in order (first existing `SKILL.md` wins):

1. Cursor: `~/.cursor/skills/applaud-debug`
2. Claude Code: `~/.claude/skills/applaud-debug`
3. Agents hub: `~/.agents/skills/applaud-debug`
4. Codex: `~/.codex/skills/applaud-debug`
5. OpenCode: `~/.config/opencode/skills/applaud-debug`

Read and follow `$SKILL_ROOT/SKILL.md` and the files it links under `references/`.

Task: $ARGUMENTS

If `$ARGUMENTS` is still the literal text "$ARGUMENTS`, take the task from the rest of the user's message. If no ticket or bug was given, ask for the Aha link or reference and stop.
