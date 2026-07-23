# Coupled handoff manifest

Record:

- source software/version, case ID and result artifact;
- source body/part, field, component semantics and units;
- exact source steps and physical times;
- unit conversion and coordinate transform;
- interpolation method, support cutoff and coverage statistics;
- target software/version, mesh/body/region and load convention;
- model assumptions, material/contact parameters and uncertainty bracket;
- generated files, hashes and validation outcomes.

Do not silently substitute temperature, contact pressure, Shell stress or wax
PVT pressure for one another. They answer different physical questions.
