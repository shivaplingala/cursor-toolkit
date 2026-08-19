#!/usr/bin/env python3
"""Download a video attachment from an Aha! record comment."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aha_comments import fetch_comments  # noqa: E402
from aha_creds import load  # noqa: E402
from aha_list_comment_videos import videos_from_comments  # noqa: E402

DEFAULT_DIR = Path.home() / ".cache" / "aha-videos"


def download(token: str, url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=600) as resp, dest.open("wb") as f:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", help="Aha reference, e.g. AC-717-9")
    parser.add_argument("--type", choices=("requirements", "features"), default="requirements")
    parser.add_argument("--index", type=int, default=0, help="Video index from list (default: 0)")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DIR)
    args = parser.parse_args()

    token, domain = load()
    try:
        comments = fetch_comments(token, domain, args.type, args.reference)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Aha API error {e.code}: {e.read().decode(errors='replace')}") from e

    videos = videos_from_comments(comments)
    if not videos:
        raise SystemExit(f"No video attachments in comments on {args.reference}")
    if args.index >= len(videos):
        raise SystemExit(f"Index {args.index} out of range ({len(videos)} videos)")

    video = videos[args.index]
    name = video.get("file_name") or f"{args.reference}-{args.index}.mp4"
    dest = args.output_dir / args.reference.replace("/", "_") / name

    if dest.exists() and dest.stat().st_size > 0:
        print(json.dumps({"local_path": str(dest.resolve()), "cached": True, **video}, indent=2))
        return

    url = video.get("download_url")
    if not url:
        raise SystemExit("Attachment missing download_url")

    print(f"Downloading {name} …", file=sys.stderr)
    download(token, url, dest)
    print(json.dumps({"local_path": str(dest.resolve()), "cached": False, **video}, indent=2))


if __name__ == "__main__":
    main()
