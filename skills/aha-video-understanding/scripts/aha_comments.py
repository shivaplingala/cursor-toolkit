#!/usr/bin/env python3
"""Shared Aha! comment fetch helpers."""

from __future__ import annotations

import json
import re
import urllib.request

from aha_creds import base_url


def fetch_comments(token: str, domain: str, record_type: str, reference: str) -> list[dict]:
    url = f"{base_url(domain)}/{record_type}/{reference}/comments"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    return data.get("comments", [])


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    return " ".join(text.split())


def attachment_meta(comment: dict, att: dict) -> dict:
    return {
        "comment_id": comment.get("id"),
        "comment_created_at": comment.get("created_at"),
        "comment_author": (comment.get("user") or {}).get("name"),
        "comment_body_text": strip_html(comment.get("body") or ""),
        "attachment_id": att.get("id"),
        "file_name": att.get("file_name"),
        "content_type": att.get("content_type"),
        "file_size": att.get("file_size"),
        "download_url": att.get("download_url"),
    }
