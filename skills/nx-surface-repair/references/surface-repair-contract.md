# NX surface-repair contract

## Required inspection

- copied source and output locations;
- unit and bounding box;
- body count by solid, sheet, facet, convergent, and unknown type;
- face, edge, open-edge, and warning counts when available;
- intended inlets, outlets, interfaces, and closed walls;
- tolerance and critical features that must be preserved.

## Repair contracts

- Sew: target sheets, tool sheets, gap tolerance, expected closure and body
  state.
- Local heal/replace: defective faces, boundary loops, continuity target, and
  affected region.
- Offset/thicken: selected sheet or faces, direction, thickness, cap rule, and
  expected output state.
- Simplify/merge: selected fragments, target analytic form, allowed deviation,
  and protected features.

## CFD acceptance

Accept only when required walls are closed, intentional openings remain named,
body count and type match, scale is unchanged, non-manifold regions are absent
or reported, and part/exchange outputs are non-empty. Stop when a repair
deletes major regions, hides warnings, or cannot prove output body identity.
