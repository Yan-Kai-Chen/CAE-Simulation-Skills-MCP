---
name: abaqus-brittle-fracture-generalization
description: Screen brittle fracture risk from saved fields or choose and validate an Abaqus crack model. Use for thermal or contact load handoff, relative design comparison, crack initiation or growth, and evidence limits for brittle components.
---

# Abaqus Brittle Fracture Generalization

## Decide the required result

Choose the evidence needed for relative screening, initiation, path, opening,
loss of support, or residual performance. Use the [claim levels](references/feasibility-gates.md)
to match the model and conclusions to the available calibration and observations.

## Screen with the intact response

Use suitable existing thermal, contact, and stress fields when available. For
tensile-opening candidates, compare positive maximum principal stress over
matched regions and physical times. Use a volume-weighted upper percentile,
time-integrated volume above a declared stress threshold, and hotspot locations.
Retain the original maximum and inspect its distance from supports and contact edges.
Evaluate adjoining regions and parts when modifying a shared load path.

For shear- or compression-dominated failure, select indicators appropriate to
the mechanism. Compare candidates on consistent domains, units, time
coverage, and material assumptions. Record how any observed crack was used
during site selection or independent validation.

## Transfer fields and choose a crack model

Preserve geometry and mesh revision, coordinate frame, physical time, field
units and provenance. Match loads at the same physical time. Check surface
orientation and equivalent resultant for applied tractions. Assign each
contact load to a single source when the receiving model also solves contact.

Use [method selection](references/method-selection.md) for XFEM, cohesive,
VCCT, distributed damage, Explicit, or phase-field routes. Calibrate the
initiation and evolution law for the relevant mode and temperature. If a crack
changes support, flow or heat transfer, define the physical event and what
source boundary or calculation must be updated. Record whether the update uses
a prescribed reduced-order rule or a recomputed field.

## Run and interpret the required Abaqus analysis

Resolve the local Abaqus version and job files. Inspect the relevant run and
lock state before starting or resuming. For a new fracture model, review the
deck and datacheck output before the full solve. Use `.sta`, `.msg`, `.dat`
and the ODB to establish actual progress. Request the crack, opening, reaction
and energy outputs supported by the selected formulation. Assess mesh,
stabilization, connectivity and morphology at the event the task requires.

For a ceramic application, see [the core framework](references/ceramic-core-framework.md).
For local vendor integration, see [the adapter design](references/secondary-development.md).

The example case records an intact screening task. Run the contract checker
from this skill's directory.

```powershell
python scripts/validate_fracture_case_config.py references/example-ceramic-core-case.json
```

The checker verifies case fields and consistency between the objective, method
and claim. Explicit fracture models require an initiation law, an evolution
law, and a calibration status. The screening route uses elastic response and
permits missing fracture parameters.

## Deliverables

Report the method, time and region coverage, the supported claim level, and the
evidence needed to strengthen it. A screening delivery can end with comparative
stress metrics and hotspot locations. A crack-model delivery also records the
resolved event, model sensitivity and relevant validation.
