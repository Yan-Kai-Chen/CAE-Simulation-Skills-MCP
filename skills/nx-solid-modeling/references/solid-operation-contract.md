# NX solid-operation contract

## Required fields

- schema and operation name;
- optional copied input part;
- output directory and model stem;
- unit system;
- operation parameters;
- exact target and tool selectors;
- whether source and tool bodies are retained;
- expected body count and solid/sheet state;
- required part and exchange-format outputs;
- dimensional, bounding-box, volume, and topology checks.

## Operation-specific requirements

- Transforms record axis, origin, matrix or angle, and copy/move intent.
- Booleans identify target and every tool uniquely and declare tool retention.
- Edge and face operations declare positive radius, angle, offset, or
  thickness and use reviewed selectors.
- Revolve, sweep, and loft jobs identify profiles, guides, axes, continuity,
  and expected solid/sheet output.
- Fluid-domain construction records which body is the outer domain and which
  device bodies are subtracted.

## Acceptance

Accept only when update succeeds, expected bodies exist, requested dimensions
and units match, outputs are non-empty, and reports contain all selectors and
parameters. Reject unexpected extra bodies, deleted targets, partial features,
or exports that do not reproduce the saved part state.
