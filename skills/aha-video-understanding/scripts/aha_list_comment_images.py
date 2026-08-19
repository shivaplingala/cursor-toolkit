#!/usr/bin/env python3
"""List image attachments on Aha! record comments (not exposed by local aha-mcp)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aha_comments import attachment_meta, fetch_comments  # noqa: E402
from aha_creds import load  # noqa: E402


def images_from_comments(comments: list[dict]) -> list[dict]:
    out: list[dict] = []
    for comment in comments:
        for att in comment.get("attachments") or []:
            ctype = (att.get("content_type") or "").lower()
            if not ctype.startswith("image/"):
                continue
            out.append(attachment_meta(comment, att))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", help="Aha reference, e.g. AC-717-2")
    parser.add_argument("--type", choices=("requirements", "features"), default="requirements")
    args = parser.parse_args()

    token, domain = load()
    try:
        comments = fetch_comments(token, domain, args.type, args.reference)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Aha API error {e.code}: {e.read().decode(errors='replace')}") from e

    images = images_from_comments(comments)
    print(json.dumps({"reference": args.reference, "type": args.type, "images": images}, indent=2))
    if not images:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
