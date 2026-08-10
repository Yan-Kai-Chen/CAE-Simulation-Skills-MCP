# Architecture

## Engineering chain

```text
CAD creation / repair / reverse modeling
    -> surface and solver meshing
    -> ProCAST thermal and casting-process evidence
    -> coordinate, unit and mesh registration
    -> Fluent melting, expansion, drainage and load history
    -> Abaqus stress, XFEM damage, opening and venting
    -> evidence dictionary, figures and Agent feedback
```

Not every project uses every stage. The skills preserve stable contracts so a
workflow can start from accepted upstream geometry, thermal evidence, or a
solver-ready mesh without inventing the missing stages.

## Software roles

- Siemens NX and SolidWorks create or edit controlled working-copy geometry.
- Reverse modeling rebuilds rough or faceted inputs when direct repair is
  insufficient.
- HyperMesh prepares validated surface meshes and solver boundary naming.
- ProCAST supplies casting-process and accepted thermal evidence.
- Fluent resolves physical-time melt, drainage, and load-release behavior.
- Abaqus resolves structural stress and fracture evidence.

No handoff may silently change units, coordinates, boundary identity, physical
time, field meaning, or evidence level.

## Software layers

```text
User / Codex
    |
    +-- Skills: workflow reasoning, engineering contracts and claim boundaries
    |
    +-- CLI: deterministic read-only checks, metrics and validation
    |
    +-- MCP (stdio): the same read-only core as eight tools
    |
    +-- Local adapters: explicit CAD / meshing / solver scripts
            |
            +-- Licensed installations and private project data
```

Mutation-capable adapters remain outside the public MCP surface so version,
license, permissions, run ownership, and user intent remain visible.
