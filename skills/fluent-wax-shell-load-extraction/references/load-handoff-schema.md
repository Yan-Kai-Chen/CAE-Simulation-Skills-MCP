# Fluent-to-Abaqus load handoff

Record:

- Fluent case, mesh and data artifact hashes;
- source wall zone and face-coordinate convention;
- physical times and source checkpoint names;
- resolved temperature/liquid-fraction/flow fields;
- pressure signal definition and quantile;
- PVT activation temperature, constitutive source and restraint parameter;
- drainage/connectivity release definition;
- coordinate transform and unit conversion;
- target Shell mesh, Wax-facing regions and load sign convention;
- interpolation method, neighbors, cutoff, coverage and distance statistics;
- generated amplitude/region tables and hashes;
- pressure activation, peak, exposure and high-load duration;
- limitations: reduced-order load, one-way coupling and uncalibrated
  parameters where applicable.

Do not silently interpolate across disconnected components or uncovered drain
openings. Do not replace a missing physical-time interval with a single held
frame.
