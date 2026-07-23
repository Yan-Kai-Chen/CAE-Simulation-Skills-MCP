---
name: abaqus-wax-shell-fracture
description: Build, screen, run, extract, and validate wax-pressure-driven Abaqus XFEM Shell-fracture analyses without prescribing an initial crack. Use when Codex must transfer a physical-time pressure history to a Shell, screen candidate edge/root regions, run global initiation and local opening models, continue a restart, compare designs, or interpret STATUSXFEM, CSDMG, CRKOPEN and energy histories.
---

# Abaqus Wax-Shell Fracture

## Preserve the load history

Use the complete accepted physical-time grid rather than sparse field anchors.
Keep pressure reconstruction, structural accommodation and material
sensitivity parameters explicit. Do not add a crack-location kernel or pressure
gain to force the expected morphology.

Read `references/fracture-evidence-gates.md` before interpreting results.

## Screen before local propagation

1. Apply pressure to geometry-defined Shell regions.
2. Evaluate multiple tensile-strength assumptions.
3. Require irreversible face-connected element clusters rather than a single
   stress extreme.
4. Keep expected crack regions and control regions so the model can falsify the
   observed morphology.
5. Run the global model before selecting a buffered worst-location local model.

## Run and continue

Datacheck before solving. Use the smallest stabilization that converges and
require stabilization and kinetic energy to remain small relative to internal
energy. For a local continuation, transfer exact cut-boundary displacement
histories, retain the physical pressure history and record the restart time
offset.

## Compare designs fairly

Freeze Shell mesh, material assumptions, support, candidate definitions,
pressure-transfer method and output schedule. Change only the design-specific
load history. Let each design select its own worst accepted candidate, then
compare initiation, damage, opening, connected extent, stress, displacement and
energy.
