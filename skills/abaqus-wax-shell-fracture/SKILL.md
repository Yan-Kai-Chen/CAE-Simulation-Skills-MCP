---
name: abaqus-wax-shell-fracture
description: Build, screen, run, extract, and validate Fluent- or ProCAST-informed wax-pressure-driven Abaqus XFEM Shell-fracture analyses without prescribing an initial crack. Use when Codex must transfer a physical-time pressure history, compare objective candidate regions, separate an independent onset check from a primary full-growth route, resolve a topology-verified vent, apply continuous reduced-order pressure feedback, compare designs, or interpret STATUSXFEM, CSDMG, CRKOPEN and energy histories.
---

# Abaqus Wax-Shell Fracture

## Preserve the load history

Use the complete accepted physical-time grid rather than sparse field anchors.
Keep the Fluent melt/drainage source, pressure reconstruction, structural
accommodation and material sensitivity parameters explicit. Do not add a
crack-location kernel or pressure gain to force the expected morphology.

Read `references/fracture-evidence-gates.md` before interpreting results.

## Screen before local propagation

1. Apply pressure to geometry-defined Shell regions.
2. Evaluate multiple tensile-strength assumptions.
3. Require irreversible face-connected element clusters rather than a single
   stress extreme.
4. Keep expected crack regions and control regions so the model can falsify the
   observed morphology.
5. Run the global model before selecting a buffered worst-location local model.

When experiment morphology informs validation, separate two roles:

- use a mechanics-only multi-candidate branch without the observed crack
  location as an independent location/onset check;
- use one accepted buffered local branch as the primary full-growth route.

Do not present a candidate branch that reaches its enrichment-window boundary
as an unrestricted propagation prediction.

## Run and continue

Datacheck before solving. Use the smallest stabilization that converges and
require stabilization and kinetic energy to remain small relative to internal
energy. For a local continuation, transfer exact cut-boundary displacement
histories, retain the physical pressure history and record the restart time
offset.

## Continue to a verified vent

1. Distinguish first cohesive damage, first fully cracked element, and first
   connected inner-to-outer path.
2. Search the vent event coarsely, then replay from the last unvented state at
   a finer output interval.
3. Activate pressure relief only when one fully cracked face-connected
   component touches both the loaded inner surface and physical exterior.
4. Keep pressure continuous at the event. Use a documented reduced-order
   feedback law rather than deleting the pressure instantaneously.
5. Continue through peak load and unloading. Treat reduced opening with
   irreversible topology as closure, not healing.
6. Report post-vent connected-extent growth separately from completion of
   already intersected crack elements.

## Compare designs fairly

Freeze Shell mesh, material assumptions, support, candidate definitions,
pressure-transfer method and output schedule. Change only the design-specific
load history. Let each design select its own worst accepted candidate, then
compare initiation, damage, opening, connected extent, stress, displacement and
energy.
