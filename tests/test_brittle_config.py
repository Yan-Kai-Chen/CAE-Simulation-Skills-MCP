import json
import runpy
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "skills/abaqus-brittle-fracture-generalization"
validate = runpy.run_path(str(SKILL / "scripts/validate_fracture_case_config.py"))["validate"]


def screening_case():
    return json.loads(
        (SKILL / "references/example-ceramic-core-case.json").read_text(encoding="utf-8")
    )


def test_intact_screen_uses_elastic_fields_without_fracture_data():
    case = screening_case()
    assert "fracture" not in case["material"]
    assert validate(case) == ([], [])


def test_crack_model_needs_fracture_data_and_calibrated_claim():
    case = screening_case()
    case["objective"] = "initiation"
    case["solver"]["method"] = "XFEM"
    case["validation"]["claim_level"] = "predictive"
    errors, _ = validate(case)
    assert "missing required field: material.fracture.evolution" in errors
    assert any("calibration_status='calibrated'" in error for error in errors)

    case["material"]["fracture"] = {
        "initiation": "maximum_principal_stress",
        "evolution": "energy_based",
        "calibration_status": "calibrated",
    }
    errors, warnings = validate(case)
    assert errors == []
    assert any("MAXPS" in warning for warning in warnings)


def test_bad_nested_objects_and_enums_return_validation_errors():
    case = screening_case()
    case["solver"] = []
    case["load"] = None
    case["validation"]["claim_level"] = {}
    errors, _ = validate(case)
    assert "missing required field: solver.method" in errors
    assert "missing required field: load.type" in errors
    assert "unsupported validation.claim_level: {}" in errors


def test_intact_screen_cannot_claim_crack_initiation():
    case = screening_case()
    case["objective"] = "initiation"
    errors, _ = validate(case)
    assert "intact_screen requires objective and validation.claim_level to be screening" in errors
