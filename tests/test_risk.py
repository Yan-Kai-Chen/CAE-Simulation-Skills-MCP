import csv

import pytest

from procast_abaqus_agent.risk import compute_pressure_risk_metrics


def test_pressure_risk_resolves_threshold_crossings(tmp_path):
    source = tmp_path / "history.csv"
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["time_s", "pressure", "temperature"])
        writer.writeheader()
        writer.writerows(
            [
                {"time_s": 0, "pressure": 0, "temperature": 0},
                {"time_s": 1, "pressure": 2, "temperature": 5},
                {"time_s": 2, "pressure": 0, "temperature": 10},
            ]
        )
    result = compute_pressure_risk_metrics(
        source,
        "pressure",
        1.0,
        temperature_column="temperature",
        activation_temperature_c=5.0,
    )
    assert result["peak_pressure_mpa"] == 2.0
    assert result["pressure_exposure_mpa_s"] == 2.0
    assert result["duration_above_threshold_s"] == 1.0
    assert result["excess_exposure_mpa_s"] == pytest.approx(0.5)
    assert result["activation_time_s"] == 1.0
    assert result["pressure_at_activation_mpa"] == 2.0
