# Reverse CAD reconstruction contract

## Required inputs

- copied source geometry and source type;
- intended downstream solver or mesher;
- unit, bounding box, and known coordinate system;
- required geometric tolerance;
- critical features and interfaces;
- allowed simplifications.

## Reconstruction levels

1. Inspect only: classify and recommend the next action.
2. Repair existing B-Rep: heal localized defects without rebuilding design
   intent.
3. Analytic replacement: fit planes, cylinders, cones, spheres, slots, ribs,
   and simple transitions.
4. Freeform fit: reconstruct bounded patches with declared continuity and
   deviation.
5. Hybrid: label analytic, freeform, preserved, simplified, and uncertain
   regions separately.

## Acceptance

Compare source and output bounding boxes, key dimensions, body count/type,
interfaces, and fitted deviation. Require non-empty native and exchange-format
outputs when supported. Stop when tolerance is unknown, critical detail cannot
be distinguished from noise, or a proposed simplification has not been
accepted.
