# HyperMesh surface-meshing contract

## Required plan fields

- schema and run identifier;
- copied geometry input and dedicated output directory;
- source and target unit;
- target and permitted minimum/maximum element size;
- surface element family and order;
- component-to-boundary-zone mapping;
- feature-edge, curvature, proximity, and defeaturing controls;
- expected output files;
- quality limits and stop conditions.

## Pre-mesh gates

- The input exists and the output will not overwrite it.
- Bounding-box scale is plausible in the declared unit.
- Components and CFD boundary roles are uniquely mapped.
- Open edges and intentionally open CFD boundaries are distinguished.
- Target size is expressed in model units after conversion.

## Acceptance gates

- The expected surface element and node counts are nonzero.
- No duplicate surface element remains.
- Failed or unmeshed faces equal zero, or are explicitly rejected.
- Surface normals and zone names are suitable for downstream import.
- Quality metrics satisfy the declared limits.
- The manifest, log, model, exported mesh, and quality report all exist.

Treat successful surface meshing as a handoff result, not proof that a later
volume mesh or CFD solve is valid.
