from __future__ import annotations

import argparse
import json
from typing import Any, Callable

from .abaqus import get_job_status
from .artifacts import index_artifacts
from .config import check_environment
from .fluent import get_fluent_run_status
from .procast import get_run_status, plan_pipeline
from .risk import compute_pressure_risk_metrics


def _emit(value: dict[str, Any]) -> int:
    print(json.dumps(value, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="procast-abaqus")
    sub = parser.add_subparsers(dest="command", required=True)

    env = sub.add_parser("env-check")
    env.add_argument("--config", required=True)
    env.set_defaults(handler=lambda a: check_environment(a.config))

    plan = sub.add_parser("pipeline-plan")
    plan.add_argument("--job", required=True)
    plan.set_defaults(handler=lambda a: plan_pipeline(a.job))

    procast = sub.add_parser("procast-status")
    procast.add_argument("--run-root", required=True)
    procast.add_argument("--prefix", required=True)
    procast.set_defaults(handler=lambda a: get_run_status(a.run_root, a.prefix))

    abaqus = sub.add_parser("abaqus-status")
    abaqus.add_argument("--job-dir", required=True)
    abaqus.add_argument("--job-name", required=True)
    abaqus.set_defaults(handler=lambda a: get_job_status(a.job_dir, a.job_name))

    fluent = sub.add_parser("fluent-status")
    fluent.add_argument("--run-root", required=True)
    fluent.set_defaults(handler=lambda a: get_fluent_run_status(a.run_root))

    risk = sub.add_parser("pressure-risk")
    risk.add_argument("--csv", required=True)
    risk.add_argument("--time-column", default="time_s")
    risk.add_argument("--pressure-column", required=True)
    risk.add_argument("--threshold-mpa", type=float, required=True)
    risk.add_argument("--temperature-column")
    risk.add_argument("--activation-temperature-c", type=float)
    risk.set_defaults(
        handler=lambda a: compute_pressure_risk_metrics(
            a.csv,
            a.pressure_column,
            a.threshold_mpa,
            a.time_column,
            a.temperature_column,
            a.activation_temperature_c,
        )
    )

    artifacts = sub.add_parser("index-artifacts")
    artifacts.add_argument("--root", required=True)
    artifacts.add_argument("--include-raw", action="store_true")
    artifacts.set_defaults(handler=lambda a: index_artifacts(a.root, a.include_raw))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    handler: Callable[[argparse.Namespace], dict[str, Any]] = args.handler
    return _emit(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
