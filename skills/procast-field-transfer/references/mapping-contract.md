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

Assign zero pressure where independent evidence identifies inactive contact.
Mark unknown support as missing or failed. If a task permits extrapolation,
record where it was used, how it was generated, and its distance from supported
data. Retain the original supported samples for comparison.
