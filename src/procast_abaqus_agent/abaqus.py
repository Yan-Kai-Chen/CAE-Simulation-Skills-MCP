from __future__ import annotations

import re
from pathlib import Path
from typing import Any


SUCCESS_RE = re.compile(r"analysis has completed successfully|completed successfully", re.IGNORECASE)
FATAL_RE = re.compile(r"\*\*\*error|fatal|terminated due to|required is less than the minimum", re.IGNORECASE)
INC_RE = re.compile(r"\b(?:increment|inc)\s*[=:]?\s*(\d+)\b", re.IGNORECASE)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def get_job_status(job_dir: str | Path, job_name: str) -> dict[str, Any]:
    """Inspect existing Abaqus status files and summarize completion or failure."""
    root = Path(job_dir).expanduser().resolve()
    sta = root / f"{job_name}.sta"
    msg = root / f"{job_name}.msg"
    lck = root / f"{job_name}.lck"
    odb = root / f"{job_name}.odb"
    text = "\n".join((_read(sta), _read(msg)))
    fatal_lines = [line.strip() for line in text.splitlines() if FATAL_RE.search(line)]
    increments = [int(match.group(1)) for match in INC_RE.finditer(text)]

    if lck.exists():
        state = "running_or_locked"
    elif fatal_lines:
        state = "failed"
    elif SUCCESS_RE.search(text):
        state = "completed"
    elif sta.exists() or msg.exists() or odb.exists():
        state = "incomplete_or_stopped"
    else:
        state = "missing"

    return {
        "job_dir": str(root),
        "job_name": job_name,
        "state": state,
        "last_increment": max(increments) if increments else None,
        "fatal_count": len(fatal_lines),
        "fatal_lines": fatal_lines[-10:],
        "files": {
            "sta": sta.exists(),
            "msg": msg.exists(),
            "lck": lck.exists(),
            "odb": odb.exists(),
        },
    }
