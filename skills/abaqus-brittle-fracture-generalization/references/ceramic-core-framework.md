# Ceramic-core fracture framework

## Applicable stages

The workflow can be adapted to ceramic cores during:

- drying, firing, sintering, machining, transport, and assembly;
- preheating and mould filling;
- metal flow impact, metallostatic loading, and buoyancy;
- solidification and cooling with metal-core-shell thermal mismatch;
- knockout, thermal shock, chemical leaching, or mechanical core removal.

Each stage needs a separate load contract. Do not combine peak loads from
different times into a fictitious simultaneous worst case unless that is an
explicit conservative envelope.

## Recommended model ladder

### A. Thermal and process history

Obtain temperature, pressure, contact state, and relevant kinematics from
ProCAST, Fluent, another solver, or experiments. Keep the physical time and
coordinate transformation. Record whether transfer is nodal, elemental,
surface-based, regional, or reduced-order.

### B. Intact global response

Use an intact thermo-mechanical history of the core and its necessary supports
or contact partners. Reuse adequate saved results. For tensile-opening risk,
track a volume-weighted upper percentile of positive maximum principal
stress, the integral of material volume above a declared stress threshold,
and hotspot locations across operating stages. Use contact pressure, slip,
displacement and thermal gradients to explain the load path. Add Weibull
analysis when the material data support its assumptions.

### C. Objective candidate selection

For an independent prediction, define zones from the numerical fields before
using crack observations for validation. For a retrospective comparison,
record any region chosen from an observed fracture and include adjoining
regions where the load could have shifted. Compare equivalent regions using
compatible meshes, material assumptions, time histories, and controls.

### D. Local fracture resolution

- XFEM: unknown dominant crack path in a reasonably continuous body.
- Cohesive zone: core/metal coating, joint, interface, or known thin ligament.
- VCCT: pre-cracked interface.
- Explicit damage: impact, fragmentation, or strong contact discontinuity.
- Phase field: multiple interacting cracks when research value justifies a UEL
  implementation.

Use a global-local or submodel route when a fine fracture mesh over the entire
core is unnecessary. Transfer displacements/temperatures consistently and
check that the local boundary is sufficiently far from the process zone.

### E. Event-driven continuation

If cracking changes a load-bearing contact, flow path, heat-transfer area, or
metal pressure distribution, stop at the event, update the coupled boundary
condition, and continue. Label a pressure-decay equation or stiffness-release
curve as reduced-order unless the source physics is recomputed.

### F. Validation

Prefer multiple independent observations:

- CT or sectioning for internal morphology;
- DIC or displacement/load measurements;
- acoustic emission for onset timing;
- fractography for origin and mode;
- instrumented bend/compression/thermal-shock tests for material calibration;
- repeated specimens for porosity and strength scatter.

## Material data hierarchy

For screening, obtain elastic and thermal response properties for the range
being analyzed. A fracture model additionally needs calibrated strength and
fracture energy or toughness appropriate to the mode. Depending on the
process, also consider:

- compressive and shear strength;
- mixed-mode fracture energy;
- high-temperature creep or stress relaxation;
- porosity, flaw population, and Weibull scatter;
- anisotropy from forming or printing;
- moisture-dependent or firing-dependent properties;
- rate dependence for impact or rapid thermal shock.

Room-temperature nominal values support a sensitivity study, not a predictive
high-temperature fracture claim.

## Difference from wax-shell cracking

The existing wax-shell workflow transfers well at the level of provenance,
candidate competition, XFEM evidence gates, ODB extraction, and reporting. It
does not transfer unchanged at the level of physics:

- core loads may be dominated by metal pressure, impact, buoyancy, support, and
  thermal mismatch rather than wax expansion;
- compression and shear may be important, so MAXPS alone can be insufficient;
- surrounding metal contact may evolve after cracking and require event-driven
  recoupling;
- a connected crack is not automatically a pressure vent;
- core failure may be statistical, so deterministic strength alone can miss
  specimen-to-specimen scatter.

## Recommended outputs

- global candidate ranking and sensitivity bands;
- onset time/load, location, mode, and connected morphology;
- crack length/area, opening, stiffness or reaction-force loss;
- contact redistribution and post-event load change;
- energy balance and stabilization/artificial energy ratios;
- mesh and parameter sensitivity;
- validation residuals against experiments.
