---
name: procast-results-export
description: Export numerical fields and native visual media from completed ProCAST Visual-Viewer Cast results. Use when Codex must select PATRAN versus Abaqus export formats, extract temperature, contact pressure, stress or displacement every N steps, batch completed cases, render fixed-range native contour frames, compose videos, or validate export completeness.
---

# ProCAST Results Export

## Choose the route

- Use PATRAN `.ntl` for compact nodal temperature, Contact Pressure and
  validated displacement-vector rows.
- Use Abaqus `.inp + .asf` when full stress tensors, connectivity or packaged
  thermo-mechanical states are required.
- Use native Visual-Viewer rendering when the deliverable is a fixed-range
  contour image sequence or video rather than numerical data.

Read `references/field-format-policy.md` before selecting a format.

## Export

1. Resolve the loadable result entry and requested part visibility.
2. Normalize requested units before export.
3. Select an explicit ascending step list; preserve every-N cadence and include
   step zero when required.
4. Write outside the raw case folder.
5. Record input, field, unit, requested/actual step, output size and row/value
   statistics in a manifest.

For native media, run `scripts/start_ve_native_field_image_export.ps1`, then
`scripts/compose_procast_native_field_videos.py`. Supply installation paths via
environment variables or command arguments.

## Validate

Require expected file counts, nonempty outputs, finite parsed values, stable
units and successful image/video decoding. Inspect the first, middle and last
native frames at original resolution. Do not infer a field from an all-sentinel
or all-negative export; switch to the validated higher-fidelity format.
