#!/usr/bin/env python3
"""List all comments on an Aha! record (text + attachment summary; not in local aha-mcp)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aha_comments import fetch_comments, strip_html  # noqa: E402
from aha_creds import load  # noqa: E402


def summarize_comments(comments: list[dict]) -> list[dict]:
    out: list[dict] = []
    for comment in comments:
        attachments = comment.get("attachments") or []
        out.append(
            {
                "comment_id": comment.get("id"),
                "created_at": comment.get("created_at"),
                "author": (comment.get("user") or {}).get("name"),
                "body_text": strip_html(comment.get("body") or ""),
                "attachment_count": len(attachments),
                "attachments": [
                    {
                        "id": att.get("id"),
                        "file_name": att.get("file_name"),
                        "content_type": att.get("content_type"),
                    }
                    for att in attachments
                ],
            }
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", help="Aha reference, e.g. AC-717-9")
    parser.add_argument("--type", choices=("requirements", "features"), default="requirements")
    args = parser.parse_args()

    token, domain = load()
    try:
        comments = fetch_comments(token, domain, args.type, args.reference)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Aha API error {e.code}: {e.read().decode(errors='replace')}") from e

    print(
        json.dumps(
            {
                "reference": args.reference,
                "type": args.type,
                "comment_count": len(comments),
                "comments": summarize_comments(comments),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
