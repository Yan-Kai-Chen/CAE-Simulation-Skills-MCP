import asyncio

from procast_abaqus_agent.mcp_server import build_server


def test_mcp_registers_read_only_tool_surface() -> None:
    tools = asyncio.run(build_server().list_tools())
    assert {tool.name for tool in tools} == {
        "check_environment",
        "plan_pipeline",
        "get_run_status",
        "get_fluent_run_status",
        "get_job_status",
        "compute_pressure_risk_metrics",
        "index_artifacts",
    }
    assert all(tool.description for tool in tools)
