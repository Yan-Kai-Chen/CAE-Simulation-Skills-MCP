# GitHub release checklist

- [x] Confirm repository owner and final public name.
- [x] Select and add a public software license.
- [x] Review authorship and citation metadata.
- [x] Run `pytest` and `ruff check .` in a fresh environment.
- [x] Validate all seven skills with `quick_validate.py`.
- [x] Install the optional MCP dependency and list all five tools.
- [x] Run path, credential, large-file and proprietary-extension scans.
- [x] Confirm examples contain synthetic paths and no research data.
- [ ] Forward-test the orchestration and evidence-reporting skills.
- [ ] Test one read-only ProCAST preflight and one Abaqus status parse on a
      second workstation if available.
- [ ] Initialize remote only after the preceding checks pass.

Local validation was completed on 2026-07-23. The public target is
`Yan-Kai-Chen/ProCAST-Abaqus-Batch-MCP` under the MIT License. The remaining
unchecked validation items require a second licensed workstation.
