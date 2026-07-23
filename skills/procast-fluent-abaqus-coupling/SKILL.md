---
name: procast-fluent-abaqus-coupling
description: Orchestrate the complete ProCAST-Fluent-Abaqus fracture workflow from thermal-history export and mesh registration through full-cycle Fluent melting/drainage, physical-time wax-to-Shell load reconstruction, Abaqus XFEM initiation/opening, and evidence reporting. Use when Codex must plan or resume the three-software chain, assign fidelity by quantity of interest, preserve one physical-time axis, or trace a crack claim back to thermal, flow and mechanical source data.
---

# ProCAST-Fluent-Abaqus Coupling

## Route the workflow

1. Use `$procast-control-workflows` and `$procast-results-export` for ProCAST
   readiness and field extraction.
2. Use `$procast-field-transfer` to map the accepted thermal boundary onto the
   Fluent Wax mesh.
3. Use `$fluent-dewaxing-batch-workflows` for full-cycle melting and drainage.
4. Use `$fluent-wax-shell-load-extraction` to reconstruct the physical-time
   Wax-to-Shell load.
5. Use `$fluent-fracture-risk-metrics` to localize the structural window.
6. Freeze the handoff manifest.
7. Use `$abaqus-wax-shell-fracture` for global initiation and local
   damage/opening.
8. Use `$abaqus-xfem-visualization` and
   `$simulation-evidence-reporting` for figures and claims.

Read `references/three-stage-handoff.md` before starting a new coupled study.

## Assign fidelity by quantity

Treat ProCAST thermal fields and accepted material inputs as upstream evidence,
Fluent as the full-cycle melt/drainage and load-history resolver, and Abaqus as
the structural fracture resolver. A rapid Agent may bracket stages and
candidate regions, but it does not replace the retained high-fidelity solver
for a quantity whose acceptance gate it fails.

## Preserve clocks and provenance

Keep distinct process-risk, severe-area and local-fracture times. Never imply
that a later global proxy generated an earlier local crack event. Every
transformed field must retain source artifact, physical time, unit, transform,
interpolation support, target region and hash.

Use MCP for read-only checks, status, planning, risk metrics and artifact
indexes. Keep vendor solver mutations in explicit skill-directed scripts.
