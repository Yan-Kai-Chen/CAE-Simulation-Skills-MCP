# Fracture method selection

Select the numerical method from the failure event and available calibration,
not from software familiarity.

| Route | Best use | Main strength | Main limitation | Minimum calibration |
|---|---|---|---|---|
| Intact elastic/thermoelastic model | Global screening and candidate localization | Fast, stable, easy to compare | No discrete crack growth | Elastic and thermal properties; tensile/compressive limits |
| XFEM | Unknown initiation site and a few dominant cracks | Crack can cross the mesh without a prescribed seam | Branching/contact can be difficult; solution may depend on stabilization and enrichment zone | Initiation criterion plus fracture energy or traction-separation law |
| Cohesive surface/elements | Known interface, bond line, or likely crack corridor | Direct mixed-mode interface representation | Path is predeclared; cohesive mesh/process-zone requirements | Normal/shear strengths, mode-I/II energies, mixed-mode law |
| VCCT | Existing interfacial crack or delamination | Clear energy-release-rate interpretation | Requires a pre-crack and prescribed interface | Critical energy-release rates and mixed-mode relation |
| Smeared damage/CDP | Distributed cracking or bulk stiffness degradation | Robust engineering-scale response | Does not provide a unique physical crack surface | Tension/compression curves, damage evolution, mesh regularization |
| Abaqus/Explicit fracture | Impact, rapid thermal shock, severe contact, fragmentation | Handles discontinuity and contact well | Quasi-static use requires kinetic-energy control; small stable time increment | Rate-dependent strength/energy if rate matters |
| Phase field through UEL/UMAT | Multiple interacting or branching cracks in research studies | Natural nucleation and branching | High development, calibration, and compute cost; not a native turnkey workflow | Fracture energy, length scale, degradation law, implementation verification |

## Solver choice

- Prefer Abaqus/Standard for quasi-static mechanical or sequential
  thermal-mechanical fracture when convergence is controllable.
- Prefer Abaqus/Explicit for physically dynamic loading, extensive separation,
  repeated contact changes, or fragmentation.
- Do not make an implicit model look successful by excessive stabilization.
- Do not call a mass-scaled Explicit model quasi-static until kinetic energy,
  loading rate, and wave propagation have been checked.

## Geometry and elements

The component name does not determine the Abaqus element family. A ceramic
"shell" or "core" with meaningful through-thickness gradients is often a 3-D
solid model rather than an S4 shell model. Use continuum elements when crack
fronts, local thickness, contact, or thermal gradients through the section are
important. Demonstrate mesh objectivity around the fracture process zone.

## Load families to consider

- transient temperature and thermal gradients;
- constrained thermal expansion and mismatch;
- pressure, flow impact, buoyancy, and acceleration;
- metal/core/shell contact and support loss;
- gravity and handling loads;
- drying, firing, sintering, machining, or assembly residual stress;
- cyclic thermal or mechanical loads when life, rather than one event, is the
  actual decision.

Separate loads that are resolved by another solver from those reconstructed by
an equation of state, reduced-order model, empirical coefficient, or assumed
restraint.
