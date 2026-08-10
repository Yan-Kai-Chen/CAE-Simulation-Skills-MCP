# Migration inventory

## Source findings

- Version 0.1 consolidated 14 ProCAST and Abaqus project workflows.
- Version 0.2 added the complete Fluent dewaxing, wax-to-Shell load, fracture
  risk, and three-solver coupling layer.
- Version 0.3 adds six existing public-safe CAD and meshing workflows: NX safe
  edit, NX solid modeling, NX surface repair, SolidWorks safe edit, reverse
  modeling, and HyperMesh surface meshing.
- The current public set contains 16 portable Codex skills and eight read-only
  MCP tools.

## Migration decisions

- Preserve workflow knowledge and evidence gates rather than copying
  workstation-specific execution scripts.
- Replace private paths with environment JSON, command arguments, and relative
  artifact references.
- Keep CAD mutation, meshing execution, solver execution, and GUI control in
  explicit local adapters.
- Add a generic evidence-dictionary contract and validator without publishing
  case-specific fracture values.
- Retain the historical Python import package and console aliases for version
  0.3 compatibility while changing the distribution and repository identity.

## Publication decisions

- Public owner/name: `Yan-Kai-Chen/CAE-Simulation-Skills-MCP`.
- License: MIT.
- Exclude raw geometry, meshes, solver databases, experiment images, private
  material data, and workstation configuration.
- Treat local licensed-software smoke tests as compatibility evidence rather
  than universal vendor support guarantees.
