# ProCAST Enclosure Radiation and View Factors

Use the geometry route to assess surface orientation, facing angles and
potential shadowing before a thermal run. Use the native route to inspect the
actual ProCAST radiation groups and coefficients from a computed state.
The CLI analyzes geometry and exported tables on the current workstation.

## 1. Set up and inspect the cavity

1. Identify the participating surface regions, openings, workpieces and
   opaque obstructions. Record the common coordinate system, length unit,
   and geometry state. Distinguish furnace wall surfaces from solid parts.
2. In Visual-Cast, use Enclosure Radiation for the cavity surfaces and the
   relevant Heat conditions with View Factors enabled. Confirm the emitting
   and receiving sides, wall temperatures or histories, and emissivities.
3. Check winding and disconnected or degenerate regions in Visual-Mesh.
   The furnace's interior radiating boundary faces into the cavity. A solid
   workpiece surface faces toward the surrounding cavity. Repeat the
   enclosure orientation check on the converted geometry after DataCAST
   when there is an enclosure error, a geometry edit, or a change of version.
   Check boundary and nonmanifold edges, shared-edge winding, and each closed
   component's signed volume. Inspect openings and concave regions separately.
4. For native view factors, check the actual case prefix and solver log
   for completed calculation or verified import. Use factors for the current
   scene and compatible solver/partition layout. An altered relative pose,
   enclosure mesh or moving boundary requires the appropriate geometry update.
   Consult the installed manual for motion triggers such as `VFTIME` and
   `VFDISP`. `RFREQ` controls radiosity updates. `ANGTOL` concerns grouping
   and is distinct from the actual ray angles reported below.

## 2. Compute angles and direct geometric view factors

The [indexed cube example](../examples/radiation_geometry.example.json)
shows the input. Supply a length unit, global coordinates and oriented
triangles, each with a unique face ID, three zero-based vertex indices and
a group name. The same manifest can reference ASCII or binary STL files by
group. STL coordinates are interpreted in the stated unit unless an explicit
scale is provided. Identical XYZ coordinates in STL inputs share vertices.
STL normals are derived from the vertex order.

For example, add this field to a geometry manifest to include a separate
obstruction exported in a different length unit.

```json
{
  "length_unit": "m",
  "stl": [
    {"path": "wall.stl", "group": "wall"},
    {"path": "obstruction_mm.stl", "group": "obstruction", "scale": 0.001}
  ]
}
```

Use the installed CLI from the repository root for the synthetic example.

```text
cae-simulation radiation-geometry --geometry examples/radiation_geometry.example.json --expect inward --pair bottom:1 top:1
cae-simulation radiation-view-factors --geometry examples/radiation_geometry.example.json --source bottom --source top --rays 12000 --seed 42
```

`radiation-geometry` reports closed-component orientation, invalid and
open edges, duplicates, and degenerate faces. Edge examples include the
vertex indices and the affected face IDs. Repeat `--enclosure-group`
to check only the named wall groups as one cavity. Omit `--expect` when
checking a mixed scene or open panels. The winding and signed-volume checks
assume no self-intersections. Use the geometric mesh check when surfaces cross.

Each `--pair` reports the center-to-center distance and the two angles
relative to the emitting and receiving normals. Zero degrees is head-on
and ninety degrees is grazing. The first hit along that centerline reveals
a possible blocker. Use ray sampling for the visibility of the full regions.

For a diffuse source the two visible differential areas contribute through
`cos(theta_source) * cos(theta_receiver) / (pi * distance^2)`. Integrating
over both surfaces and dividing by the source area gives the view factor.
Occluded and back-facing pairs contribute zero.

