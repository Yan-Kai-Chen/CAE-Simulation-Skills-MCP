# Pressure-risk metric contract

Freeze:

- physical-time column and unit;
- pressure column, unit and physical meaning;
- spatial statistic and weighting;
- activation temperature and temperature statistic, if used;
- severe-load threshold and its rationale;
- integration interval;
- interpolation rule for threshold crossings;
- source file hash and output hash.

## Required output

- number of time samples;
- first/final time;
- activation time and pressure, when defined;
- peak pressure and time;
- total pressure exposure;
- duration above threshold;
- excess exposure above threshold.

## Claim limits

- Do not call equivalent pressure native contact stress.
- Do not mix pressure and Shell stress metrics under one symbol.
- Do not infer subframe crack time from a coarse Fluent sampling interval.
- Do not infer crack elimination from a reduced risk metric.
