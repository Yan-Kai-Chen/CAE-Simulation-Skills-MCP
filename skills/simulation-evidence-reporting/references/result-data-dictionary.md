# Result data-dictionary contract

Use one row per manuscript quantity. Required columns are:

- `id`: stable unique identifier;
- `category`: input, timing, pressure, damage, opening, topology, energy,
  validation, or scope;
- `quantity`: human-readable name;
- `value` and `unit`;
- `physical_time_s` when time applies;
- `criterion`: exact event or extraction definition;
- `route`: solver branch or evidence role;
- `claim_status`: accepted result, assumption, sensitivity, qualitative
  validation, reduced-order result, or not claimed;
- `source_id`: stable pointer resolved in a separate source table or README.

## Source priority

Prefer accepted machine-readable summaries, accepted continuous histories,
route-closure reports, parameter-evidence reports, and figures in that order.
Never recover exact numbers from raster plots when CSV or JSON exists.

## Supersession

When a newer calculation extends a historical endpoint, retain the earlier
values as intermediate evidence and explicitly state which conclusion is
superseded. Update the active skill, project state, paper-readiness file, data
dictionary, and one factual run log together.

## Validation

- Parse the CSV successfully.
- Require unique IDs and all required columns.
- Compare key numeric values directly with authoritative source files.
- Confirm every source exists in the private working project.
- Scan active documentation for stale contradictory conclusions.
- Keep private paths out of the public template; resolve them only in local
  project configuration.
