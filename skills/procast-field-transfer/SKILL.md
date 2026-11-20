---
name: procast-field-transfer
description: Register dissimilar ProCAST, Fluent, CAD, or Abaqus meshes and transfer temperature, contact pressure, stress, displacement, or corresponding-point data by physical coordinates. Use when meshes have different IDs or density, geometry moved rigidly, local design features changed, bottom or opening surfaces need controlled extrapolation, or displaced STL geometry must be reconstructed.
---

# ProCAST Field Transfer

## Treat correspondence as geometry

Verify mesh identity and body scope before using original IDs. For different
meshes, normalize units and register source and target coordinates before
interpolation.

Read `references/mapping-contract.md` before a production transfer.

## Select a method

1. Use verified IDs only inside the same mesh and coordinate frame.
2. For rigid motion, solve or load `x_target = R x_source + t` and validate
   symmetric overlap.
3. For similar geometry, rigidly prealign, add feature-aware descriptors and
   reject new/deleted features without a defensible equivalent.
4. Use barycentric interpolation when volume connectivity is available;
   otherwise use local kNN with explicit distance support.
5. Rotate tensor components with `R sigma R^T`; do not rotate scalar pressure,
   temperature or von Mises stress.

Use `scripts/procast_correspondence_csv.py` for generic point-cloud tables.

## Align time and physical meaning

Use the step and time recorded for each field and run segment. Compare within
common coverage, and document the interpolation and its validity for the
quantity being transferred. Retain jump events such as a change of contact
or loading regime. For surface loads verify the side, normal, units, and
resultant where applicable. Record whether the target receives an applied
load, initial state, or field for comparison.

## Reconstruct geometry

Build deformed coordinates from the original coordinate plus signed vector
displacement after unit conversion. Do not reconstruct geometry from total
displacement magnitude alone. State the origin or center used for any final
global scaling.

## Report confidence

Return matched coordinates, nearest distance, interpolation support, part
match, transform error, sampled value, unit and one of: `exact_id`,
`rigid_high`, `interpolated`, `local_corrected`, `extrapolated`,
`no_equivalent`, or `failed`.
