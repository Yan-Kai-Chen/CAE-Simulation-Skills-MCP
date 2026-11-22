---
name: procast-control-workflows
description: Configure, run, diagnose, and resume ProCAST cases using VDB settings, DataCAST inputs, solver logs, and stored states. Use for step and output controls, MPI launch, progress, termination, failure analysis, or restart.
---

# ProCAST Control Workflows

Use the requested entry in the [ProCAST workflows](../../docs/procast-workflows.md).
For VDB geometry, material, and boundary edits, use
[model preparation](../procast-model-preparation/SKILL.md).

## Configure and launch

1. Resolve installed tools with `scripts/resolve_procast_environment.ps1` or
   the machine's configured environment. Identify the case prefix, VDB,
   generated solver inputs, intended endpoint, and MPI layout.
2. Read active physics, time limits, increments, field update cadence, and
   each output interval. Storage intervals expressed in steps need the
   actual step-to-time index for interpreting results. Save and reread
   changes in the VDB when Visual-Cast is the source. Use
   `scripts/procast_run_parameter_deck.py` for a copied `p.dat`.
3. Use a dedicated run directory. Inspect existing jobs and logs before
   launch. Use DataCAST at cold start or as a separate requested handoff.
   Pass verified preprocessed inputs only through a compatible local route.
   Launch, stop, and resume within the authorized task.
4. Confirm the reported MPI layout, first accepted step, and physical
   time in native logs. For a batch, retain a separate status and prefix
   for each case. Use a short run when the task calls for a startup check.

Read the [control contract](references/control-contract.md) for local execution.
The portable `cae-simulation procast-status` command and
`scripts/get_procast_solver_status.ps1` summarize existing logs. Attribute
processes to a run by its recorded launcher and case information.

## Diagnose the current segment

| Symptom | First evidence |
|---|---|
| Import or DataCAST failure | First error, current file prefix, current VDB assignments, and generated inputs |
| Startup stalls | Initialization log, license or MPI error, reported ranks, and CPU or file growth |
| View factors fail or a face sees no receivers | Check the converted enclosure and offending face using the [radiation workflow](../../docs/procast-radiation.md). |
| Repeated retries or shrinking increments | Accepted time versus attempted time, the iteration block, and one relevant saved-field check |
| Unexpected contact or frozen fields | Field activation, native frame times, selection and units, then actual motion and physical conditions |

Read the clock and termination reason from the matched segment. Record
completion, a target stop, or a failure with its first relevant evidence.
Report final accepted time and last saved time for each field needed downstream.

## Resume from stored state

Match mesh, inputs, solver version, and partition layout. Locate the state
actually saved for every required active field. For the validated ProCAST
restart route, set `INILEV` to that step and `DT=0` to reuse its increment,
then launch with `-skippre`. Guard the state files because normal DataCAST can
erase results. Verify the restart step and a subsequent accepted advance in
the new log. Follow the requested endpoint.
