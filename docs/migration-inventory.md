# Migration inventory

## Source findings

- The initial audit covered 14 project-local skills: 11 ProCAST and 3 Abaqus.
- 72 files and approximately 279 kB inside the original skill directories.
- 84 executable references across the skill text; all referenced basenames
  were found in the private project.
- 251 workstation/project absolute-path occurrences in the source skill tree.
- Python cache files were present in two source skills and are excluded here.
- No credential, API key, bearer token or private-key material was identified.
- The v0.2 audit added the mature Fluent dewaxing, wax-shell load extraction,
  pressure-risk metric, and three-solver coupling workflows. They were
  distilled into portable contracts without copying private case assets.

## Migration decisions

- Consolidate overlapping workflows into ten portable skills instead of
  publishing path-heavy copies.
- Preserve representative portable scripts only.
- Replace private paths with environment JSON, command arguments and relative
  repository paths.
- Keep case-specific values as examples or private validation evidence.
- Exclude raw simulation data and all vendor software.

## Publication decisions

- Public owner/name: `Yan-Kai-Chen/ProCAST-Abaqus-Batch-MCP`.
- License: MIT.
- Keep proprietary-paper screenshots and case-specific processed research
  examples outside the public repository.
- Forward-test each skill in a clean Codex project.
- Test vendor adapters on a second workstation and software version.
