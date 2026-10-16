# Aha intake

Local `aha-mcp` returns the record description only. Comments, history, and files need the scripts below. Credentials stay in `~/.cursor/mcp.json` (`aha-mcp` env). Never print the token.

Parse the reference from the link or text (`AC-123`, `AC-123-4`). Feature vs requirement is whichever `scripts/aha_intake.py` resolves.

```bash
SKILL=~/.cursor/skills/applaud-debug
AHA=~/.cursor/skills/aha-video-understanding
python3 "$SKILL/scripts/aha_intake.py" AC-123-4
python3 "$AHA/scripts/aha_list_comments.py" AC-123-4
# on 404, retry: --type features
```

Read, in this order:

1. Intake JSON: name, description, requirements (child requirements on a feature, parent on a requirement), acceptance criteria, workflow, record attachments, history.
2. Every comment's `body_text` (skill `aha-video-understanding` — text before media).
3. Videos in comments or on the record: that skill's download script, then `video-analyzer` `analyze_video` on the local path.
4. Images: that skill's image download, then Read the file.
5. Other files (markdown, text, pdf, logs) and URLs in the description or comments: download with the same Bearer token to `/tmp/applaud-debug-aha/<REF>/`, then Read text-like files. Skip huge binaries after noting name, type, and size.
6. Delete `/tmp/applaud-debug-aha/<REF>/`, `~/.cache/aha-videos/<REF>/`, `~/.cache/aha-images/<REF>/`, and `/tmp/mcp-video-*` once you understand them.

Write a short repro note: expected vs actual, steps, and which app the behavior lives in. Then ask if it is reproducible on stage. Do not boot local apps until that answer is in.
