---
name: nx-surface-repair
description: Inspect, repair, sew, heal, replace, offset, or thicken Siemens NX sheet and surface geometry for downstream meshing while preserving source geometry and reporting unresolved defects. Use when imported CAD has open sheets, gaps, bad faces, sliver surfaces, non-watertight boundaries, or mixed solid, sheet, facet, and convergent bodies that require a controlled repair decision.
---

# NX Surface Repair

Read `references/surface-repair-contract.md` before selecting a repair method.

## Classify first

Record units, bounding box, body types, body/face/edge counts, open or naked
edges, import warnings, and intended CFD boundaries. Distinguish solid, sheet,
facet, convergent, and imported B-Rep geometry before editing.

## Choose the lowest-risk route

1. Sew or stitch sheets when small gaps prevent closure.
2. Heal or replace localized defective faces when surrounding boundaries are
   reliable.
3. Offset or thicken a valid sheet when physical thickness is required.
4. Simplify fragmented B-Rep faces only with a declared deviation tolerance.
5. Route heavily faceted or noisy geometry to reverse modeling rather than
   applying blind smoothing.

Work on a copied model, use exact selectors, regenerate after each operation,
and stop if topology, scale, body identity, or important interfaces change
unexpectedly. Export the accepted part and Parasolid plus JSON/Markdown defect
and repair reports.
