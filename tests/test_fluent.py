from procast_abaqus_agent.fluent import get_fluent_run_status


def test_fluent_status_parses_latest_monitor_time(tmp_path):
    monitors = tmp_path / "monitors"
    monitors.mkdir()
    (monitors / "global_monitors.out").write_text(
        '"global_monitors"\n'
        '("Time Step" "flow-time" "delta-time" "temperature")\n'
        "0 0 0.1 293.15\n"
        "2 0.2 0.1 310.0\n",
        encoding="utf-8",
    )
    result = get_fluent_run_status(tmp_path)
    assert result["state"] == "progress_recorded"
    assert result["latest_flow_time_s"] == 0.2
    assert result["latest_time_step"] == 2.0
