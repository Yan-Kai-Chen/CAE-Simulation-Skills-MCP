# Security and data policy

Never commit:

- license files, tokens, credentials or user profile configuration;
- ProCAST/Visual-Environment/Abaqus/Fluent binaries or proprietary modules;
- raw `.unf`, `.vdb`, `.asf`, `.odb`, Fluent `.cas.h5`/`.dat.h5`/`.msh.h5`,
  restart, or solver database files;
- private meshes, experiment photographs or unpublished material data;
- local absolute paths that reveal usernames or internal storage structure.

The `.gitignore` blocks common solver payloads. Release validation must also
scan file contents and Git history because ignore rules do not protect files
already committed.
