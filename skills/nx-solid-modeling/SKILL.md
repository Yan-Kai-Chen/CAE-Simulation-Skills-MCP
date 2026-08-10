---
name: nx-solid-modeling
description: Plan and validate controlled Siemens NX solid-modeling operations for CFD and CAE geometry preparation, including primitives, transforms, booleans, edge features, shell or thickness operations, and profile-based solids. Use when Codex must create or modify NX bodies through an approved journal or adapter with explicit units, selectors, expected topology, rebuild checks, and portable exports.
---

# NX Solid Modeling

Read `references/solid-operation-contract.md` before generating or executing a
modeling job.

## Workflow

1. Run NX preflight and preserve the original input.
2. Define one declarative operation contract with units, parameters, exact
   target/tool selectors, expected body state, and validation limits.
3. Test a new operation class on synthetic geometry first.
4. Execute a known, version-compatible journal through a local adapter.
5. Regenerate and validate body count, solid/sheet state, bounding box,
   dimensions, and topology.
6. Save the part, export Parasolid and optional STEP, and write JSON/Markdown
   reports with relative artifact paths.

## Operation families

- primitives: block, cylinder, sphere, cone;
- transforms: move, copy, rotate, mirror;
- booleans: subtract, unite, intersect;
- edge/wall operations: fillet, chamfer, shell, thicken, offset, plane cut;
- profiles: revolve, sweep, loft;
- CFD domains: outer domain minus device bodies.

Stop when selectors are ambiguous, units are missing, rebuild fails, expected
body state is wrong, or an export is empty.
