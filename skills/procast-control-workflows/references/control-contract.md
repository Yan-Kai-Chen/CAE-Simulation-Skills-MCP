# ProCAST control contract

## Inputs

- environment JSON containing installation and tool paths;
- copied VDB or copied `p.dat`;
- case prefix, run root, core count and finite target;
- explicit authorization state for solver mutations.

## Ordered stages

`preflight -> setup -> persistence check -> DataCAST -> launch -> monitor ->
target stop -> restart preparation -> -skippre continuation -> final status`

## Required records

Preserve settings, before/after snapshots, console logs, launch identity,
status snapshots, stop/restart manifests and the final process count. Treat
administrator mode as a machine-specific fallback rather than a universal
ProCAST requirement.

## Parameter rules

Keep thermal and mechanical storage frequencies aligned when downstream field
handoffs require common time levels. Change only requested settings. Reload the
saved VDB and compare values before launching a solve.
