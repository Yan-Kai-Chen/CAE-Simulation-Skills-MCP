# Repository guidance

- Keep reusable skills free of workstation-specific absolute paths and private
  case identifiers.
- Never commit vendor binaries, licenses, solver databases, meshes, raw fields
  or experimental images without explicit publication clearance.
- Keep the core Python package read-only and vendor-independent.
- Preserve the ProCAST thermal -> Fluent melt/load -> Abaqus fracture meaning
  and physical-time chain.
- Require explicit user authorization before adding any MCP or CLI tool that
  starts, stops, restarts or modifies a solver job.
- Validate every skill with the Codex skill validator and run the complete test
  suite before release.
