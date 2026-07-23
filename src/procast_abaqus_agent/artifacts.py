from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any


RAW_SUFFIXES = {
    ".odb", ".sim", ".prt", ".sta", ".msg", ".com", ".dat", ".res",
    ".unf", ".vdb", ".asf", ".ntl", ".npz", ".npy", ".parquet",
}
RAW_COMPOUND_SUFFIXES = {".cas.h5", ".dat.h5", ".msh.h5"}


def _is_raw(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() in RAW_SUFFIXES or any(
        name.endswith(suffix) for suffix in RAW_COMPOUND_SUFFIXES
    )


def index_artifacts(root: str | Path, include_raw: bool = False) -> dict[str, Any]:
    """Index processed artifacts, excluding vendor/raw solver files by default."""
    base = Path(root).expanduser().resolve()
    if not base.is_dir():
        raise FileNotFoundError(base)
    files = [path for path in base.rglob("*") if path.is_file()]
    selected = files if include_raw else [path for path in files if not _is_raw(path)]
    extensions = Counter(path.suffix.lower() or "<none>" for path in selected)
    return {
        "root": str(base),
        "include_raw": include_raw,
        "all_file_count": len(files),
        "indexed_file_count": len(selected),
        "excluded_raw_count": len(files) - len(selected),
        "indexed_bytes": sum(path.stat().st_size for path in selected),
        "extensions": dict(sorted(extensions.items())),
    }
