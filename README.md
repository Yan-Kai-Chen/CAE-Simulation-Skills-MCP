# ProCAST-Abaqus Batch MCP

Reusable Codex skills, deterministic batch utilities, and an optional
read-only MCP server for ProCAST-to-Abaqus engineering workflows.

The project does **not** distribute ProCAST, Visual-Environment, Abaqus,
Fluent, vendor APIs, licenses, meshes, solver databases, or research case
data. Users provide their own licensed installations and local configuration.

## Capability layers

1. **Skills** hold engineering workflow knowledge and evidence rules.
2. **Core Python** validates environment files, plans handoffs, reads solver
   status, and indexes processed artifacts without vendor dependencies.
3. **Optional MCP** exposes the same read-only capabilities to Codex and other
   MCP clients over stdio.
4. **Vendor adapters** remain explicit scripts invoked by the skills when the
   user has supplied licensed software and authorized execution.

## Included skills

- `procast-control-workflows`
- `procast-results-export`
- `procast-field-transfer`
- `abaqus-wax-shell-fracture`
- `abaqus-xfem-visualization`
- `procast-abaqus-coupling`
- `simulation-evidence-reporting`

See [the capability map](docs/capability-map.md) for the mapping from the 14
original project skills to these seven portable skills.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev,mcp]"
.\.venv\Scripts\procast-abaqus env-check --config examples/environment.example.json
.\.venv\Scripts\pytest
```

Start the optional MCP adapter:

```powershell
.\.venv\Scripts\procast-abaqus-mcp
```

The MCP server is deliberately read-only in version 0.1. Solver launch, stop,
restart, and vendor GUI/batch operations remain skill-directed actions with
explicit user authorization.

## License and repository

Copyright 2026 Yan-Kai Chen. Released under the [MIT License](LICENSE).

The intended public repository is
`Yan-Kai-Chen/ProCAST-Abaqus-Batch-MCP`. See
[the release checklist](docs/github-release-checklist.md).
