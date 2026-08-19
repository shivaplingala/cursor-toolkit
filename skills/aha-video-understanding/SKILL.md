---
name: aha-video-understanding
description: >-
  Understand Aha! requirement/feature comments — read comment text first, then
  videos (video-analyzer MCP) and images (Read on local files). Local aha-mcp
  does NOT return comments or attachments. Delete all downloads and temp frames
  after understanding — nothing persists on disk. Use for Aha/AHA comment media,
  QA/DA recordings, screenshots, AC-* refs, company.aha.io.
---

# Aha! comment understanding (text + media)

**Goal:** read comment text and understand attached videos/images. **Disk policy:** download only transiently; delete everything local once understood.

## MCP tools (`~/.cursor/mcp.json`)

| Server | Use for |
|--------|---------|
| `aha-mcp` | Record/page **description** only |
| `video-analyzer` | Local `.mp4`: Whisper transcript, keyframes, OCR |

**Images:** download locally, then **Read** the file (PNG/JPEG/WebP/GIF). No extra MCP.

**Gap:** `aha-mcp` has no comments API. Always use scripts below.

## Full workflow (follow in order)

```
0. aha_list_comments.py <REF>           → read ALL comment text first
1. aha_list_comment_videos.py <REF>     → videos in comments (if any)
2. aha_list_comment_images.py <REF>     → images in comments (if any)
3. Download only what you need          → video and/or image scripts
4. Understand                           → summarize text + media for the user
5. Cleanup (mandatory)                  → delete every local file you created
```

**Step 0 is not optional.** Comments often carry requirements, QA notes, or context that attachments alone do not show (e.g. "QA / DA recording"). Read and summarize comment text even when the user only mentioned a video.

Scripts live in `scripts/` next to this `SKILL.md`. Set `SKILL_ROOT` to that folder, then:

```bash
SKILL_ROOT="<folder-containing-this-SKILL.md>"
python3 "$SKILL_ROOT/scripts/aha_list_comments.py" AC-717-9
```

### 0. List comments (text)

```bash
python3 "$SKILL_ROOT/scripts/aha_list_comments.py" AC-717-9
python3 "$SKILL_ROOT/scripts/aha_list_comments.py" AC-717 --type features
```

Output: author, date, `body_text`, attachment list per comment. Incorporate this in your summary.

### Video branch

```bash
python3 "$SKILL_ROOT/scripts/aha_list_comment_videos.py" AC-717-9
python3 "$SKILL_ROOT/scripts/aha_download_video.py" AC-717-9
```

Then `video-analyzer` → `analyze_video` with absolute `local_path` from download JSON.

For transcript-only: `get_transcript` on the same path.

### Image branch

```bash
python3 "$SKILL_ROOT/scripts/aha_list_comment_images.py" AC-717-2
python3 "$SKILL_ROOT/scripts/aha_download_images.py" AC-717-2
python3 "$SKILL_ROOT/scripts/aha_download_images.py" AC-717-2 --index 0
```

Then **Read** each `local_path`. Files land in `~/.cache/aha-images/<REF>/`.

### Report

Include for each relevant comment: author, date, **comment text**, and what attachments show (transcript/OCR/vision summary).

### Cleanup (mandatory — after step 4)

Delete **everything** you downloaded or that the tools created. Do not leave cache behind.

```bash
# Videos
rm -f "/path/from/local_path.mp4"
rmdir ~/.cache/aha-videos/AC-717-9 2>/dev/null || true

# Images (whole ref dir)
rm -rf ~/.cache/aha-images/AC-717-9

# video-analyzer keyframes (paths in analyze_video response, under /tmp/mcp-video-*)
rm -rf /tmp/mcp-video-*
```

If multiple refs were processed, clean each `~/.cache/aha-videos/<REF>/` and `~/.cache/aha-images/<REF>/`. User has limited disk — **no permanent local copies**.

## Aha REST API (when scripts are not enough)

Credentials: `AHA_API_TOKEN`, `AHA_DOMAIN` from `~/.cursor/mcp.json` → `mcpServers.aha-mcp.env`.

```
GET https://{domain}.aha.io/api/v1/requirements/{ref}/comments
GET https://{domain}.aha.io/api/v1/features/{ref}/comments
```

## Prerequisites

- `ffmpeg` on PATH
- Whisper for silent videos: `pip install --user openai-whisper`
- Node 20+ for `video-analyzer`

## Do not

- Skip reading comment text when working on a requirement
- Pass Aha `download_url` directly to video-analyzer (auth required — download first)
- Use `get_record` alone when user asked about **comments** or **recordings**
- Use YouTube-oriented MCPs for this workflow
- Leave files in `~/.cache/aha-videos/`, `~/.cache/aha-images/`, or `/tmp/mcp-video-*` after you are done

## Optional upgrade

[Remote Aha MCP](https://support.aha.io/aha-develop/integrations/mcp-server/remote-mcp-server~7611250482619899159) has broader read/write; local `aha-mcp` + these scripts remain sufficient.
