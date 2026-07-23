---
name: procast-control-workflows
description: Plan, configure, launch, monitor, stop, and restart isolated ProCAST solver workflows from VDB projects or p.dat decks. Use when Codex must inspect ProCAST settings, prepare a copied case, choose MPI ranks, perform a finite smoke run, advance to a target step, resume with INILEV and -skippre, or read solver status without affecting unrelated jobs.
---

# ProCAST Control Workflows

## Start with a plan

1. Load a machine-local environment JSON; never embed installation or case
   paths in reusable scripts.
2. Inspect the source VDB or copied `p.dat` before changing settings. Treat UNF
   files as results, not setup sources.
3. Create one isolated run root containing the copied model, generated solver
   inputs, logs and manifests.
4. Run plan-only validation before any vendor process starts.
5. Require explicit authorization for launch, stop or restart actions.

Read `references/control-contract.md` before a real solver operation.

## Route the request

- Read or patch transparent deck parameters with
  `scripts/procast_run_parameter_deck.py`.
- Resolve and validate installation paths with
  `scripts/resolve_procast_environment.ps1`.
- Read a run snapshot with `scripts/get_procast_solver_status.ps1` or the
  portable `procast-abaqus procast-status` command.
- Keep Visual-Cast VDB persistence, DataCAST preprocessing, solver launch,
  target-step stop and restart as distinct stages and manifests.

## Restart correctly

Select a step stored for every required active field, set `INILEV` to that
step, set `DT=0`, and launch the continuation with `-skippre`. Do not run normal
DataCAST over an existing result prefix because it can erase stored results.

## Finish with evidence

Classify the result as prepared, preprocessing, running, completed, failed or
stopped-after-progress. A successful startup smoke test is not a completed
production solve. Confirm that only the recorded process tree was stopped.
