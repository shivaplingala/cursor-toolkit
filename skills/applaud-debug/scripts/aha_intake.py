#!/usr/bin/env python3
"""Aha record text, acceptance fields, history, attachment names. No token output."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

AHA_SCRIPTS = Path.home() / ".cursor" / "skills" / "aha-video-understanding" / "scripts"
sys.path.insert(0, str(AHA_SCRIPTS))
from aha_comments import strip_html  # noqa: E402
from aha_creds import base_url, load  # noqa: E402

TEXT_LIMIT = 8000
HISTORY_LIMIT = 25


def get_json(token: str, url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def as_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return strip_html(value)[:TEXT_LIMIT]
    if isinstance(value, dict):
        body = value.get("body") or value.get("html") or value.get("value") or ""
        if isinstance(body, str):
            return strip_html(body)[:TEXT_LIMIT]
        return as_text(body)
    if isinstance(value, list):
        parts = [as_text(item) for item in value]
        return "\n".join(p for p in parts if p)[:TEXT_LIMIT]
    return str(value)[:TEXT_LIMIT]


def acceptance_fields(record: dict) -> list[dict]:
    out: list[dict] = []
    for key in ("acceptance_criteria", "acceptanceCriteria"):
        if record.get(key):
            out.append({"name": key, "text": as_text(record[key])})
    for field in record.get("custom_fields") or []:
        name = str(field.get("name") or field.get("key") or "")
        if "accept" in name.lower():
            out.append({"name": name, "text": as_text(field.get("value"))})
    return out


def attachments(record: dict) -> list[dict]:
    found: list[dict] = []
    blobs = list(record.get("attachments") or [])
    desc = record.get("description")
    if isinstance(desc, dict):
        blobs.extend(desc.get("attachments") or [])
    for att in blobs:
        found.append(
            {
                "id": att.get("id"),
                "file_name": att.get("file_name"),
                "content_type": att.get("content_type"),
                "file_size": att.get("file_size"),
                "download_url": att.get("download_url"),
            }
        )
    return found


def history_rows(payload: dict) -> list[dict]:
    rows = payload.get("history") or payload.get("audit") or payload.get("audits") or []
    if isinstance(rows, dict):
        rows = rows.get("history") or []
    slim = []
    for row in rows[-HISTORY_LIMIT:]:
        user = row.get("user") or {}
        slim.append(
            {
                "created_at": row.get("created_at") or row.get("created_on"),
                "user": user.get("name") if isinstance(user, dict) else None,
                "changes": row.get("changes") or row.get("audited_changes"),
            }
        )
    return slim


def related_requirements(
    token: str, domain: str, kind: str, ref: str, record: dict
) -> tuple[dict | None, list[dict]]:
    parent = record.get("feature") or record.get("parent")
    parent_out = None
    if isinstance(parent, dict):
        parent_out = {
            "reference": parent.get("reference_num") or parent.get("reference_number"),
            "name": parent.get("name"),
        }
    blobs = list(record.get("requirements") or [])
    if kind == "features" and not blobs:
        try:
            payload = get_json(token, f"{base_url(domain)}/features/{ref}/requirements")
            blobs = payload.get("requirements") or []
        except urllib.error.HTTPError:
            blobs = []
    children = []
    for row in blobs:
        children.append(
            {
                "reference": row.get("reference_num") or row.get("reference_number"),
                "name": row.get("name"),
                "description": as_text(row.get("description"))[:1500],
            }
        )
    return parent_out, children


def load_record(token: str, domain: str, ref: str) -> tuple[str, dict]:
    base = base_url(domain)
    errors: list[str] = []
    for kind, key in (("requirements", "requirement"), ("features", "feature")):
        url = f"{base}/{kind}/{ref}"
        try:
            payload = get_json(token, url)
        except urllib.error.HTTPError as exc:
            errors.append(f"{kind} {exc.code}")
            continue
        record = payload.get(key) or payload
        return kind, record
    raise SystemExit("Aha record not found: " + ", ".join(errors))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: aha_intake.py <REF>")
    ref = sys.argv[1]
    token, domain = load()
    kind, record = load_record(token, domain, ref)
    history: list[dict] | str = []
    try:
        payload = get_json(token, f"{base_url(domain)}/{kind}/{ref}/history")
        history = history_rows(payload)
    except urllib.error.HTTPError as exc:
        history = f"history HTTP {exc.code}"
    if isinstance(history, str) or not history:
        try:
            payload = get_json(token, f"{base_url(domain)}/{kind}/{ref}/audits")
            history = history_rows(payload)
        except urllib.error.HTTPError as exc:
            if isinstance(history, str):
                history = f"{history}; audits HTTP {exc.code}"

    parent, children = related_requirements(token, domain, kind, ref, record)
    status = record.get("workflow_status") or {}
    print(
        json.dumps(
            {
                "reference": ref,
                "type": kind,
                "name": record.get("name"),
                "workflow_status": status.get("name") if isinstance(status, dict) else status,
                "description": as_text(record.get("description")),
                "parent_feature": parent,
                "requirements": children,
                "acceptance": acceptance_fields(record),
                "attachments": attachments(record),
                "history": history,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
