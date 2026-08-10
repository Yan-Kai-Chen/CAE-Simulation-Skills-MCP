---
name: nx-safe-edit
description: Inspect and edit Siemens NX models through controlled working copies, exact selectors, rebuild checks, version-aware local adapters, and portable reports. Use when Codex must change an NX expression, feature, dimension, body, or configuration; regenerate a model; or export Parasolid or STEP without modifying the original file or exposing raw NXOpen execution.
---

# NX Safe Edit

## Workflow

1. Resolve the NX version and journal runner from local configuration.
2. Copy the input model into a dedicated run directory; never edit the source
   in place or overwrite an existing output.
3. Inspect units, bodies, features, expressions, dependencies, and bounding
   box before selecting an edit target.
4. Select targets by exact expression name, persistent identifier, or a
   reviewed geometric selector. Stop when zero or multiple entities match.
5. Execute only an approved journal or bounded adapter operation.
6. Regenerate the model and reject blocking update errors.
7. Save the edited part, export Parasolid or STEP as requested, and write JSON
   plus Markdown reports containing inputs, parameters, outputs, and checks.

## Boundaries

- Do not expose arbitrary Python, arbitrary journals, or raw NXOpen calls as
  unrestricted MCP tools.
- Test a new operation family on synthetic geometry before using it on a real
  model.
- Treat a geometry edit as successful only when rebuild, body count, units,
  bounding box, and required exports all pass.
