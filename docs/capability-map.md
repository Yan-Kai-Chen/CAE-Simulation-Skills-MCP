# Capability map

Version 0.3 consolidates the established solver workflows plus six public-safe
CAD and meshing workflows into 16 portable skills.

| Source workflow | Portable skill | Role |
|---|---|---|
| NX safe edit | nx-safe-edit | Working-copy inspection and bounded edits |
| NX solid modeling | nx-solid-modeling | Primitives, booleans, transforms and CFD domains |
| NX surface repair | nx-surface-repair | Sew, heal, thicken and sheet closure |
| SolidWorks safe edit | solidworks-safe-edit | Controlled feature/dimension edits and STEP export |
| Reverse modeling | reverse-cad-modeling | STL/facet/B-Rep reconstruction |
| HyperMesh meshing | hypermesh-surface-meshing | Surface mesh, zones and quality handoff |
| procast-solver-setup-control | procast-control-workflows | Setup and persistence |
| procast-solver-launch-control | procast-control-workflows | Launch/status/stop contract |
| procast-production-run-control | procast-control-workflows | Target-step and restart |
| procast-post-export | procast-results-export | Numerical field export |
| procast-batch-wax-surface-extraction | procast-results-export | Batch/resume/completeness |
| procast-native-field-visualization | procast-results-export | Native frames and video |
| procast-fluent-wax-temperature | procast-field-transfer | Temperature mapping |
| procast-fluent-wax-contact-pressure | procast-field-transfer | Contact-pressure mapping |
| procast-spatial-correspondence | procast-field-transfer | Registration and sampling |
| procast-deformed-stl-export | procast-field-transfer | Deformed geometry |
| wax-melt-fluent | fluent-dewaxing-batch-workflows | Fluent run/resume/package |
| export-global-surface-physics-metrics | fluent-wax-shell-load-extraction | Global and wall histories |
| export-model-surface-distribution-statistics | fluent-wax-shell-load-extraction | Area-weighted fields |
| w11-cracking-risk | fluent-fracture-risk-metrics | Load/risk interpretation |
| wax-melt-single-case-risk-metrics | fluent-fracture-risk-metrics | Reproducible metrics |
| abaqus-lee-pvt-shell-fracture | abaqus-wax-shell-fracture | Objective onset and full-growth XFEM |
| abaqus-xfem-fracture-visualization | abaqus-xfem-visualization | Figures and validators |
| abaqus-shell-fracture-paper-workflow | simulation-evidence-reporting | Evidence hierarchy and data dictionary |
| procast-control-orchestrator | procast-fluent-abaqus-coupling | Cross-solver routing |

Private case labels, workstation paths, geometry, meshes, material values, and
raw solver outputs remain outside the portable skills.
