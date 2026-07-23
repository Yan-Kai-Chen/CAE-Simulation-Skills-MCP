# Dewaxing case contract

Record these fields for every case:

- case label and geometry hash;
- Fluent version and precision;
- cell count, wall-face count and monitored wall area;
- wax solidus, liquidus, latent heat, heat capacity, conductivity, viscosity
  and temperature-dependent density;
- gravity direction and any state-gated release;
- outlet pressure, reverse-flow and replacement-phase rules;
- wall-temperature source, units, spatial mapping and time interpolation;
- initialization state;
- startup time-step sequence and later state-gated fixed time steps;
- physical end time and engineering melt endpoint;
- monitor names, autosave cadence and checkpoint rules;
- core count, segmented-session length and restart policy;
- final case/data, monitor, manifest and package hashes.

## Minimum monitor families

- physical time, time step and iterations;
- average/max temperature;
- average/max liquid fraction;
- outlet mass flow and cumulative discharge;
- wall pressure or normal-load proxy;
- wall heat-transfer indicators;
- solver warnings and fatal messages.

## Interpretation gates

- Separate melting from literal void formation.
- Separate Fluent wall pressure from Shell stress.
- Preserve the early dense time grid used by downstream fracture analysis.
- Compare designs at matched physical state or state-aligned checkpoints when
  heat input or mesh resolution differs.
