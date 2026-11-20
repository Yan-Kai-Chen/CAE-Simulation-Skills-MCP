# ProCAST control contract

## Inputs

- environment JSON containing installation and tool paths;
- copied VDB or copied `p.dat`;
- case prefix, run root, compatible MPI layout and requested endpoint;
- the solver actions authorized for the current task.

## Applicable stages

For a new run, confirm inputs, persist the intended configuration, preprocess
with DataCAST, and launch and monitor to the requested endpoint. For an existing
run, enter at inspection, target stop, restart, or result handoff as needed.
Use the plan-only mode to inspect a new job configuration or uncertain paths.

## Required records

Preserve settings, logs, launch identity, and the manifests that correspond to
actions performed. Record the terminal condition and the physical time of the
last saved field used downstream. Follow the local installation requirements
for license, executable, and privilege settings.

## Parameter rules

Choose common storage levels when the intended restart or downstream
application requires them. Different cadences can be joined on their verified
physical times for postprocessing. Compare any changed VDB setting on reload.
