---
name: reverse-cad-modeling
description: Classify and rebuild rough STL, faceted, scanned, convergent, or over-fragmented CAD into cleaner analytic, NURBS, or hybrid geometry for CFD and CAE. Use when direct healing is insufficient and Codex must segment geometry, fit primitives or surfaces, preserve critical interfaces, compare deviations, and produce a transparent reconstructed CAD handoff.
---

# Reverse CAD Modeling

Read `references/reconstruction-contract.md` before choosing a reconstruction
level.

## Decision

- Repair existing CAD when B-Rep defects are local.
- Replace regions analytically when planes, cylinders, cones, ribs, holes,
  symmetry, and simple fillets are clear.
- Fit freeform surfaces when smooth regions cannot be represented by simple
  primitives.
- Use a hybrid route when analytic, freeform, preserved, and uncertain regions
  coexist.

## Workflow

1. Preserve and classify the source geometry.
2. Record units, bounding box, facet/face counts, tolerance, downstream use,
   and critical features.
3. Identify datums, axes, symmetry, repeated features, interfaces, and details
   that may be suppressed for CFD.
4. Rebuild a small pilot region and compare it with the source.
5. Continue only when deviation and feature preservation meet the declared
   contract.
6. Validate key dimensions, body state, watertightness intent, and downstream
   mesh suitability.
7. Export clean CAD and a report labeling reconstructed, preserved, simplified,
   and unresolved regions.

Do not describe visual smoothing or approximate surface fitting as exact CAD
recovery.
