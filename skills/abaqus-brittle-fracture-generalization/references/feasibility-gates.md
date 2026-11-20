# Feasibility and claim gates

## Level 1: screening-ready

Required:

- defensible geometry, supports, unit system, and load envelope;
- elastic/thermal property ranges;
- mesh and boundary-condition sensitivity;
- objective risk metric.

Allowed claim: likely high-risk regions and comparative ranking.

## Level 2: mechanism-ready

Required in addition:

- justified fracture method and initiation/evolution law;
- resolved or traceable time-varying loads;
- connected crack morphology, energy, and numerical-quality checks;
- qualitative agreement with at least one independent observation.

Allowed claim: plausible initiation/growth mechanism and relative design
effect. Do not claim absolute failure probability or exact service life.

## Level 3: conditional engineering prediction

Required in addition:

- temperature- and process-relevant strength/fracture calibration;
- mesh-objective response over the relevant range;
- quantitative validation across more than one load/design/specimen condition;
- declared uncertainty and applicability domain.

Allowed claim: conditional engineering prediction within the calibrated range.

## Level 4: predictive deployment

Required in addition:

- independent validation set and acceptance thresholds;
- material/manufacturing scatter model;
- version-controlled automated pipeline and regression tests;
- monitored field performance or production correlation;
- change-control rules for geometry, material batch, mesh, solver release, and
  process window.

Allowed claim: predictive use inside the validated domain, with uncertainty.

## Stop or downgrade conditions

Downgrade the claim when any of the following remains unresolved:

- room-temperature properties are used for a high-temperature event;
- load timing or coordinate registration is uncertain;
- the initiation law excludes a likely dominant compression/shear mechanism;
- crack path changes materially with mesh, stabilization, or enrichment zone;
- artificial/viscous/kinetic energy is large enough to control the result;
- an observed crack location was used to place the only candidate zone;
- a reduced-order pressure/contact release is presented as two-way coupling;
- one specimen is used to claim deterministic ceramic strength;
- the solver ends before the event needed by the claim.
