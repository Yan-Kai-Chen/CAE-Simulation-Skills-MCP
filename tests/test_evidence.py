import csv

from procast_abaqus_agent.evidence import validate_evidence_dictionary


FIELDNAMES = [
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
]


def _write_dictionary(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def test_validate_evidence_dictionary_accepts_unique_complete_rows(tmp_path):
    source = tmp_path / "evidence.csv"
    _write_dictionary(
        source,
        [
            {
                "id": "T01",
                "category": "timing",
                "quantity": "First damage",
                "value": "1.2",
                "unit": "s",
                "physical_time_s": "1.2",
                "criterion": "first positive damage",
                "route": "objective onset",
                "claim_status": "accepted_result",
                "source_id": "SUMMARY",
            }
        ],
    )
    result = validate_evidence_dictionary(source)
    assert result["valid"] is True
    assert result["row_count"] == 1
    assert result["unique_id_count"] == 1


def test_validate_evidence_dictionary_reports_duplicate_ids(tmp_path):
    source = tmp_path / "evidence.csv"
    row = {
        "id": "T01",
        "category": "timing",
        "quantity": "First damage",
        "value": "1.2",
        "unit": "s",
        "physical_time_s": "1.2",
        "criterion": "first positive damage",
        "route": "objective onset",
        "claim_status": "accepted_result",
        "source_id": "SUMMARY",
    }
    _write_dictionary(source, [row, row])
    result = validate_evidence_dictionary(source)
    assert result["valid"] is False
    assert result["duplicate_ids"] == ["T01"]
