---
name: procast-abaqus-coupling
description: Orchestrate end-to-end ProCAST-to-Abaqus engineering handoffs from case readiness and field export through coordinate registration, reduced pressure or temperature histories, Abaqus loading, XFEM extraction, comparison and reporting. Use when Codex must choose among the toolkit skills, build a coupled job plan, resume a multi-software workflow, or preserve traceability across case variants.
---

# ProCAST–Abaqus Coupling

## Build the handoff chain

1. Use `$procast-control-workflows` for case setup and solver state.
2. Use `$procast-results-export` for numerical or native result extraction.
3. Use `$procast-field-transfer` to normalize units, register meshes and create
   spatial/time-aligned load tables.
4. Freeze the handoff manifest before Abaqus model generation.
5. Use `$abaqus-wax-shell-fracture` for global initiation, local opening and
   design comparisons.
6. Use `$abaqus-xfem-visualization` for publication figures.
7. Use `$simulation-evidence-reporting` for claims and handoff records.

Read `references/handoff-schema.md` before creating a new coupled project.

## Preserve provenance

Every transformed field must identify source case, field, unit, source step and
time, registration transform, interpolation support, target region and output
hash. Keep project-specific material parameters and case labels in local
configuration, not in reusable skills or MCP tools.

## Use MCP selectively

Use the optional MCP server for read-only environment checks, pipeline plans,
solver-status snapshots and artifact indexes. Keep vendor execution and any
state-changing solver action in explicit skill-directed scripts.
