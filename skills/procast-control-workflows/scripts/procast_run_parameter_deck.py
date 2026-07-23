#!/usr/bin/env python3
"""Snapshot or patch scalar ProCAST p.dat run parameters."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def numeric_token(tokens: list[str]) -> tuple[int, float] | None:
    for index in range(len(tokens) - 1, 0, -1):
        try:
            return index, float(tokens[index])
        except ValueError:
            continue
    return None


def read_deck(path: Path) -> tuple[list[str], dict[str, dict[str, Any]]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    values: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(lines, start=1):
        tokens = line.strip().split()
        if len(tokens) < 2:
            continue
        key = tokens[0].upper()
        found = numeric_token(tokens)
        if found is None:
            continue
        token_index, value = found
        values[key] = {
            "value": value,
            "line": line_number,
            "tokens": tokens,
            "value_token_index": token_index,
        }
    return lines, values


def compact_snapshot(path: Path, values: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "input": str(path.resolve()),
        "parameter_count": len(values),
        "parameters": {key: item["value"] for key, item in sorted(values.items())},
    }


def format_like(original: str, value: float) -> str:
    if "e" in original.lower():
        precision = max(1, len(original.lower().split("e", 1)[0].split(".")[-1]))
        return f"{value:.{precision}e}"
    if "." in original:
        precision = len(original.split(".", 1)[1])
        return f"{value:.{precision}f}"
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def replace_value(line: str, token_index: int, new_value: float) -> str:
    newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
    body = line[: -len(newline)] if newline else line
    spans = []
    in_token = False
    start = 0
    for index, char in enumerate(body + " "):
        if not char.isspace() and not in_token:
            start = index
            in_token = True
        elif char.isspace() and in_token:
            spans.append((start, index))
            in_token = False
    if token_index >= len(spans):
        raise ValueError("Cannot locate value token in line: %s" % body)
    start, end = spans[token_index]
    replacement = format_like(body[start:end], new_value)
    return body[:start] + replacement + body[end:] + newline


def load_settings(path: Path) -> tuple[dict[str, float], dict[str, float]]:
    # Windows PowerShell 5.1 writes a UTF-8 BOM for ``-Encoding UTF8``.
    # ``utf-8-sig`` accepts both BOM and BOM-free JSON settings files.
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    raw_parameters = payload.get("parameters", payload)
    expected = payload.get("expected", {})
    if not isinstance(raw_parameters, dict) or not raw_parameters:
        raise ValueError("Settings must contain a non-empty 'parameters' object")
    parameters = {str(key).upper(): float(value) for key, value in raw_parameters.items()}
    expected_values = {str(key).upper(): float(value) for key, value in expected.items()}
    return parameters, expected_values


def command_snapshot(args: argparse.Namespace) -> None:
    source = Path(args.input)
    _lines, values = read_deck(source)
    Path(args.output).write_text(
        json.dumps(compact_snapshot(source, values), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def command_patch(args: argparse.Namespace) -> None:
    source = Path(args.input)
    destination = Path(args.output)
    settings = Path(args.settings)
    lines, before = read_deck(source)
    changes, expected = load_settings(settings)

    missing_expected = sorted(set(expected) - set(before))
    missing_changes = sorted(set(changes) - set(before))
    if missing_expected or missing_changes:
        raise KeyError(
            "Missing parameters: expected=%s changes=%s"
            % (missing_expected, missing_changes)
        )
    mismatches = {
        key: {"expected": value, "actual": before[key]["value"]}
        for key, value in expected.items()
        if not math.isclose(before[key]["value"], value, rel_tol=1e-9, abs_tol=1e-12)
    }
    if mismatches:
        raise ValueError("Input expectation mismatch: %s" % json.dumps(mismatches))

    for key, value in changes.items():
        item = before[key]
        line_index = item["line"] - 1
        lines[line_index] = replace_value(lines[line_index], item["value_token_index"], value)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("".join(lines), encoding="utf-8", newline="")
    _new_lines, after = read_deck(destination)
    report = {
        "input": str(source.resolve()),
        "output": str(destination.resolve()),
        "settings": str(settings.resolve()),
        "changes": {
            key: {"before": before[key]["value"], "after": after[key]["value"]}
            for key in changes
        },
        "verified": all(
            math.isclose(after[key]["value"], value, rel_tol=1e-9, abs_tol=1e-12)
            for key, value in changes.items()
        ),
    }
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser("snapshot")
    snapshot.add_argument("--input", required=True)
    snapshot.add_argument("--output", required=True)
    snapshot.set_defaults(func=command_snapshot)

    patch = subparsers.add_parser("patch")
    patch.add_argument("--input", required=True)
    patch.add_argument("--settings", required=True)
    patch.add_argument("--output", required=True)
    patch.add_argument("--report")
    patch.set_defaults(func=command_patch)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
