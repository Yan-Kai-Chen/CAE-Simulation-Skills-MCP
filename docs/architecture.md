# Architecture

```text
User / Codex
    |
    +-- Skills: workflow reasoning, physics rules, authorization boundaries
    |
    +-- CLI: deterministic read-only environment/status/index utilities
    |
    +-- Optional MCP (stdio): the same read-only CLI capabilities as tools
    |
    +-- Vendor adapters: explicit VE/ProCAST/Abaqus scripts selected by skills
            |
            +-- Local licensed installations and private case data
```

Skills decide *what* a valid engineering workflow is. Core Python implements
small stable operations that do not need vendor imports. Vendor adapters are
kept explicit because they depend on installation version, permissions,
licenses and case state.

The architecture avoids turning a long-lived MCP process into a hidden solver
controller. A future mutation-capable server should be a separate package with
an authorization protocol, run ownership and process-identity checks.
