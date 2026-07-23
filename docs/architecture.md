# Architecture

## Engineering chain

```text
ProCAST thermal evidence
    -> coordinate/unit registration
    -> Fluent full-cycle melting, expansion and drainage
    -> Fluent-informed restrained-expansion pressure history
    -> Abaqus global XFEM initiation
    -> Abaqus local damage/opening
    -> evidence and Agent feedback
```

The three solvers answer different questions:

- ProCAST supplies accepted upstream thermal and casting-process evidence.
- Fluent resolves physical-time wax state, drainage and load release.
- Abaqus resolves Shell stress, XFEM connectivity, damage and opening.

No field may silently change meaning between stages.

## Software layers

```text
User / Codex
    |
    +-- Skills: workflow reasoning, physics and evidence contracts
    |
    +-- CLI: deterministic read-only checks and metrics
    |
    +-- MCP (stdio): the same read-only core as seven tools
    |
    +-- Vendor adapters: explicit ProCAST / VE / Fluent / Abaqus scripts
            |
            +-- Licensed local installations and private case data
```

Skills decide what constitutes a valid workflow. Core Python implements stable
vendor-independent reads. Vendor adapters remain explicit because they depend
on version, license, permissions and live solver state.

A future mutation-capable MCP must remain a separate package with an
authorization protocol, run ownership and process-identity checks.
