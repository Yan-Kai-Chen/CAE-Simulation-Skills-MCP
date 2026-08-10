import json

from procast_abaqus_agent.config import check_environment


def test_environment_check_with_existing_commands(tmp_path):
    launcher = tmp_path / "procast.bat"
    batch = tmp_path / "vebatch.bat"
    abaqus = tmp_path / "abaqus.bat"
    for path in (launcher, batch, abaqus):
        path.write_text("test", encoding="utf-8")
    config = {
        "schema": "procast_abaqus_environment_v1",
        "procast": {"launcher": str(launcher)},
        "visual_environment": {"batch": str(batch)},
        "abaqus": {"command_path": str(abaqus)},
        "tools": {},
    }
    source = tmp_path / "environment.json"
    source.write_text(json.dumps(config), encoding="utf-8")
    result = check_environment(source)
    assert result["ready"] is True
    assert result["required_present"] == 3


def test_cae_environment_accepts_cad_and_meshing_groups(tmp_path):
    nx = tmp_path / "run_journal.exe"
    hypermesh = tmp_path / "hmbatch.exe"
    nx.write_text("test", encoding="utf-8")
    hypermesh.write_text("test", encoding="utf-8")
    config = {
        "schema": "cae_simulation_environment_v1",
        "nx": {"journal_runner": str(nx)},
        "hypermesh": {"batch": str(hypermesh)},
    }
    source = tmp_path / "environment.json"
    source.write_text(json.dumps(config), encoding="utf-8")
    result = check_environment(source)
    assert result["ready"] is True
    assert {item["group"] for item in result["checks"]} == {"nx", "hypermesh"}
