from procast_abaqus_agent.abaqus import get_job_status


def test_abaqus_completed_status(tmp_path):
    (tmp_path / "demo.sta").write_text(
        "INCREMENT 14\nTHE ANALYSIS HAS COMPLETED SUCCESSFULLY\n",
        encoding="utf-8",
    )
    result = get_job_status(tmp_path, "demo")
    assert result["state"] == "completed"
    assert result["last_increment"] == 14


def test_abaqus_minimum_increment_failure(tmp_path):
    (tmp_path / "demo.msg").write_text(
        "***ERROR: TIME INCREMENT REQUIRED IS LESS THAN THE MINIMUM SPECIFIED\n",
        encoding="utf-8",
    )
    result = get_job_status(tmp_path, "demo")
    assert result["state"] == "failed"
    assert result["fatal_count"] == 1
