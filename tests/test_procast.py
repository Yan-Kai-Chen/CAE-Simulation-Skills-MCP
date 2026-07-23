import json

from procast_abaqus_agent.procast import get_run_status, plan_pipeline


def test_pipeline_plan_blocks_unauthorized_solver_action(tmp_path):
    job = {
        "schema": "procast_pipeline_job_v1",
        "job_name": "blocked",
        "case": {"case_dir": "case"},
        "execution": {"plan_only": False, "authorized_solver_actions": False},
        "stages": {"solver_launch": {"enabled": True}},
    }
    source = tmp_path / "job.json"
    source.write_text(json.dumps(job), encoding="utf-8")
    result = plan_pipeline(source)
    assert result["valid"] is False
    assert result["blocked_stages"] == ["solver_launch"]


def test_pipeline_plan_preserves_case_prefix(tmp_path):
    job = {
        "schema": "procast_pipeline_job_v1",
        "job_name": "prefix",
        "case": {"case_dir": "case", "prefix": "132"},
        "execution": {"plan_only": True, "authorized_solver_actions": False},
        "stages": {},
    }
    source = tmp_path / "job.json"
    source.write_text(json.dumps(job), encoding="utf-8")
    assert plan_pipeline(source)["case"]["prefix"] == "132"


def test_procast_status_parses_step_and_fatal(tmp_path):
    (tmp_path / "132p.out").write_text(
        "Number of processors 8\nTIME STEP 12\nFATAL: synthetic failure\n",
        encoding="utf-8",
    )
    result = get_run_status(tmp_path, "132")
    assert result["last_step"] == 12
    assert result["state"] == "failed"
    assert result["fatal_count"] == 1
