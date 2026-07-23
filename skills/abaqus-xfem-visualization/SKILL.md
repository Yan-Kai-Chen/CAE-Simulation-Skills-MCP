---
name: abaqus-xfem-visualization
description: Render and validate publication-ready Abaqus XFEM figures with translucent reference geometry, fixed cameras, real crack coordinates, dedicated non-overlapping colorbars, and high-resolution PNG/PDF/SVG output. Use when STATUSXFEM, CSDMG, CRKOPEN, stress or crack-evolution plots are clipped, ambiguous, too small, visually misleading, or need a consistent paper style.
---

# Abaqus XFEM Visualization

## Render defensible geometry

Plot undeformed Shell context with a restrained translucent color. Plot spatial
crack paths only from actual STATUSXFEM element coordinates and verified face
connectivity. Keep CSDMG and CRKOPEN as scalar histories or distributions when
Abaqus internal crack-surface labels lack physical coordinates.

Read `references/figure-standard.md` before approving a figure set.

## Use fixed presentation rules

- Hold camera, crop and color range fixed across compared frames.
- Include top, underside, strict side and three-quarter views when spatial
  interpretation requires them.
- Put colorbars in dedicated layout bands.
- Use local insets instead of inflating crack markers until they imply false
  width.
- Apply display-only clipping only after asserting that no crack-result point
  is removed.

Use `scripts/xfem_figure_standard.py` for collision-aware saving and
`scripts/validate_xfem_figure_set.py` for output checks.

## Validate

Inspect final raster files at original resolution. Require at least 450 dpi,
matching vector output, no clipping or text collision, stable units and an
explicit distinction between connectivity-line width and physical crack width.