`radiation-view-factors` samples source triangles by area and uses
cosine-weighted diffuse rays. The nearest opaque hit determines the receiver.
It reports factors by group, conditional mean emission and incidence angles,
sampling intervals, and area reciprocity for pairs computed in both directions.
Escaping rays and back-side hits are reported separately, without scaling
the other fractions to fill their share. The interval measures Monte Carlo
sampling variation for the supplied geometry. Check the mesh, orientation,
openings and group selection before interpreting a deficit or a small
factor. For a changed pose, run the same groups on the new geometry and
compare the factors and intervals. [NASA first-hit method](https://ntrs.nasa.gov/citations/19690000038)

Read F(i → j) as the fraction of the radiation leaving i that reaches j
directly. For example, to compare the exposure of two workpiece regions to
a heater, use those regions as source groups and compare their factors to
the heater. The reciprocity relation explains the corresponding differences
in irradiation per unit area for a uniform heater radiosity. Report where
the fraction went when a shield is introduced and whether rays now hit the
shield or escape through an opening.

These are diffuse direct geometric factors. Use the native solution for
emissivity, temperatures, reflected exchange and resulting heat flux. In
the estimator, every supplied face can block a ray. A back-side hit is a
geometry or orientation clue, especially in an intended closed cavity.
Set `--ray-epsilon` in the stated length unit when gaps approach the
automatically chosen origin tolerance.

## 3. Export and interpret native factors with RDEBUG

1. Use a working case and record the solver version and selected scene.
   In the installed ProCAST 2022 Visual-Cast documentation under **Radiation
   Simulation Parameters**, `RDEBUG=2` requests the symmetrized face-to-group
   factors in `<prefix>radVF.usf`. `RDEBUG=3` also requests the
   pre-symmetrization row-sum error in `<prefix>VFserr.usf`. Confirm the
   option in the manual for the actual release and in the final solver input.
2. Run or read the authorized case at the required geometry state. For a
   stationary geometry check, a short isolated case only needs to reach
   successful factor generation and a readable debug field. Confirm the
   native factor message and the expected result file under that prefix.
3. Load the matching result in Visual-Viewer Cast and activate the USF field
   at the relevant state. In **Result Export**, use **Select Steps** for a
   selected state when enabled. Try the formats offered for that active
   field and verify that the export retains radiation face identity. Obtain
   `Face Groups`, `Face to Group n` and `Face to All Groups` for that same
   state. If the format supplies mapped or renumbered entities, retain the
   original face mapping or use a supported face-level report. Verify one
   face against the native display before joining exports. Record the state
   time when geometry moves. An interpolated nodal export needs an explicit
   mapping back to radiation faces before it can support face-area analysis.
4. Join the fields by verified radiation face ID into one CSV per state.
   Supply `face_id`, `Face Groups` or `source_group`, and columns named
   `Face to Group <id>`. Include `Face to All Groups` for a native row-total
   check and `area` for area weighting. Match the IDs of source and receiver
   groups when assigning physical names. Keep unknown or missing values
   visible during export and resolve them before creating the analysis CSV.

The CLI takes a face table. Use the installed Visual-Viewer Cast exporter or
query for the release-specific USF file. The
[worked CSV](../examples/radiation_rdebug.example.csv) is synthetic.

```text
cae-simulation radiation-rdebug --csv examples/radiation_rdebug.example.csv --closed-enclosure --complete-groups --area-unit m2
```

The report ranks the receiver groups, locates the maximum-coefficient
radiation face for each group and checks row totals. When area is supplied,
the mean for group `i` toward group `j` is
`sum(A_face * F_face_to_j) / sum(A_face)`. With no area, it reports
equal-face statistics. Use `--complete-groups` for an area-based reciprocity
check only when exported source groups cover the full exchange areas.
Use `--closed-enclosure` for the closure check when every receiving region
is represented in the scene and row totals. A subset of receiver columns can
legitimately sum below the native total. The default absolute sum tolerance
is for reporting, with `--sum-tolerance` available for the task.

Relate coefficient differences to the confirmed physical surfaces and their
motion or obstruction. Combine the direct factors with native temperature
and radiation outputs when assessing actual heating.
