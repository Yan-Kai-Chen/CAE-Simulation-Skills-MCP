# Migration inventory

## Source findings

- 14 project-local skills: 11 ProCAST and 3 Abaqus.
- 72 files and approximately 279 kB inside the original skill directories.
- 84 executable references across the skill text; all referenced basenames
  were found in the private project.
- 251 workstation/project absolute-path occurrences in the source skill tree.
- Python cache files were present in two source skills and are excluded here.
- No credential, API key, bearer token or private-key material was identified.

## Migration decisions

- Consolidate overlapping skills instead of publishing 14 path-heavy copies.
- Preserve representative portable scripts only.
- Replace private paths with environment JSON, command arguments and relative
  repository paths.
- Keep case-specific values as examples or private validation evidence.
- Exclude raw simulation data and all vendor software.

## Publication decisions

- Public owner/name: `Yan-Kai-Chen/ProCAST-Abaqus-Batch-MCP`.
- License: MIT.
- Decide whether proprietary-paper screenshots or B52-specific processed
  examples may be released;
- forward-test each skill in a clean Codex project;
- test vendor adapters on a second workstation and software version.
