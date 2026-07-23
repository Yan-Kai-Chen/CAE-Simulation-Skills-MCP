# Vendor compatibility

The private validation history includes ProCAST 2022, Visual-Environment 18,
Fluent 2024 R1, Abaqus 2025 and Windows PowerShell. These versions demonstrate
one working route; they are not a compatibility guarantee.

Keep installation paths, administrator requirements and launcher commands in
local environment configuration. Detect missing vendor APIs at runtime and
fail with an actionable message. Do not import vendor-only modules in the core
package or test suite.

When adding support for another release, record:

- software version and operating system;
- launcher and batch entry points;
- result-field names and export behavior;
- permission/elevation requirement;
- one read-only preflight and one finite smoke result.
