# GitHub release checklist

- [x] Confirm owner and `CAE-Simulation-Skills-MCP` repository identity.
- [x] Retain the MIT License and update citation metadata.
- [x] Run the complete Python test suite and Ruff.
- [x] Validate all 16 skills with `quick_validate.py`.
- [x] Install the optional MCP dependency and list all eight tools.
- [x] Run environment, pressure-risk, artifact, and evidence-dictionary CLI
      smoke tests.
- [x] Run concise path, credential, proprietary-extension, and large-file
      scans.
- [x] Confirm examples contain only synthetic paths and values.
- [ ] Push through the required GitHub proxy and verify CI.
- [ ] Forward-test licensed local adapters on another workstation when
      available.

The second-workstation checks are useful compatibility evidence but are not a
release blocker for the portable skills and read-only core.
