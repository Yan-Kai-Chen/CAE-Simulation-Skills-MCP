import json
import struct
from pathlib import Path

import pytest

from procast_abaqus_agent.radiation import estimate_view_factors, face_angle_pairs
from procast_abaqus_agent.radiation_geometry import check_cavity_normals, load_radiation_geometry
from procast_abaqus_agent.radiation_results import analyze_rdebug_csv


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
CUBE = EXAMPLES / "radiation_geometry.example.json"


def test_cube_orientation_and_facing_angles():
    scene = load_radiation_geometry(CUBE)
    report = check_cavity_normals(scene, expected="inward")
    assert report["all_components_match"]
    assert report["components"][0]["signed_volume"] == pytest.approx(-1.0)

    pair = face_angle_pairs(scene, [("bottom:1", "top:1")])[0]
    assert pair["distance"] == pytest.approx(1.0)
    assert pair["emission_angle_deg"] == pytest.approx(0.0)
    assert pair["incidence_angle_deg"] == pytest.approx(0.0)
    assert pair["centerline_reaches_target"]


def test_mixed_winding_is_detected_after_large_translation(tmp_path):
    data = json.loads(CUBE.read_text())
    data["vertices"] = [[coordinate + 1e9 for coordinate in point] for point in data["vertices"]]
    path = tmp_path / "moved.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert check_cavity_normals(load_radiation_geometry(path), expected="inward")[
        "all_components_match"
    ]

    data["faces"][0]["nodes"].reverse()
    path.write_text(json.dumps(data), encoding="utf-8")
    component = check_cavity_normals(load_radiation_geometry(path))["components"][0]
    assert component["same_direction_shared_edges"] == 3
    assert component["orientation"] == "indeterminate"
    assert all(
        "bottom:1" in edge["face_ids"]
        for edge in component["example_edge_issues"]["same_direction"]
    )


def test_diffuse_cube_factor_matches_opposing_unit_squares():
    scene = load_radiation_geometry(CUBE)
    result = estimate_view_factors(scene, ["bottom", "top"], rays=10000, seed=42)
    for source, target in (("bottom", "top"), ("top", "bottom")):
        row = result["sources"][source]
        assert row["sum_view_factors"] == 1.0
        assert row["back_side_hits"] == row["escaped_rays"] == 0
        assert row["receivers"][source]["view_factor"] == 0.0
        assert row["receivers"][target]["view_factor"] == pytest.approx(0.1998249, abs=0.015)
    assert len(result["reciprocity"]) == 1
    assert result["reciprocity"][0]["absolute_difference"] < 0.02


def test_blocker_and_open_scene_are_reported(tmp_path):
    path = tmp_path / "blocked.json"
    path.write_text(json.dumps({
        "length_unit": "m",
        "vertices": [[x, y, z] for z in (0, 0.5, 1) for x, y in ((0, 0), (2, 0), (0, 2))],
        "faces": [
            {"id": "s", "group": "source", "nodes": [0, 1, 2]},
            {"id": "b", "group": "blocker", "nodes": [3, 5, 4]},
            {"id": "t", "group": "target", "nodes": [6, 8, 7]},
        ],
    }), encoding="utf-8")
    geometry = load_radiation_geometry(path)
    pair = face_angle_pairs(geometry, [("s", "t")])[0]
    assert pair["mutually_facing"]
    assert pair["first_hit_face"] == "b"
    assert not pair["centerline_reaches_target"]
    row = estimate_view_factors(geometry, ["source"], rays=1000)["sources"]["source"]
    assert row["receivers"]["target"]["view_factor"] == 0
    assert row["receivers"]["blocker"]["view_factor"] > 0
    assert row["escaped_rays"] > 0
    assert row["sum_view_factors"] + row["escaped_fraction"] == pytest.approx(1.0)


def test_ascii_and_binary_stl_groups_share_coordinates(tmp_path):
    (tmp_path / "first.stl").write_text(
        "solid plate\nfacet normal 0 0 1\nouter loop\n"
        "vertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\n"
        "endloop\nendfacet\nendsolid plate\n",
        encoding="utf-8",
    )
    (tmp_path / "second.stl").write_bytes(
        b"triangle".ljust(80, b"\0") + struct.pack("<I12fH", 1, 0, 0, 1,
                                                  1000, 0, 0, 1000, 1000, 0, 0, 1000, 0, 0)
    )
    path = tmp_path / "parts.json"
    path.write_text(json.dumps({
        "length_unit": "m",
        "stl": [{"path": "first.stl", "group": "plate"},
                {"path": "second.stl", "group": "plate", "scale": 0.001}],
    }), encoding="utf-8")
    geometry = load_radiation_geometry(path)
    component = check_cavity_normals(geometry)["components"][0]
    assert component["face_count"] == 2
    assert component["open_edges"] == 4
    assert all(face.area == pytest.approx(0.5) for face in geometry.faces)


def test_rdebug_area_weighting_and_reciprocity():
    result = analyze_rdebug_csv(
        EXAMPLES / "radiation_rdebug.example.csv", closed_enclosure=True, complete_groups=True
    )
    assert result["weighting"] == "face_area"
    assert result["sum_mismatch_faces"] == result["closure_mismatch_faces"] == 0
    assert result["sources"]["1"]["receivers"]["2"]["mean"] == pytest.approx(0.25)
    assert result["sources"]["1"]["receivers"]["2"]["max_face_id"] == "101"
    assert result["reciprocity"][0]["absolute_difference"] == pytest.approx(0.0)


def test_rdebug_partial_columns_and_open_geometry_are_distinguished(tmp_path):
    path = tmp_path / "partial.csv"
    path.write_text(
        "face_id,Face Groups,Face to Group 2,Face to All Groups\n100,1.0,0.35,0.9\n",
        encoding="utf-8",
    )
    result = analyze_rdebug_csv(path)
    assert result["weighting"] == "equal_faces"
    assert result["sum_mismatch_faces"] == 1
    assert result["closure_mismatch_faces"] is None
    assert result["sources"]["1"]["receivers"]["2"]["mean"] == pytest.approx(0.35)
    assert analyze_rdebug_csv(path, closed_enclosure=True)["closure_mismatch_faces"] == 1
    with pytest.raises(ValueError, match="area column"):
        analyze_rdebug_csv(path, complete_groups=True)
