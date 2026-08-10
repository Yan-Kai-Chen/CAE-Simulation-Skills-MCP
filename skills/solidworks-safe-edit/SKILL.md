---
name: solidworks-safe-edit
description: Inspect, create, modify, rebuild, save, and export SolidWorks models through controlled working copies and bounded COM or MCP adapters. Use when Codex must change dimensions, equations, features, materials, configurations, or geometry while preserving the original model, resolving targets uniquely, validating rebuild status, and producing portable STEP plus JSON and Markdown reports.
---

# SolidWorks Safe Edit

## Existing-model workflow

1. Copy the model into a dedicated output directory and never edit the source
   in place.
2. Inspect units, features, dimensions, equations, materials, configurations,
   and rebuild state.
3. Resolve the requested feature, dimension, equation, or configuration
   uniquely; stop instead of guessing.
4. Apply only the requested bounded edit through an approved adapter.
5. Rebuild and reject blocking errors.
6. Save to a non-existing output, export STEP, and write JSON plus Markdown
   reports describing targets, old/new values, rebuild, and exports.

For a new model, declare units and dimensions first, build only the requested
features, rebuild, save, export STEP, and report the resulting body and
bounding-box checks.

Do not expose unrestricted macro, Python, COM, or code execution as a public
MCP tool.
