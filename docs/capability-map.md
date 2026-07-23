# Capability map

The private project accumulated 19 relevant local workflows. Version 0.2
consolidates them into 10 portable skills.

| Original project skill | Portable skill | Disposition |
|---|---|---|
| procast-control-orchestrator | procast-fluent-abaqus-coupling | Cross-solver routing |
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
| abaqus-lee-pvt-shell-fracture | abaqus-wax-shell-fracture | XFEM execution |
| abaqus-xfem-fracture-visualization | abaqus-xfem-visualization | Figures and validators |
| abaqus-shell-fracture-paper-workflow | simulation-evidence-reporting | Evidence hierarchy |

Private case labels, calibrated-looking constants and machine-recovery records
remain validation evidence, not public defaults.
