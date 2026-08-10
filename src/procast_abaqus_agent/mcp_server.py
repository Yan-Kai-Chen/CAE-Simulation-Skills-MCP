from __future__ import annotations

from .abaqus import get_job_status
from .artifacts import index_artifacts
from .config import check_environment
from .evidence import validate_evidence_dictionary
from .fluent import get_fluent_run_status
from .procast import get_run_status, plan_pipeline
from .risk import compute_pressure_risk_metrics


def build_server():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - exercised without optional dependency
        raise RuntimeError('Install the optional MCP dependency with: pip install -e ".[mcp]"') from exc

    server = FastMCP(
        "CAE Simulation Skills MCP",
        instructions=(
            "Read-only engineering tools for CAD/CAE environment checks, "
            "ProCAST/Fluent/Abaqus status inspection, pressure-risk metrics, "
            "artifact indexing, and evidence-dictionary validation."
        ),
    )
    server.tool()(check_environment)
    server.tool()(plan_pipeline)
    server.tool()(get_run_status)
    server.tool()(get_fluent_run_status)
    server.tool()(get_job_status)
    server.tool()(compute_pressure_risk_metrics)
    server.tool()(index_artifacts)
    server.tool()(validate_evidence_dictionary)
    return server


def main() -> None:
    build_server().run(transport="stdio")


if __name__ == "__main__":
    main()
