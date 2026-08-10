# Vendor compatibility

The project contains version-aware engineering contracts for Siemens NX,
SolidWorks, HyperMesh, ProCAST, Visual-Environment, Fluent, and Abaqus. A
workflow demonstrated on one release is not a compatibility guarantee for all
releases.

Keep installation paths, permissions, launch commands, and license settings in
local configuration. Detect missing vendor APIs at runtime and fail with an
actionable message. Do not import vendor-only modules in the core package or
test suite.

When adding another release, record:

- software version and operating system;
- launcher, batch, journal, or adapter entry point;
- input/output formats and naming behavior;
- unit and coordinate behavior;
- permission or elevation requirement;
- one read-only preflight and one finite synthetic smoke result.
