# Secondary-development architecture

## Layered design

Keep the reusable framework independent of a particular case:

```text
case configuration
  -> environment/version adapter
  -> geometry and mesh adapter
  -> load and field-transfer adapter
  -> material/fracture model
  -> Abaqus deck builder
  -> job controller
  -> ODB extractor
  -> crack/topology analyzer
  -> evidence package
```

The portable layer may validate, plan, parse, compare, and report. Licensed
solver execution and private files stay in explicit local adapters.

## Stable data contracts

Every adapter should expose:

- schema and case version;
- unit system;
- source and target coordinate frames plus transform;
- physical-time basis and interpolation rule;
- mesh/geometry revision and hashes;
- source variable, region, aggregation, and missing-data policy;
- target set/surface and mapping quality metrics;
- assumption/calibration status.

Do not use filenames or screenshots as the only provenance record.

## Backend interfaces

Provide interchangeable backends rather than one monolithic script:

- `LoadAdapter`: ProCAST field, Fluent field, CSV/HDF5, experiment, or analytic
  history;
- `FractureBackend`: Standard XFEM, cohesive zone, VCCT, Explicit damage, or
  research UEL;
- `MaterialProvider`: deterministic, temperature-dependent, statistical, or
  calibrated material sets;
- `JobBackend`: datacheck, submit, monitor, restart, and collect; authorization
  remains explicit for state-changing operations;
- `ResultExtractor`: ODB field/history output and derived topology metrics;
- `EvidenceWriter`: manifest, plots, tables, hashes, and claim level.

Use Abaqus Python/CAE scripting for model construction when required and
`odbAccess` for result extraction. Isolate differences between Abaqus releases.
Prefer input-keyword generation for stable, reviewable features; use CAE APIs
where geometry/assembly operations genuinely need them.

## Pipeline states

1. `PRECHECKED`: environment, license, inputs, units, and transforms resolved.
2. `BUILT`: deck and manifest generated.
3. `DATACHECKED`: syntax, sets, sections, interactions, and output requests
   accepted.
4. `SOLVED`: requested event/time reached without disqualifying numerical
   evidence.
5. `EXTRACTED`: canonical tables and crack geometry produced.
6. `VALIDATED`: mesh, energy, sensitivity, and experimental checks evaluated.
7. `PACKAGED`: public-safe scripts/configuration separated from private data.

Persist the state and reason for every transition so interrupted work can be
resumed without guessing.

## Testing strategy

- unit-test transforms, interpolation, time alignment, connected-component
  logic, and derived metrics on synthetic meshes;
- retain golden input decks and manifests without private geometry;
- run an Abaqus datacheck smoke case for each supported release;
- maintain one tiny solve for each fracture backend;
- regression-test ODB extraction against frozen expected tables;
- verify that reports cannot promote a case above its evidence gate.

## Development roadmap

### Phase 0: portable contract

Generalize case configuration, environment discovery, hashes, and outputs.
This is low risk and directly reusable.

### Phase 1: ceramic-core screening

Add temperature-dependent material tables, thermal/contact load adapters,
global candidate generation, and Weibull screening. Feasibility is high.

### Phase 2: local crack backends

Parameterize XFEM and cohesive workflows, candidate windows, restart logic,
and ODB topology extraction. Feasibility is medium-high, governed mainly by
material calibration and solver robustness.

### Phase 3: event-driven coupling

Detect opening/support-loss events, update pressure/contact/thermal boundaries,
and continue. Feasibility is medium with sequential coupling.

### Phase 4: two-way coupled fracture

Recompute fluid/thermal fields as the crack changes the domain. Feasibility is
case-dependent and development cost is high; only implement when the decision
cannot be answered by one-way or event-driven coupling.

### Phase 5: user interface or MCP wrapper

Expose read-only planning, validation, status, and evidence tools first. Keep
solver submit/stop/restart operations as explicit local actions with clear
authorization and audit records.
