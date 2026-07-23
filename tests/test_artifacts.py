from procast_abaqus_agent.artifacts import index_artifacts


def test_artifact_index_excludes_raw_by_default(tmp_path):
    (tmp_path / "figure.png").write_bytes(b"png")
    (tmp_path / "job.odb").write_bytes(b"odb")
    result = index_artifacts(tmp_path)
    assert result["all_file_count"] == 2
    assert result["indexed_file_count"] == 1
    assert result["excluded_raw_count"] == 1
