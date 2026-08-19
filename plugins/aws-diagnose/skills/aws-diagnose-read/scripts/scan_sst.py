#!/usr/bin/env python3
"""Static scan of SST configs and stack files for agent infrastructure resolution."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOT = Path(__file__).resolve().parents[1]

RE_APP_NAME = re.compile(r"\bname:\s*['\"]([a-z0-9][a-z0-9-]*)['\"]")
RE_SST_FUNCTION = re.compile(
    r"new\s+sst(?:\.aws)?\.Function\(\s*['\"]([^'\"]+)['\"]", re.MULTILINE
)
RE_SST_QUEUE = re.compile(
    r"new\s+sst(?:\.aws)?\.Queue\(\s*['\"]([^'\"]+)['\"]", re.MULTILINE
)
RE_ROUTE = re.compile(r"routeKey:\s*['\"]([^'\"]+)['\"]")
RE_SSM_NAME = re.compile(r"name:\s*`([^`]+)`")
RE_HANDLER = re.compile(r"handler:\s*['\"]([^'\"]+)['\"]")
RE_STACK_IMPORT = re.compile(r"import\('\./sst/stacks/([^']+)'\)")
RE_CREATE_STACK = re.compile(r"create([A-Z][a-zA-Z]+Stack)")


@dataclass
class AppScan:
    path: str
    sst_name: str | None = None
    stacks: list[str] = field(default_factory=list)
    functions: list[dict[str, str]] = field(default_factory=list)
    queues: list[dict[str, str]] = field(default_factory=list)
    routes: list[dict[str, str]] = field(default_factory=list)
    ssm_parameters: list[dict[str, str]] = field(default_factory=list)


def _find_sst_configs(root: Path) -> list[Path]:
    return sorted(root.glob("apps/**/sst.config.ts")) + sorted(
        root.glob("infra/sst.config.ts")
    )


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _app_slug(config_path: Path) -> str:
    rel = config_path.parent.relative_to(REPO_ROOT)
    return str(rel).replace("\\", "/")


def _extract_app_name(config_text: str) -> str | None:
    for match in RE_APP_NAME.finditer(config_text):
        name = match.group(1)
        if name not in ("aws", "sst"):
            return name
    return None


def _scan_stack_file(app_path: Path, stack_file: Path, app: AppScan) -> None:
    text = _read_text(stack_file)
    rel = str(stack_file.relative_to(REPO_ROOT)).replace("\\", "/")

    for match in RE_SST_FUNCTION.finditer(text):
        entry: dict[str, str] = {
            "logical_name": match.group(1),
            "file": rel,
        }
        handler = _handler_near(text, match.start())
        if handler:
            entry["handler"] = handler
        app.functions.append(entry)

    for match in RE_SST_QUEUE.finditer(text):
        app.queues.append({"logical_name": match.group(1), "file": rel})

    for match in RE_ROUTE.finditer(text):
        app.routes.append({"route_key": match.group(1), "file": rel})

    for match in RE_SSM_NAME.finditer(text):
        app.ssm_parameters.append({"path_template": match.group(1), "file": rel})


def _handler_near(text: str, pos: int) -> str | None:
    window = text[pos : pos + 2500]
    m = RE_HANDLER.search(window)
    return m.group(1) if m else None


def _discover_stack_files(app_dir: Path, config_text: str) -> list[Path]:
    stacks_dir = app_dir / "sst" / "stacks"
    found: set[Path] = set()
    if stacks_dir.is_dir():
        found.update(stacks_dir.glob("**/*.ts"))

    for imp in RE_STACK_IMPORT.findall(config_text):
        candidate = app_dir / "sst" / "stacks" / imp
        if candidate.is_file():
            found.add(candidate)

    return sorted(found)


def scan_repo(root: Path | None = None) -> dict[str, Any]:
    """Scan all SST apps under repo root and return manifest dict."""
    root = root or REPO_ROOT
    apps: list[AppScan] = []

    for config_path in _find_sst_configs(root):
        app_dir = config_path.parent
        config_text = _read_text(config_path)
        app = AppScan(
            path=_app_slug(config_path),
            sst_name=_extract_app_name(config_text),
        )

        stack_files = _discover_stack_files(app_dir, config_text)
        app.stacks = [
            str(p.relative_to(REPO_ROOT)).replace("\\", "/") for p in stack_files
        ]

        for stack_file in stack_files:
            _scan_stack_file(app_dir, stack_file, app)

        apps.append(app)

    return {
        "repo_root": str(root),
        "app_count": len(apps),
        "apps": [asdict(a) for a in apps],
    }


def _resolve_ssm_path(template: str, stage: str, shared_stage: str | None = None) -> str:
    shared = shared_stage or stage
    out = template.replace("${sharedStage}", shared).replace("${stage}", stage)
    if "${" in out:
        out = re.sub(r"\$\{[^}]+\}", stage, out)
    return out


def _shared_stage_hint(stage: str) -> str:
    """ponytail: mirrors getSharedResourceStage — personal dev-* → dev."""
    if stage.startswith("dev-") and stage != "dev":
        return "dev"
    return stage


def _log_group_hint(sst_name: str | None, logical_name: str, stage: str) -> str:
    prefix = (sst_name or "app").split("-")[0][:8]
    return f"/aws/lambda/{prefix}-*-{stage}-*{logical_name}*"


def query_manifest(
    manifest: dict[str, Any],
    *,
    app: str | None = None,
    topic: str | None = None,
    search: str | None = None,
    stage: str | None = None,
) -> dict[str, Any]:
    """Filter manifest for agent consumption."""
    apps = manifest["apps"]
    if app:
        apps = [a for a in apps if app in a["path"] or a.get("sst_name") == app]

    shared = _shared_stage_hint(stage) if stage else None

    def match_search(item: dict[str, str], *keys: str) -> bool:
        if not search:
            return True
        hay = " ".join(str(item.get(k, "")) for k in keys).lower()
        return search.lower() in hay

    result: dict[str, Any] = {"apps": [], "stage": stage, "shared_stage": shared}

    for a in apps:
        entry: dict[str, Any] = {
            "path": a["path"],
            "sst_name": a.get("sst_name"),
            "stacks": a.get("stacks", []),
        }

        if topic in (None, "lambda", "functions"):
            funcs = [f for f in a.get("functions", []) if match_search(f, "logical_name", "handler")]
            if topic == "functions":
                topic = "lambda"
            if topic == "lambda" and funcs:
                if stage:
                    for f in funcs:
                        f["log_group_hint"] = _log_group_hint(
                            a.get("sst_name"), f["logical_name"], stage
                        )
                entry["functions"] = funcs

        if topic in (None, "queue", "queues"):
            queues = [q for q in a.get("queues", []) if match_search(q, "logical_name")]
            if queues:
                entry["queues"] = queues

        if topic in (None, "api", "routes"):
            routes = [r for r in a.get("routes", []) if match_search(r, "route_key")]
            if routes:
                entry["routes"] = routes

        if topic in (None, "ssm"):
            ssms = a.get("ssm_parameters", [])
            if search:
                ssms = [s for s in ssms if match_search(s, "path_template")]
            if stage:
                for s in ssms:
                    s = dict(s)
                    s["resolved_path"] = _resolve_ssm_path(
                        s["path_template"], stage, shared
                    )
                    entry.setdefault("ssm_parameters", []).append(s)
            elif ssms:
                entry["ssm_parameters"] = ssms

        if topic == "stacks":
            entry = {"path": a["path"], "sst_name": a.get("sst_name"), "stacks": a["stacks"]}

        has_data = len(entry) > 2 or topic == "stacks"
        if has_data or topic is None:
            if topic is None or has_data:
                result["apps"].append(entry)

    if search and topic is None:
        result["apps"] = [
            e
            for e in result["apps"]
            if any(
                [
                    e.get("functions"),
                    e.get("queues"),
                    e.get("routes"),
                    e.get("ssm_parameters"),
                    search.lower() in e.get("path", "").lower(),
                    search.lower() in (e.get("sst_name") or "").lower(),
                ]
            )
        ]

    return result


def _cache_path() -> Path:
    return SKILL_ROOT / "cache" / "manifest.json"


def load_or_scan(use_cache: bool, root: Path) -> dict[str, Any]:
    cache = _cache_path()
    if use_cache and cache.is_file():
        try:
            cached = json.loads(cache.read_text())
            if cached.get("repo_root") == str(root):
                return cached
        except (json.JSONDecodeError, OSError):
            pass
    manifest = scan_repo(root)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(manifest, indent=2))
    return manifest


def main() -> int:
    p = argparse.ArgumentParser(description="Scan SST infra for agent resolution")
    p.add_argument("--repo", type=Path, default=REPO_ROOT)
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--list-apps", action="store_true")
    p.add_argument("--app", help="Filter by app path or sst name")
    p.add_argument(
        "--topic",
        choices=["lambda", "queue", "api", "ssm", "stacks", "functions", "queues", "routes"],
    )
    p.add_argument("--search", "-s", help="Substring filter")
    p.add_argument("--stage", help="Resolve SSM paths and log group hints for stage")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--refresh-cache", action="store_true")
    args = p.parse_args()

    if args.refresh_cache:
        manifest = scan_repo(args.repo)
        _cache_path().parent.mkdir(parents=True, exist_ok=True)
        _cache_path().write_text(json.dumps(manifest, indent=2))
    else:
        manifest = load_or_scan(not args.no_cache, args.repo)

    if args.list_apps:
        out = [
            {"path": a["path"], "sst_name": a.get("sst_name"), "stack_count": len(a.get("stacks", []))}
            for a in manifest["apps"]
        ]
    else:
        out = query_manifest(
            manifest,
            app=args.app,
            topic=args.topic,
            search=args.search,
            stage=args.stage,
        )

    print(json.dumps(out, indent=2 if args.json else None))
    return 0


def _self_check() -> None:
    manifest = scan_repo(REPO_ROOT)
    assert manifest["app_count"] >= 10
    conv = [a for a in manifest["apps"] if "conversation-service" in a["path"]]
    assert conv and any(f["logical_name"] == "MessagesWebSocketHandler" for f in conv[0]["functions"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        _self_check()
        print("ok")
        sys.exit(0)
    sys.exit(main())
