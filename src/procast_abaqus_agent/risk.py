from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def _read_columns(path: Path, names: list[str]) -> dict[str, list[float]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"No rows found: {path}")
    missing = [name for name in names if name not in rows[0]]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    return {name: [float(row[name]) for row in rows] for name in names}


def _crossing_time(
    t0: float, t1: float, y0: float, y1: float, threshold: float
) -> float:
    if y1 == y0:
        return t1
    return t0 + (threshold - y0) * (t1 - t0) / (y1 - y0)


def _interpolate(times: list[float], values: list[float], target: float) -> float:
    if target <= times[0]:
        return values[0]
    if target >= times[-1]:
        return values[-1]
    for i in range(1, len(times)):
        if target <= times[i]:
            ratio = (target - times[i - 1]) / (times[i] - times[i - 1])
            return values[i - 1] + ratio * (values[i] - values[i - 1])
    return values[-1]


def compute_pressure_risk_metrics(
    csv_path: str | Path,
    pressure_column: str,
    threshold_mpa: float,
    time_column: str = "time_s",
    temperature_column: str | None = None,
    activation_temperature_c: float | None = None,
) -> dict[str, Any]:
    """Compute physical-time pressure peak, exposure and threshold metrics."""
    source = Path(csv_path).expanduser().resolve()
    names = [time_column, pressure_column]
    if temperature_column:
        names.append(temperature_column)
    data = _read_columns(source, names)
    times = data[time_column]
    pressure = data[pressure_column]
    if len(times) < 2:
        raise ValueError("At least two time samples are required")
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("Physical time must be strictly increasing")

    exposure = 0.0
    duration = 0.0
    excess = 0.0
    for t0, t1, p0, p1 in zip(times, times[1:], pressure, pressure[1:]):
        dt = t1 - t0
        exposure += 0.5 * (p0 + p1) * dt
        q0 = p0 - threshold_mpa
        q1 = p1 - threshold_mpa
        if q0 > 0.0 and q1 > 0.0:
            duration += dt
            excess += 0.5 * (q0 + q1) * dt
        elif q0 > 0.0 or q1 > 0.0:
            crossing = _crossing_time(t0, t1, p0, p1, threshold_mpa)
            active_dt = crossing - t0 if q0 > 0.0 else t1 - crossing
            duration += active_dt
            excess += 0.5 * max(q0, q1) * active_dt

    peak_index = max(range(len(pressure)), key=pressure.__getitem__)
    result: dict[str, Any] = {
        "source_csv": str(source),
        "time_column": time_column,
        "pressure_column": pressure_column,
        "sample_count": len(times),
        "first_time_s": times[0],
        "final_time_s": times[-1],
        "peak_pressure_mpa": pressure[peak_index],
        "peak_time_s": times[peak_index],
        "pressure_exposure_mpa_s": exposure,
        "threshold_mpa": threshold_mpa,
        "duration_above_threshold_s": duration,
        "excess_exposure_mpa_s": excess,
    }

    if temperature_column or activation_temperature_c is not None:
        if not temperature_column or activation_temperature_c is None:
            raise ValueError(
                "temperature_column and activation_temperature_c must be provided together"
            )
        temperature = data[temperature_column]
        activation_time: float | None = None
        for i, value in enumerate(temperature):
            if value >= activation_temperature_c:
                activation_time = (
                    times[0]
                    if i == 0
                    else _crossing_time(
                        times[i - 1],
                        times[i],
                        temperature[i - 1],
                        value,
                        activation_temperature_c,
                    )
                )
                break
        result.update(
            {
                "temperature_column": temperature_column,
                "activation_temperature_c": activation_temperature_c,
                "activation_time_s": activation_time,
                "pressure_at_activation_mpa": (
                    _interpolate(times, pressure, activation_time)
                    if activation_time is not None
                    else None
                ),
            }
        )
    return result
