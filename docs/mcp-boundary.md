# MCP boundary

## Included in version 0.2

- environment JSON validation for ProCAST, Visual-Environment, Fluent and
  Abaqus;
- ProCAST pipeline-plan validation;
- ProCAST run-status parsing;
- Fluent monitor/result status parsing;
- Abaqus job-status parsing;
- physical-time pressure-risk metrics;
- processed-artifact indexing.

These seven functions are read-only, deterministic and independently testable.

## Intentionally excluded

- starting or stopping any solver;
- administrator elevation;
- GUI clicks or vendor sessions;
- editing VDB, Fluent case/data or Abaqus input decks;
- deleting locks or result files;
- running long exports or simulations.

Those actions remain explicit skill-directed scripts so consent, vendor state
and process ownership stay visible.

## Client configuration

After `pip install -e ".[mcp]"`, start `procast-fluent-abaqus-mcp`. The
implementation uses `mcp.server.fastmcp.FastMCP` over stdio.
