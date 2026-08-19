#!/usr/bin/env python3
"""Read Aha! API credentials from env or ~/.cursor/mcp.json."""

from __future__ import annotations

import json
import os
from pathlib import Path


def load() -> tuple[str, str]:
    token = os.environ.get("AHA_API_TOKEN")
    domain = os.environ.get("AHA_DOMAIN", "default")
    if token:
        return token, domain

    mcp_path = Path.home() / ".cursor" / "mcp.json"
    if not mcp_path.exists():
        raise SystemExit("AHA_API_TOKEN not set and ~/.cursor/mcp.json not found")

    cfg = json.loads(mcp_path.read_text())
    env = cfg.get("mcpServers", {}).get("aha-mcp", {}).get("env", {})
    token = env.get("AHA_API_TOKEN")
    domain = env.get("AHA_DOMAIN", "default")
    if not token:
        raise SystemExit("aha-mcp env missing AHA_API_TOKEN in ~/.cursor/mcp.json")
    return token, domain


def base_url(domain: str) -> str:
    return f"https://{domain}.aha.io/api/v1"
