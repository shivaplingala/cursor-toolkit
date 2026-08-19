#!/usr/bin/env python3
"""Download image attachments from Aha! record comments."""

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
from aha_list_comment_images import images_from_comments  # noqa: E402

DEFAULT_DIR = Path.home() / ".cache" / "aha-images"


def download(token: str, url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as f:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    return dest


def dest_name(att: dict, index: int) -> str:
    ext = ".png"
    ctype = (att.get("content_type") or "").lower()
    if "jpeg" in ctype or "jpg" in ctype:
        ext = ".jpg"
    elif "webp" in ctype:
        ext = ".webp"
    elif "gif" in ctype:
        ext = ".gif"
    return f"{att.get('attachment_id') or index}{ext}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", help="Aha reference, e.g. AC-717-2")
    parser.add_argument("--type", choices=("requirements", "features"), default="requirements")
    parser.add_argument("--index", type=int, help="Download one image by index (default: all)")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DIR)
    args = parser.parse_args()

    token, domain = load()
    try:
        comments = fetch_comments(token, domain, args.type, args.reference)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Aha API error {e.code}: {e.read().decode(errors='replace')}") from e

    images = images_from_comments(comments)
    if not images:
        raise SystemExit(f"No image attachments in comments on {args.reference}")

    indices = [args.index] if args.index is not None else range(len(images))
    out_dir = args.output_dir / args.reference.replace("/", "_")
    results = []

    for i in indices:
        if i >= len(images):
            raise SystemExit(f"Index {i} out of range ({len(images)} images)")
        img = images[i]
        name = dest_name(img, i)
        dest = out_dir / name
        if not (dest.exists() and dest.stat().st_size > 0):
            url = img.get("download_url")
            if not url:
                raise SystemExit(f"Attachment {img.get('attachment_id')} missing download_url")
            print(f"Downloading {name} …", file=sys.stderr)
            download(token, url, dest)
            cached = False
        else:
            cached = True
        results.append({"local_path": str(dest.resolve()), "cached": cached, **img})

    print(json.dumps({"reference": args.reference, "downloads": results}, indent=2))


if __name__ == "__main__":
    main()
