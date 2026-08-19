#!/usr/bin/env python3
"""List video attachments on Aha! record comments (not exposed by local aha-mcp)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aha_comments import attachment_meta, fetch_comments, strip_html  # noqa: E402
from aha_creds import load  # noqa: E402

VIDEO_TYPES = ("video/mp4", "video/webm", "video/ogg", "video/quicktime")


def videos_from_comments(comments: list[dict]) -> list[dict]:
    out: list[dict] = []
    for comment in comments:
        for att in comment.get("attachments") or []:
            ctype = (att.get("content_type") or "").lower()
            if not ctype.startswith("video/") and ctype not in VIDEO_TYPES:
                continue
            out.append(attachment_meta(comment, att))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", help="Aha reference, e.g. AC-717-9 or AC-717")
    parser.add_argument(
        "--type",
        choices=("requirements", "features"),
        default="requirements",
        help="Record type (default: requirements)",
    )
    args = parser.parse_args()

    token, domain = load()
    try:
        comments = fetch_comments(token, domain, args.type, args.reference)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"Aha API error {e.code}: {body}") from e

    videos = videos_from_comments(comments)
    print(json.dumps({"reference": args.reference, "type": args.type, "videos": videos}, indent=2))
    if not videos:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
