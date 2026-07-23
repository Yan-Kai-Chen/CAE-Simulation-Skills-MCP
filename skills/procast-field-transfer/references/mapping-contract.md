# Mapping contract

## Required inputs

- source and target XYZ coordinates;
- explicit source/target units and frame names;
- body/part labels and optional surface normals;
- field name, component semantics, step and time;
- known transform, landmarks or sufficient overlap geometry.

## Validation

Report source-to-target and target-to-source P50/P95/max distances and coverage
within declared tolerances. Verify that high-distance points do not cross
parts, wall sides, openings or newly created geometry.

## Extrapolation

Use zero outside support only when zero has physical meaning, such as inactive
contact pressure. For temperature or stress, mark unsupported values as
extrapolated or failed. Keep drain-port or added-feature extrapolation separate
from directly observed values.
