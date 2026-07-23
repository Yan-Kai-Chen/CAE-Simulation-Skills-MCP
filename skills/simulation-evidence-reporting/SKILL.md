---
name: simulation-evidence-reporting
description: Turn coupled ProCAST/Fluent/Abaqus simulation outputs into reproducible engineering reports and manuscript claims with explicit evidence levels. Use when Codex must summarize a run, compare designs, prepare figures/tables, decide whether a fracture claim is mechanism-level or predictive, package processed writing assets, or prevent Fluent risk and numerical XFEM damage from being overstated as guaranteed physical rupture.
---

# Simulation Evidence Reporting

## Reconstruct the evidence chain

Present geometry, ProCAST thermal source, Fluent melt/drainage and load
history, field transfer, Abaqus model, initiation morphology, local
damage/opening, energy quality and experiment comparison in that order. Keep
assumptions and measured inputs separate.

Read `references/claim-levels.md` before writing conclusions.

## Separate resolved and conditional statements

- Report directly resolved quantities with units and time.
- Label material, restraint, contact and fracture-energy brackets as
  assumptions or sensitivities until calibrated.
- Describe numerical XFEM activation as numerical damage onset, not guaranteed
  visible cracking.
- Distinguish risk suppression from crack elimination and local damage from
  complete rupture or pressure release.

## Package for reuse

Include processed tables, figures, captions, methods/results text, claim
boundaries, source maps, plotting scripts and checksums. Exclude vendor solver
databases and private case data unless the recipient explicitly needs a restart
package and has the required licenses.
