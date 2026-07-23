from __future__ import annotations

from .abaqus import get_job_status
from .artifacts import index_artifacts
from .config import check_environment
from .procast import get_run_status, plan_pipeline


def build_server():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - exercised without optional dependency
        raise RuntimeError('Install the optional MCP dependency with: pip install -e ".[mcp]"') from exc

    server = FastMCP(
        "ProCAST-Abaqus Batch MCP",
        instructions=(
            "Read-only engineering tools for environment checks, pipeline planning, "
            "solver-status inspection, and processed-artifact indexing."
        ),
    )
    server.tool()(check_environment)
    server.tool()(plan_pipeline)
    server.tool()(get_run_status)
    server.tool()(get_job_status)
    server.tool()(index_artifacts)
    return server


def main() -> None:
    build_server().run(transport="stdio")


if __name__ == "__main__":
    main()
