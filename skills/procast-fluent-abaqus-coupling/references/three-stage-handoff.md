# Three-stage fracture handoff

## Stage A: ProCAST to Fluent

- Export the accepted temperature history and source timestamps.
- Register nonmatching meshes and document coordinate/unit transforms.
- Validate coverage, unmapped drain openings and interpolation error.

## Stage B: Fluent dewaxing and load reconstruction

- Retain the dense early physical-time grid.
- Resolve melting, thermal expansion, drainage and load release.
- Declare which pressure quantities are solved and which are reconstructed.
- Export robust regional pressure histories and fracture-risk descriptors.

## Stage C: Fluent to Abaqus

- Preserve exact timestamps and load regions.
- Freeze Shell mesh, material/contact assumptions and supports.
- Screen global edge/root candidates before selecting a local submodel.
- Validate STATUSXFEM connectivity, damage, opening and energy histories.

## Evidence levels

The chain may support mechanism, morphology or comparative suppression claims.
It does not support calibrated crack time, through-thickness rupture or
pressure relief unless those quantities are independently demonstrated.
