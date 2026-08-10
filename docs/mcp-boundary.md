# MCP boundary

## Included in version 0.3

- environment JSON validation for NX, SolidWorks, HyperMesh, ProCAST,
  Visual-Environment, Fluent, Abaqus, and helper tools;
- ProCAST pipeline-plan validation and run-status parsing;
- Fluent monitor/result status parsing;
- Abaqus job-status parsing;
- physical-time pressure-risk metrics;
- processed-artifact indexing;
- manuscript evidence-dictionary validation.

These eight functions are read-only, deterministic, and independently
testable.

## Intentionally excluded

- creating or modifying CAD geometry;
- running arbitrary journals, macros, Python, Tcl, COM, or vendor APIs;
- starting or stopping a solver;
- administrator elevation or GUI automation;
- editing solver databases, cases, decks, meshes, or results;
- deleting locks or files.

Those actions remain explicit skill-directed local adapters so user intent,
software version, license state, and process ownership stay visible.

## Client configuration

After `pip install -e ".[mcp]"`, start `cae-simulation-mcp`. The implementation
uses `mcp.server.fastmcp.FastMCP` over stdio. Historical console aliases remain
available in version 0.3.
