---
name: simulation-evidence-reporting
description: Turn coupled CAD, meshing, ProCAST, Fluent, and Abaqus outputs into reproducible engineering reports and manuscript claims with explicit evidence levels and a canonical result data dictionary. Use when Codex must summarize a run, compare designs, freeze superseding results, prepare figures or tables, decide whether a fracture claim is mechanism-level or predictive, package processed writing assets, or prevent risk and numerical XFEM damage from being overstated.
---

# Simulation Evidence Reporting

## Reconstruct the evidence chain

Present geometry, ProCAST thermal source, Fluent melt/drainage and load
history, field transfer, Abaqus model, initiation morphology, local
damage/opening, energy quality and experiment comparison in that order. Keep
assumptions and measured inputs separate.

Read `references/claim-levels.md` before writing conclusions. Read
`references/result-data-dictionary.md` when freezing manuscript values or
superseding an earlier endpoint.

## Separate resolved and conditional statements

- Report directly resolved quantities with units and time.
- Label material, restraint, contact and fracture-energy brackets as
  assumptions or sensitivities until calibrated.
- Describe numerical XFEM activation as numerical damage onset, not guaranteed
  visible cracking.
- Distinguish risk suppression from crack elimination and local damage from
  complete rupture or pressure release.
- Separate an independent objective location/onset route from a primary
  full-growth route when they answer different validation questions.
- Treat topology-verified venting, reduced-order pressure feedback, and fully
  coupled pressure relief as different evidence levels.

## Freeze one canonical result set

1. Assign one accepted role to each route, such as screening, objective onset
   cross-check, primary growth, sensitivity, or visualization.
2. Declare when a newer endpoint supersedes an older interpretation while
   preserving the old result as intermediate evidence.
3. Build a machine-readable dictionary with quantity, value, unit, physical
   time, criterion, route, source, and claim status.
4. Verify dictionary values against authoritative CSV or JSON sources rather
   than reading numbers from figures.
5. Scan active skills and reports for stale claims that contradict the new
   accepted endpoint.

## Package for reuse

Include processed tables, figures, captions, methods/results text, claim
boundaries, source maps, plotting scripts and checksums. Exclude vendor solver
databases and private case data unless the recipient explicitly needs a restart
package and has the required licenses.
