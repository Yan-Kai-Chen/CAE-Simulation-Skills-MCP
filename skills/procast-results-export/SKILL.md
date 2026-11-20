---
name: procast-results-export
description: Extract and visualize saved ProCAST fields by physical time, location, and unit. Use for temperature, contact pressure, stress tensors, displacement vectors, fixed-range contour frames, or comparison-ready datasets.
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

1. Resolve the current loadable result prefix, actual parts, and available
   field records. For a run in progress, select a coherent stored frame.
2. Choose and verify units and the node, element, or surface location of
   the exported quantity. Preserve stress components and signed displacement
   vectors when requested.
3. Match the field's saved steps to physical time, including restart segments.
   Select an explicit list from the actual records.
4. Export outside the source run. Record field, unit, location, requested
   and actual step/time, and the applicable row and value statistics.

For native media, run `scripts/start_ve_native_field_image_export.ps1` with the
current input, field, visible parts, saved steps, and legend range. Set the
animation increment and end so the exporter can reach every requested step.
Use a common range, camera and deformation scale for matched views.
For video, pass the actual step-to-time CSV to
`scripts/compose_procast_native_field_videos.py`.

## Validate

Check expected files, finite parsed data, actual units, and relevant samples.
For rendered media, check frame coverage, legend and decode. Verify apparently
empty or sentinel-like exports by refreshing the active contour and checking
the selected frame and format. Use the full tensor route when stress
components are needed.

For cross-case output, use [field transfer](../procast-field-transfer/SKILL.md)
to align physical times, units, regions, and mesh correspondence. Record
common coverage and any interpolation.
