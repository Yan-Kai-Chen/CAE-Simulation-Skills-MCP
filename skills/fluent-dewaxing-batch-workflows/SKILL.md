---
name: fluent-dewaxing-batch-workflows
description: Plan, launch, resume, monitor, and package transient Fluent wax-melting and dewaxing batches with isolated run folders, physical-time autosaves, staged fixed time steps, melt/drainage monitors, and reproducible completion records. Use when Codex must prepare or supervise one or many Fluent dewaxing cases, recover interrupted segmented runs, compare geometry variants fairly, or preserve complete histories for a later Shell-fracture handoff.
---

# Fluent Dewaxing Batch Workflows

## Freeze the case contract

Record mesh identity, material tables, phase-change interval, latent heat,
density/thermal-expansion model, viscosity assumption, gravity, outlet
behavior, wall-temperature source, initialization, solver controls and output
schedule before launching a batch.

Read `references/dewaxing-contract.md` when creating a new case family or
comparing variants.

## Run on physical time

1. Give each case a dedicated run directory and manifest.
2. Preserve startup resolution before increasing the fixed time step.
3. Change time step only at documented state gates such as average liquid
   fraction; do not call chunk switching CFL adaptivity.
4. Write monitors every accepted step and case/data checkpoints frequently
   enough to reconstruct the fracture-relevant interval.
5. Resume only from the newest validated case/data pair.
6. Keep one visible compact monitor per case when interactive supervision is
   requested.

Use the `get_fluent_run_status` MCP tool or the `fluent-status` CLI command for
read-only progress inspection. Keep solver start, stop and resume in explicit
vendor scripts.

## Compare batches fairly

Freeze material physics, thermal boundary source, initialization, monitor
definitions, physical endpoint and state-alignment rule. Record cell count,
wall area and integrated heat input because mesh differences can masquerade as
geometry performance.

Treat a single-wax model as an expansion/load-release model unless a gas/VOF
replacement phase is explicitly solved. Do not interpret fixed-domain liquid
fraction as remaining wax volume.

## Accept and package

Require a final physical time, final case/data pair, complete monitor history,
solver-health summary and inventory. Package restart-critical files separately
from processed tables and figures. Exclude raw solver payloads from a public
repository.
