---
name: fluent-wax-shell-load-extraction
description: Convert transient Fluent dewaxing outputs into traceable wax-to-Shell thermal and mechanical load histories using physical-time alignment, robust surface quantiles, regional aggregation, coordinate registration, drainage-release terms, and explicit Lee-PVT or restraint assumptions. Use when Codex must extract pressure-driving fields, transfer loads between nonmatching Wax and Shell meshes, create Abaqus amplitude tables, or distinguish resolved Fluent quantities from reconstructed contact loads.
---

# Fluent Wax-Shell Load Extraction

## Classify every quantity

Separate:

- Fluent-resolved temperature, liquid fraction, velocity, outlet flow, wall
  pressure and heat flux;
- derived drainage, connectivity and unreleased-expansion descriptors;
- reconstructed restrained-expansion/contact pressure;
- Abaqus-resolved Shell stress and fracture variables.

Never rename one class as another. In particular, native Fluent static pressure
is not automatically Wax-Shell contact pressure, and neither is Shell stress.

Read `references/load-handoff-schema.md` before generating a new Abaqus load
package.

## Build the physical-time history

1. Recover every accepted early frame needed by fracture initiation.
2. Use actual physical time from each Fluent checkpoint; do not infer time from
   file index when staged time steps are used.
3. Evaluate surface temperature and melt state on the Wax-facing boundary.
4. Use robust area-weighted quantiles for extreme loading; preserve the raw
   maximum only as a diagnostic.
5. Apply the documented restrained-expansion/PVT and drainage-release model
   only to quantities not solved directly.
6. Aggregate into geometry-defined Shell regions without adding a hotspot
   kernel that forces the expected crack location.

## Transfer between meshes

Register source and target coordinates, transform units, use k-nearest or
barycentric interpolation with a support cutoff, and export coverage and
nearest-distance statistics. Keep unmatched faces explicit.

## Validate the handoff

Check monotonic physical time, unit consistency, finite values, region
coverage, pressure sign, activation behavior, robust peak, exposure integral
and exact Abaqus amplitude timestamps. Hash every generated table.
