from __future__ import annotations

import argparse
import json
from typing import Any, Callable

from .abaqus import get_job_status
from .artifacts import index_artifacts
from .config import check_environment
from .evidence import validate_evidence_dictionary
from .fluent import get_fluent_run_status
from .procast import get_run_status, plan_pipeline
from .radiation import estimate_view_factors, face_angle_pairs
from .radiation_geometry import check_cavity_normals, load_radiation_geometry
from .radiation_results import analyze_rdebug_csv
from .risk import compute_pressure_risk_metrics


def _emit(value: dict[str, Any]) -> int:
    print(json.dumps(value, indent=2, ensure_ascii=False))
    return 0


def _radiation_geometry(args: argparse.Namespace) -> dict[str, Any]:
    mesh = load_radiation_geometry(args.geometry)
    report = check_cavity_normals(mesh, args.enclosure_group, args.expect)
    if args.pair:
        report["angle_pairs"] = face_angle_pairs(mesh, args.pair, args.ray_epsilon)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cae-simulation")
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

    geometry = sub.add_parser("radiation-geometry", help="Check cavity normals and paired angles")
    geometry.add_argument("--geometry", required=True)
    geometry.add_argument("--enclosure-group", action="append")
    geometry.add_argument("--expect", choices=("inward", "outward"))
    geometry.add_argument("--pair", nargs=2, action="append", metavar=("SOURCE_FACE", "TARGET_FACE"))
    geometry.add_argument("--ray-epsilon", type=float)
    geometry.set_defaults(handler=_radiation_geometry)

    view = sub.add_parser("radiation-view-factors", help="Estimate diffuse direct view factors")
    view.add_argument("--geometry", required=True)
    view.add_argument("--source", action="append", required=True, help="Emitting group, repeatable")
    view.add_argument("--rays", type=int, default=8192, help="Random samples per emitting group")
    view.add_argument("--seed", type=int, default=0)
    view.add_argument("--ray-epsilon", type=float)
    view.set_defaults(handler=lambda a: estimate_view_factors(
        load_radiation_geometry(a.geometry), a.source, a.rays, a.seed, a.ray_epsilon
    ))

    rdebug = sub.add_parser("radiation-rdebug", help="Summarize exported face-to-group coefficients")
    rdebug.add_argument("--csv", required=True)
    rdebug.add_argument("--closed-enclosure", action="store_true")
    rdebug.add_argument("--complete-groups", action="store_true", help="Check reciprocity with areas")
    rdebug.add_argument("--sum-tolerance", type=float, default=0.01)
    rdebug.add_argument("--area-unit")
    rdebug.set_defaults(handler=lambda a: analyze_rdebug_csv(
        a.csv, closed_enclosure=a.closed_enclosure, complete_groups=a.complete_groups,
        sum_tolerance=a.sum_tolerance, area_unit=a.area_unit
    ))

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

    evidence = sub.add_parser("validate-evidence-dictionary")
    evidence.add_argument("--csv", required=True)
    evidence.set_defaults(handler=lambda a: validate_evidence_dictionary(a.csv))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    handler: Callable[[argparse.Namespace], dict[str, Any]] = args.handler
    if args.command.startswith("radiation-"):
        try:
            return _emit(handler(args))
        except (OSError, ValueError, TypeError) as exc:
            parser.error(str(exc))
    return _emit(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
