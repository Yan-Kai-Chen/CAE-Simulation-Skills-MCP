---
name: procast-model-preparation
description: Import and repair geometry or meshes, edit a ProCAST VDB, assign physical conditions, and verify DataCAST inputs. Use for part moves, clearance or thickness changes, local remeshing, material and interface setup, and import or preprocessing defects.
---

# ProCAST Model Preparation

Use the current geometry, mesh, or VDB to prepare a case with measurable
dimensions and traceable solver conditions. Resolve the installed Visual-Mesh,
Visual-Cast, and DataCAST version through the user's environment. Work on a
case copy with its required companion files and referenced libraries.

## Import and inspect

1. Confirm the source format, length unit, part scale, and expected volumes
   and groups. Keep referenced include files together when importing meshes.
2. For an import error, locate the first failing record. Check the element
   keyword, connectivity, node references, and any nonstandard exporter
   metadata. Scope a format repair to the affected records or metadata block.
3. Inspect the affected parts for disconnected cells, orphan nodes, duplicate
   faces, intersections, and degenerate or inverted elements. Check the role
   of free nodes and open edges before deleting them. A surface mesh or an
   intentionally separate body can legitimately have these features.

## Select a geometry edit

Record the target body or face group, original and requested dimension,
coordinate system, measurement direction, and adjacent surfaces to preserve.
For a gap, measure the intended opposing faces in the design direction.
Check edge or corner overlap separately when it matters to contact.

| Change | Prepare and verify |
| --- | --- |
| Node displacement or rigid part move | Resolve original IDs and confirm source coordinates. Include shared-node effects and any transition region. Check intended sizes, preserved connectivity, and affected cell quality. |
| Remesh, replace, merge, or split | Map the new bodies and faces by geometry and role. Rebind material, loads, constraints, interfaces, and radiation surfaces to the resulting entities. |

For a compatible VE18 local adapter, the coordinate edit uses
`VistaDb.ModelGetNodeFromID`, `GetVgPoint3Value(node, "Point")`,
`SetVgPoint3Value`, and `VExpMngr.ExportFile` in a loaded Visual-Cast session.
Confirm the installed API and the loaded model before writing coordinates.
After saving, reopen the VDB and remeasure the target and affected neighbors.

## Attach the physical model

- Associate the active volume with the intended material record. Check the
  units and temperature coverage of properties relevant to the analysis.
- Apply initial conditions, curves, and loads to the intended bodies, faces,
  or nodes. Check the time and temperature units, direction, and active time
  range. Record actual supports and any additional numerical locators.
- Identify both sides of each interface. Verify thermal exchange, mechanical
  contact assumptions, and connectivity separately. Record search settings
  alongside the independently measured geometric clearance.
- For a solve-ready handoff, run Data Checks and inspect the generated
  DataCAST mesh and condition assignments for the current prefix. Rebuild
  preprocessing after solver-relevant geometry changes. Use a fresh start for
  a changed mesh unless a compatible state-transfer procedure is established.

Return the output VDB, a change and measurement summary, and the relevant
warnings or preprocessing status. Use
[solver control](../procast-control-workflows/SKILL.md) for run settings,
launch, and restart.
