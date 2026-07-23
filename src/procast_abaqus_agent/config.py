from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    source = Path(path).expanduser().resolve()
    data = json.loads(source.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {source}")
    return data


def resolve_from(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = base / candidate
    return candidate.resolve()


def check_environment(config_path: str | Path) -> dict[str, Any]:
    """Validate configured vendor/tool paths without launching any application."""
    source = Path(config_path).expanduser().resolve()
    data = load_json(source)
    if data.get("schema") != "procast_abaqus_environment_v1":
        raise ValueError("schema must be procast_abaqus_environment_v1")

    checks: list[dict[str, Any]] = []
    for group_name in ("procast", "visual_environment", "abaqus", "tools"):
        group = data.get(group_name, {})
        if not isinstance(group, dict):
            continue
        for key, value in group.items():
            if not isinstance(value, str) or key in {"version", "command"}:
                continue
            command_path = shutil.which(value) if group_name == "tools" else None
            path = Path(command_path).resolve() if command_path else resolve_from(source.parent, value)
            checks.append(
                {
                    "group": group_name,
                    "key": key,
                    "path": str(path) if path else None,
                    "exists": bool(path and path.exists()),
                    "kind": "file" if path and path.is_file() else "directory" if path and path.is_dir() else "missing",
                }
            )

    required = [item for item in checks if item["key"] in {"launcher", "batch", "command_path"}]
    return {
        "schema": data["schema"],
        "config_path": str(source),
        "checks": checks,
        "required_count": len(required),
        "required_present": sum(bool(item["exists"]) for item in required),
        "ready": bool(required) and all(bool(item["exists"]) for item in required),
    }
