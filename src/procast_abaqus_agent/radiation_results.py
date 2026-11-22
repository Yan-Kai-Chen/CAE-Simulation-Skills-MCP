from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .radiation import reciprocity_checks


@dataclass(slots=True)
class _Range:
    weighted_sum: float = 0.0
    minimum: float = math.inf
    maximum: float = -math.inf
    peak_face: str = ""

    def add(self, value: float, weight: float, face: str) -> None:
        self.weighted_sum += weight * value
        self.minimum = min(self.minimum, value)
        if value > self.maximum:
            self.maximum = value
            self.peak_face = face

    def report(self, weight: float) -> dict[str, Any]:
        return {
            "mean": self.weighted_sum / weight, "min": self.minimum,
            "max": self.maximum, "max_face_id": self.peak_face,
        }


@dataclass(slots=True)
class _Group:
    receivers: dict[str, _Range]
    summed: _Range = field(default_factory=_Range)
    reported: _Range = field(default_factory=_Range)
    faces: int = 0
    weight: float = 0.0


def _group_name(label: str) -> str:
    name = label.strip()
    if not name:
        raise ValueError("Empty radiation group label")
    try:
        number = float(name)
    except ValueError:
        return name
    if math.isfinite(number) and number.is_integer() and abs(number) < 2**53:
        return str(int(number))
    return name


def _number(row: dict[str, str], column: str, face_id: str) -> float:
    try:
        value = float(row[column])
    except (TypeError, ValueError):
        raise ValueError(f"Face {face_id!r} has an invalid value for {column!r}") from None
    if not math.isfinite(value):
        raise ValueError(f"Face {face_id!r} has a nonfinite value for {column!r}")
    return value


def analyze_rdebug_csv(
    csv_path: str | Path,
    *,
    closed_enclosure: bool = False,
    complete_groups: bool = False,
    sum_tolerance: float = 0.01,
    area_unit: str | None = None,
) -> dict[str, Any]:
    """Analyze face-level exported RDEBUG data from one radiation state."""
    if not math.isfinite(sum_tolerance) or sum_tolerance < 0:
        raise ValueError("Sum tolerance must be finite and nonnegative")
    path = Path(csv_path).expanduser().resolve()
    groups: dict[str, _Group] = {}
    seen: set[str] = set()
    examples = []
    out_of_range = sum_mismatch = closure_mismatch = 0
    worst_sum_difference = worst_closure_error = 0.0
    target_prefix = "face to group "

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        columns = {name.strip().casefold(): name for name in header}
        if len(columns) != len(header):
            raise ValueError("Duplicate column names in RDEBUG table")
        face_col = columns.get("face_id")
        group_col = columns.get("source_group") or columns.get("face groups")
        area_col = columns.get("area")
        total_col = columns.get("face to all groups")
        receivers = {}
        for key, column in columns.items():
            if key.startswith(target_prefix):
                target = _group_name(column.strip()[len(target_prefix):])
                if target in receivers:
                    raise ValueError(f"Duplicate receiver group {target!r}")
                receivers[target] = column
        if not face_col or not group_col or not receivers:
            raise ValueError("Expected face_id, source_group or Face Groups, and Face to Group columns")
        if complete_groups and not area_col:
            raise ValueError("An area column is required for reciprocity")

        for row in reader:
            face_id = (row.get(face_col) or "").strip()
            if None in row or not face_id or face_id in seen:
                raise ValueError(f"Invalid, empty or duplicate face ID at CSV line {reader.line_num}")
            seen.add(face_id)
            name = _group_name(row.get(group_col) or "")
            weight = _number(row, area_col, face_id) if area_col else 1.0
            if weight <= 0:
                raise ValueError(f"Face {face_id!r} needs positive area")
            values = {target: _number(row, column, face_id) for target, column in receivers.items()}
            total = math.fsum(values.values())
            reported = _number(row, total_col, face_id) if total_col else None

            if name not in groups:
                groups[name] = _Group({target: _Range() for target in receivers})
            group = groups[name]
            group.faces += 1
            group.weight += weight
            group.summed.add(total, weight, face_id)
            if reported is not None:
                group.reported.add(reported, weight, face_id)
            for target, value in values.items():
                group.receivers[target].add(value, weight, face_id)

            flags = []
            in_range = all(0 <= value <= 1 for value in values.values())
            if not in_range or (reported is not None and not 0 <= reported <= 1 + sum_tolerance):
                out_of_range += 1
                flags.append("coefficient_out_of_range")
            if reported is not None:
                difference = abs(total - reported)
                worst_sum_difference = max(worst_sum_difference, difference)
                if difference > sum_tolerance:
                    sum_mismatch += 1
                    flags.append("exported_group_sum_differs_from_native_total")
            if closed_enclosure:
                closure = abs(1 - (reported if reported is not None else total))
                worst_closure_error = max(worst_closure_error, closure)
                if closure > sum_tolerance:
                    closure_mismatch += 1
                    flags.append("closed_enclosure_sum_differs_from_one")
            if flags and len(examples) < 10:
                examples.append({
                    "face_id": face_id, "source_group": name, "checks": flags,
                    "exported_group_sum": total, "native_total": reported,
                })
    if not seen:
        raise ValueError(f"No face rows found in {path}")

    summary = {}
    mean_factors = {}
    areas = {}
    for name, group in groups.items():
        targets = sorted(group.receivers, key=lambda target: -group.receivers[target].weighted_sum)
        result = {target: group.receivers[target].report(group.weight) for target in targets}
        mean_factors[name] = {target: stats["mean"] for target, stats in result.items()}
        if area_col:
            areas[name] = group.weight
        summary[name] = {
            "face_count": group.faces, "area": areas.get(name),
            "exported_group_sum": group.summed.report(group.weight),
            "native_total": group.reported.report(group.weight) if total_col else None,
            "receivers": result,
        }
    return {
        "analysis": "procast_rdebug2_face_to_group", "source_csv": str(path),
        "face_count": len(seen), "weighting": "face_area" if area_col else "equal_faces",
        "area_unit": area_unit if area_col else None,
        "sum_tolerance": sum_tolerance, "closed_enclosure_check": closed_enclosure,
        "out_of_range_faces": out_of_range,
        "sum_mismatch_faces": sum_mismatch if total_col else None,
        "max_abs_sum_difference": worst_sum_difference if total_col else None,
        "closure_mismatch_faces": closure_mismatch if closed_enclosure else None,
        "max_abs_closure_error": worst_closure_error if closed_enclosure else None,
        "example_flagged_faces": examples, "sources": summary,
        "reciprocity": reciprocity_checks(mean_factors, areas) if complete_groups else None,
    }
