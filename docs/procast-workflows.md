# ProCAST Workflows

Start with the artifact available for the task. A mesh or VDB can go through
preparation and solve, a run folder can go through monitoring or recovery,
and saved results can go straight to export.

| Workflow | Typical task | Skill | Handoff |
| --- | --- | --- | --- |
| Import and edit | Fix an import error, adjust a clearance or thickness, move a part, or replace a local mesh | [Model preparation](../skills/procast-model-preparation/SKILL.md) | Reopened VDB with measured dimensions, part assignments, and mesh checks |
| Set up and preprocess | Assign materials, process curves, supports, exchanges, and interfaces, then set time controls and field output | [Model preparation](../skills/procast-model-preparation/SKILL.md) and [solver control](../skills/procast-control-workflows/SKILL.md) | Verified VDB and DataCAST inputs for the chosen prefix, when requested |
| Run and resume | Start a case, follow progress, stop at a target, or continue from a stored state | [Solver control](../skills/procast-control-workflows/SKILL.md) | Run identity, actual MPI layout and progress, endpoint, and saved-state coverage |
| Diagnose and recover | Locate an import, conversion, MPI, iteration, contact, or saved-field issue | [Model preparation](../skills/procast-model-preparation/SKILL.md) and [solver control](../skills/procast-control-workflows/SKILL.md) | First failing stage, evidence, and the smallest applicable correction |
| Extract and compare | Export temperature, pressure, stress or displacement, compare cases, or create contour media | [Results export](../skills/procast-results-export/SKILL.md) and [field transfer](../skills/procast-field-transfer/SKILL.md) | Fields or visuals with units, locations, physical time, and common coverage |

## Handoff from an edited model

Specify the target surface and dimension, then pick a coordinate edit or a
topology change. A coordinate edit retains the original IDs only after the
mesh and entity assignments have been checked. A topology change needs
geometric correspondence and a review of reattached conditions. Measure the
saved copy and resolve relevant mesh or binding errors before preprocessing.

## Handoff from a solver run

Identify the case prefix and segment first. Use the native log to record the
actual solver target and reason for stopping. Record the final accepted step,
the last available frame for each requested field, and a restart step when
needed. These can be at different physical times. A restart uses a compatible
mesh, partition layout, and stored state for the active fields.

## Handoff to another model or comparison

Match time from the saved records before comparing cases or driving another
solver. Preserve field meaning and position: nodal contact pressure, a stress
tensor, and a displacement vector have different roles. For changed meshes,
verify spatial coverage and flag unsupported regions. Choose comparison
metrics according to the application and retain the corresponding region,
time range, and units.

## Enclosure radiation

The [general radiation workflow](procast-radiation.md) covers normal and
topology checks, actual ProCAST view factor generation, and `RDEBUG=2`
result export. Use the geometry CLI to compare orientation and shadowing
and the native table analyzer to compare computed face-to-group factors.

The [portable CLI and MCP](mcp-boundary.md) provide read-only planning,
inspection, and evidence tools. Model edits and licensed solver actions use
local, version-aware adapters. The repository's environment and job examples
use synthetic inputs.
