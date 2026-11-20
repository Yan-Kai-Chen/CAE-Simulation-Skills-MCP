#!/usr/bin/env python3
"""Validate the portable contract for a brittle-fracture case.

This checks structure and provenance fields only. It does not validate material
calibration, Abaqus availability, or physical correctness.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_OBJECTIVES = {
    "screening",
    "initiation",
    "initiation_and_path",
    "opening_or_leakage",
    "residual_strength",
    "life",
}
ALLOWED_METHODS = {
    "intact_screen",
    "XFEM",
    "cohesive",
    "VCCT",
    "smeared_damage",
    "Explicit_damage",
    "phase_field_UEL",
}
ALLOWED_CLAIMS = {"screening", "mechanism", "conditional_engineering", "predictive"}
MISSING = object()


def nested(data: dict[str, Any], dotted: str, default: Any = None) -> Any:
    value: Any = data
    for key in dotted.split("."):
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "schema_version",
        "case_id",
        "objective",
        "units.length",
        "units.stress",
        "units.time",
        "units.temperature",
        "geometry.mesh",
        "geometry.coordinate_frame",
        "geometry.revision",
        "solver.product",
        "solver.method",
        "solver.step",
        "load.source",
        "load.type",
        "load.time_basis",
        "load.regions",
        "material.elastic",
        "validation.claim_level",
    ]
    method = nested(data, "solver.method")
    if isinstance(method, str) and method in ALLOWED_METHODS - {"intact_screen"}:
        required.extend(
            (
                "material.fracture.initiation",
                "material.fracture.evolution",
                "material.fracture.calibration_status",
            )
        )

    for key in required:
        value = nested(data, key, MISSING)
        if value is MISSING:
            errors.append(f"missing required field: {key}")
        elif value in (None, "", [], {}):
            errors.append(f"empty required field: {key}")

    objective = data.get("objective")
    claim = nested(data, "validation.claim_level")
    choices = (
        ("objective", objective, ALLOWED_OBJECTIVES),
        ("solver.method", method, ALLOWED_METHODS),
        ("validation.claim_level", claim, ALLOWED_CLAIMS),
    )
    for field, value, allowed in choices:
        if value is not None and (not isinstance(value, str) or value not in allowed):
            errors.append(f"unsupported {field}: {value!r}")
    if method == "intact_screen" and (objective, claim) != ("screening", "screening"):
        errors.append("intact_screen requires objective and validation.claim_level to be screening")

    for field in ("load.type", "load.regions"):
        value = nested(data, field, MISSING)
        if value is MISSING:
            continue
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip() for item in value
        ):
            errors.append(f"{field} must be a list of nonempty strings")

    calibration = nested(data, "material.fracture.calibration_status")
    if claim in ("conditional_engineering", "predictive") and calibration != "calibrated":
        errors.append(
            "conditional_engineering/predictive claims require "
            "material.fracture.calibration_status='calibrated'"
        )
    elif calibration not in (None, "calibrated") and method != "intact_screen":
        warnings.append("uncalibrated fracture properties support screening or mechanism claims")

    if method == "XFEM":
        initiation = nested(data, "material.fracture.initiation")
        if initiation == "maximum_principal_stress":
            warnings.append("confirm tensile opening dominates before using MAXPS")

    time_basis = nested(data, "load.time_basis")
    if time_basis not in (None, "physical_seconds"):
        warnings.append("document the conversion from solver/pseudo time to physical time")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="JSON case configuration")
    args = parser.parse_args()

    try:
        data = json.loads(args.config.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2
    if not isinstance(data, dict):
        print(json.dumps({"valid": False, "errors": ["top-level JSON value must be an object"]}, indent=2))
        return 2

    errors, warnings = validate(data)
    result = {
        "valid": not errors,
        "case_id": data.get("case_id"),
        "method": nested(data, "solver.method"),
        "claim_level": nested(data, "validation.claim_level"),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
