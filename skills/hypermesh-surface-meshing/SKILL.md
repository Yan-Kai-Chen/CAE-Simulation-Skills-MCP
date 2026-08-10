---
name: hypermesh-surface-meshing
description: Plan, prepare, run, and validate controlled HyperMesh CFD surface-meshing workflows while preserving units, geometry scale, boundary-zone names, quality evidence, and solver handoff. Use when Codex must inspect imported CAD or STL, build a two-dimensional surface mesh, prepare a reviewed Tcl or Python batch adapter, diagnose HyperMesh meshing output, or hand a surface mesh to Fluent without publishing private geometry or workstation paths.
---

# HyperMesh Surface Meshing

Read `references/surface-meshing-contract.md` before generating a plan or
accepting a mesh.

## Prepare the run

1. Preserve the original geometry and work on a copied input.
2. Resolve the licensed HyperMesh runtime from user configuration or an
   environment file; never hard-code an installation path in the skill.
3. Inspect units, bounding box, component count, surface count, free edges,
   duplicate surfaces, and existing boundary names before choosing mesh size.
4. Write a declarative plan containing input, output, target size, element
   family, feature controls, zone-name mapping, and acceptance limits.
5. Generate Tcl or Python only from the reviewed plan. Keep arbitrary commands
   outside public MCP tools.

## Mesh and validate

- Default to a two-dimensional surface mesh. Create volume or boundary-layer
  meshes only when a separate, explicit downstream contract requests them.
- Convert the requested engineering size into the detected model unit before
  meshing.
- Preserve stable CFD names such as `inlet`, `outlet`, `wall`, `symmetry`, and
  interface names; record every rename.
- Report element and node counts, free edges, duplicate elements, normals,
  aspect ratio, skewness, minimum/maximum size, and failed faces.
- Save the model, exported solver mesh, plan, log, JSON manifest, and concise
  quality report under one run directory.

## Accept runtime evidence

Do not rely on process exit code alone. Require the expected completion marker,
non-empty declared outputs, a parsed quality report, and no fatal message. Some
licensed HyperMesh batch versions may return a nonzero process code after
writing valid outputs; record that code but let the complete evidence gate
decide acceptance.

## Handoff

Before Fluent import, verify zone names, units, surface orientation,
watertightness intent, and the absence of unintended 3D elements. Return a
portable manifest using relative artifact paths.
