from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = (
    "id",
    "category",
    "quantity",
    "value",
    "unit",
    "physical_time_s",
    "criterion",
    "route",
    "claim_status",
    "source_id",
)

REQUIRED_VALUES = tuple(name for name in REQUIRED_COLUMNS if name != "physical_time_s")


def validate_evidence_dictionary(csv_path: str | Path) -> dict[str, Any]:
    """Validate a manuscript evidence-dictionary CSV without modifying it."""
    source = Path(csv_path).expanduser().resolve()
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = tuple(reader.fieldnames or ())
        rows = list(reader)

    missing_columns = [name for name in REQUIRED_COLUMNS if name not in columns]
    ids = [str(row.get("id", "")).strip() for row in rows]
    duplicate_ids = sorted(name for name, count in Counter(ids).items() if name and count > 1)
    incomplete_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        missing_values = [name for name in REQUIRED_VALUES if not str(row.get(name, "")).strip()]
        if missing_values:
            incomplete_rows.append(
                {"line": index, "id": str(row.get("id", "")).strip(), "missing": missing_values}
            )

    status_counts = Counter(str(row.get("claim_status", "")).strip() for row in rows)
    valid = bool(rows) and not missing_columns and not duplicate_ids and not incomplete_rows
    return {
        "schema": "cae_evidence_dictionary_validation_v1",
        "path": str(source),
        "row_count": len(rows),
        "unique_id_count": len(set(ids) - {""}),
        "columns": list(columns),
        "missing_required_columns": missing_columns,
        "duplicate_ids": duplicate_ids,
        "incomplete_rows": incomplete_rows,
        "claim_status_counts": dict(sorted(status_counts.items())),
        "valid": valid,
    }
