from __future__ import annotations

import re
from pathlib import Path
from typing import Any


HEADER_RE = re.compile(r'"([^"]+)"')
FATAL_RE = re.compile(
    r"fatal error|floating point exception|license.*fail|abnormal exit|segmentation",
    re.IGNORECASE,
)


def _last_monitor_row(path: Path) -> dict[str, float] | None:
    headers: list[str] | None = None
    last: dict[str, float] | None = None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if line.startswith("(") and "flow-time" in line:
            headers = HEADER_RE.findall(line)
            continue
        if not headers or not line or not (line[0].isdigit() or line[0] in "+-."):
            continue
        fields = line.split()
        if len(fields) < len(headers):
            continue
        try:
            last = {name: float(value) for name, value in zip(headers, fields)}
        except ValueError:
            continue
    return last


def _tail(path: Path, limit: int = 20000) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[-limit:]


def get_fluent_run_status(run_root: str | Path) -> dict[str, Any]:
    """Inspect Fluent monitors and result artifacts without modifying the run."""
    root = Path(run_root).expanduser().resolve()
    if not root.is_dir():
        return {"run_root": str(root), "state": "missing", "exists": False}

    monitor_dir = root / "monitors"
    monitors = sorted(monitor_dir.glob("*.out")) if monitor_dir.is_dir() else []
    rows = [(path, _last_monitor_row(path)) for path in monitors]
    valid = [(path, row) for path, row in rows if row and "flow-time" in row]
    latest_path: Path | None = None
    latest_row: dict[str, float] | None = None
    if valid:
        latest_path, latest_row = max(valid, key=lambda item: item[1]["flow-time"])

    log_paths = sorted(
        path
        for pattern in ("*.log", "*.trn")
        for path in root.rglob(pattern)
        if path.is_file()
    )
    fatal_lines: list[str] = []
    for path in log_paths:
        fatal_lines.extend(
            line.strip() for line in _tail(path).splitlines() if FATAL_RE.search(line)
        )

    case_files = list(root.rglob("*.cas.h5"))
    data_files = list(root.rglob("*.dat.h5"))
    final_data = [path for path in data_files if "final" in path.name.lower()]

    state = "no_monitor_data"
    if fatal_lines:
        state = "failed"
    elif final_data:
        state = "completed_artifact_present"
    elif latest_row:
        state = "progress_recorded"
    elif case_files or data_files:
        state = "artifacts_only"

    return {
        "run_root": str(root),
        "state": state,
        "exists": True,
        "monitor_count": len(monitors),
        "latest_monitor": str(latest_path) if latest_path else None,
        "latest_flow_time_s": latest_row.get("flow-time") if latest_row else None,
        "latest_time_step": latest_row.get("Time Step") if latest_row else None,
        "latest_delta_time_s": latest_row.get("delta-time") if latest_row else None,
        "case_file_count": len(case_files),
        "data_file_count": len(data_files),
        "final_data_count": len(final_data),
        "fatal_count": len(fatal_lines),
        "fatal_lines": fatal_lines[-10:],
    }
