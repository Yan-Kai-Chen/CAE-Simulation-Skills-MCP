from __future__ import annotations

import argparse
import json
from typing import Any, Callable

from .abaqus import get_job_status
from .artifacts import index_artifacts
from .config import check_environment
from .procast import get_run_status, plan_pipeline


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
