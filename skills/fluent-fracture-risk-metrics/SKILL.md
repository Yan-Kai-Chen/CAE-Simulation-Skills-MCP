---
name: fluent-fracture-risk-metrics
description: Compute single-case physical-time fracture-driving descriptors from Fluent-informed wax-pressure histories, including activation pressure, robust peak, cumulative exposure, excess exposure, and threshold duration with linearly resolved crossings. Use when Codex must quantify a completed dewaxing case, select a fracture-relevant time window, compare a rapid screen with Fluent, or prepare reproducible pressure-risk tables without claiming that a risk metric is an actual crack prediction.
---

# Fluent Fracture Risk Metrics

## Use a declared pressure signal

Prefer an area-weighted extreme quantile such as P99.9 over a raw maximum when
mesh singularities or isolated faces dominate. State whether the signal is
Fluent pressure, Fluent-temperature/PVT-informed equivalent pressure, or a
different reduced-order load.

Read `references/metric-contract.md` before freezing thresholds or writing
claims.

## Compute on physical time

For pressure history `P(t)` report:

- activation pressure `P(T_a)` when a surface-temperature signal is supplied;
- robust peak `max P(t)` and its time;
- exposure `I_P = integral P(t) dt`;
- high-load duration `tau = integral H(P(t)-P_c) dt`;
- excess exposure `integral max(P(t)-P_c, 0) dt`.

Resolve threshold crossings linearly inside each interval. Require strictly
increasing physical time.

Use the `compute_pressure_risk_metrics` MCP tool or:

```text
cae-simulation pressure-risk --csv <history.csv> --pressure-column <column> \
  --threshold-mpa <value>
```

Add `--temperature-column` and `--activation-temperature-c` when the CSV
contains a matching surface-temperature history.

## Preserve the claim boundary

Use these metrics to localize and rank loading windows. They do not prove
crack initiation, crack growth or rupture. Promote the accepted history to
Abaqus XFEM and retain experiment morphology and energy-quality gates.
