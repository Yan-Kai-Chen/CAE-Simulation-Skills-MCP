from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .config import load_json, resolve_from


STAGES = (
    "preflight",
    "readiness",
    "solver_setup",
    "solver_launch",
    "target_step",
    "restart_prepare",
    "restart_launch",
    "restart_target_step",
    "numerical_export",
    "native_export",
    "video_compose",
)

STEP_RE = re.compile(
    r"^[ \t]*(?:TIME[ \t]+)?STEP(?:[ \t]+NO\.)?[ \t]*[=:]?[ \t]*(\d+)\b",
    re.IGNORECASE | re.MULTILINE,
)
FATAL_RE = re.compile(r"fatal|abort|license.*fail|segmentation|error termination", re.IGNORECASE)
COMPLETE_RE = re.compile(
    r"normal end|normal termination|analysis completed|calculation completed|"
    r"end of procast|\bTFINAL[ \t]+reached\b",
    re.IGNORECASE,
)


def plan_pipeline(job_path: str | Path) -> dict[str, Any]:
    """Resolve a ProCAST pipeline job and report enabled or blocked stages."""
    source = Path(job_path).expanduser().resolve()
    job = load_json(source)
    if job.get("schema") != "procast_pipeline_job_v1":
        raise ValueError("schema must be procast_pipeline_job_v1")
    execution = job.get("execution", {})
    stages = job.get("stages", {})
    enabled = [name for name in STAGES if bool(stages.get(name, {}).get("enabled", False))]
    solver_stages = {"solver_launch", "target_step", "restart_launch", "restart_target_step"}
    authorized = bool(execution.get("authorized_solver_actions", False))
    plan_only = bool(execution.get("plan_only", True))
    blocked = [name for name in enabled if name in solver_stages and not (plan_only or authorized)]

    case = job.get("case", {})
    path_keys = {"case_dir", "input_vdb", "input_unf", "time_csv"}
    resolved_case = {
        key: str(resolve_from(source.parent, value))
        if key in path_keys and isinstance(value, str) and value
        else value
        for key, value in case.items()
    }
    return {
        "job_name": job.get("job_name"),
        "job_path": str(source),
        "plan_only": plan_only,
        "authorized_solver_actions": authorized,
        "enabled_stages": enabled,
        "blocked_stages": blocked,
        "case": resolved_case,
        "valid": not blocked,
    }


def _tail(path: Path, limit: int = 4000) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[-limit:]


def get_run_status(run_root: str | Path, prefix: str) -> dict[str, Any]:
    """Inspect existing ProCAST run logs and manifests without changing the run."""
    root = Path(run_root).expanduser().resolve()
    pout = root / f"{prefix}p.out"
    text = _tail(pout)
    steps = STEP_RE.findall(text)
    fatal_lines = [line.strip() for line in text.splitlines() if FATAL_RE.search(line)]
    stop_manifest = root / "stop_manifest.json"
    launcher_status = root / "launcher_status.json"

    state = "missing"
    if pout.exists():
        state = "failed" if fatal_lines else "completed" if COMPLETE_RE.search(text) else "progress_recorded"
    if stop_manifest.exists():
        state = "stopped"
    elif launcher_status.exists() and state not in ("failed", "completed"):
        try:
            status_data = json.loads(launcher_status.read_text(encoding="utf-8-sig"))
            if isinstance(status_data, dict) and status_data.get("state"):
                state = str(status_data["state"])
        except (OSError, ValueError, TypeError):
            pass

    return {
        "run_root": str(root),
        "prefix": prefix,
        "state": state,
        "p_out": str(pout),
        "p_out_exists": pout.exists(),
        "last_step": int(steps[-1]) if steps else None,
        "fatal_count": len(fatal_lines),
        "fatal_lines": fatal_lines[-10:],
        "stop_manifest_exists": stop_manifest.exists(),
        "launcher_status_exists": launcher_status.exists(),
    }
