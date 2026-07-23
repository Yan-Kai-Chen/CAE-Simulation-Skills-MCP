---
name: procast-field-transfer
description: Register dissimilar ProCAST, Fluent, CAD, or Abaqus meshes and transfer temperature, contact pressure, stress, displacement, or corresponding-point data by physical coordinates. Use when meshes have different IDs or density, geometry moved rigidly, local design features changed, bottom or opening surfaces need controlled extrapolation, or displaced STL geometry must be reconstructed.
---

# ProCAST Field Transfer

## Treat correspondence as geometry

Never reuse node IDs across different meshes. Normalize units and body scope,
then register source and target coordinates before interpolation.

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
