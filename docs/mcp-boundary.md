# MCP boundary

## Included in version 0.1

- environment JSON validation;
- ProCAST pipeline-plan validation;
- ProCAST run-status parsing;
- Abaqus job-status parsing;
- processed-artifact indexing.

These functions are read-only, deterministic and independently testable.

## Intentionally excluded

- starting or stopping ProCAST/Abaqus;
- administrator elevation;
- GUI clicks or Visual-Environment sessions;
- editing VDBs or solver decks;
- deleting locks or result files;
- running long exports or simulations.

Those actions remain explicit skill-directed scripts. This keeps consent,
vendor state and process ownership visible to the user.

## Client configuration

After `pip install -e ".[mcp]"`, configure an stdio MCP server with command
`procast-abaqus-mcp`. The implementation uses the official Python SDK import
`mcp.server.fastmcp.FastMCP` and calls `run(transport="stdio")`.
