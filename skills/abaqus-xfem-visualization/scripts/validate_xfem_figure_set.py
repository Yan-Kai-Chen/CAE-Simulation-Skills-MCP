#!/usr/bin/env python3
"""Validate required high-resolution XFEM clear-view deliverables."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


REQUIRED_SUFFIXES = (
    "top_plusZ_clear",
    "top_minusZ_clear",
    "top_views_clear",
    "top_evolution_clear",
    "side_views_clear",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--expected-dpi", type=float, default=500.0)
    parser.add_argument("--min-width", type=int, default=5000)
    parser.add_argument("--min-height", type=int, default=4000)
    parser.add_argument("--json-out")
    args = parser.parse_args()

    root = Path(args.directory)
    errors = []
    records = []
    for suffix in REQUIRED_SUFFIXES:
        png = root / f"{args.prefix}_{suffix}.png"
        pdf = png.with_suffix(".pdf")
        record = {"suffix": suffix, "png": str(png), "pdf": str(pdf)}
        if not png.is_file() or png.stat().st_size == 0:
            errors.append(f"missing or empty PNG: {png}")
            records.append(record)
            continue
        if not pdf.is_file() or pdf.stat().st_size == 0:
            errors.append(f"missing or empty PDF: {pdf}")
        with Image.open(png) as image:
            width, height = image.size
            dpi = image.info.get("dpi", (0.0, 0.0))
        record.update({"width": width, "height": height, "dpi": list(dpi)})
        if width < args.min_width:
            errors.append(f"{png.name}: width {width} < {args.min_width}")
        if height < args.min_height:
            errors.append(f"{png.name}: height {height} < {args.min_height}")
        if min(dpi) + 1.0 < args.expected_dpi:
            errors.append(
                f"{png.name}: embedded DPI {dpi} < {args.expected_dpi}"
            )
        records.append(record)

    result = {
        "schema": "xfem_figure_set_validation_v1",
        "directory": str(root),
        "prefix": args.prefix,
        "passed": not errors,
        "errors": errors,
        "files": records,
    }
    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
