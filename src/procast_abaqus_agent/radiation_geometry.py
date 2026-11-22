from __future__ import annotations

import math
import struct
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

from .config import load_json

Vector = tuple[float, float, float]
Nodes = tuple[int, int, int]


def subtract(a: Vector, b: Vector) -> Vector:
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def scale(a: Vector, factor: float) -> Vector:
    return a[0] * factor, a[1] * factor, a[2] * factor


def dot(a: Vector, b: Vector) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vector, b: Vector) -> Vector:
    return a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]


def angle_degrees(cosine: float) -> float:
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


@dataclass(frozen=True, slots=True)
class Face:
    id: str
    group: str
    nodes: Nodes
    origin: Vector
    edge1: Vector
    edge2: Vector
    normal: Vector
    area: float
    center: Vector
    lower: Vector
    upper: Vector


@dataclass(frozen=True, slots=True)
class Geometry:
    length_unit: str
    faces: list[Face]
    groups: dict[str, list[int]]
    lower: Vector
    upper: Vector


def _point(values: Iterable[float]) -> Vector:
    x, y, z = (float(value) for value in values)
    if not all(math.isfinite(value) for value in (x, y, z)):
        raise ValueError("Expected three finite coordinates")
    return x, y, z


def _bounds(points: Iterable[Vector]) -> tuple[Vector, Vector]:
    columns = tuple(zip(*points))
    return (min(columns[0]), min(columns[1]), min(columns[2])), (
        max(columns[0]), max(columns[1]), max(columns[2])
    )


def _read_stl(source: Path) -> Iterator[tuple[Vector, Vector, Vector]]:
    raw = source.read_bytes()
    if len(raw) >= 84:
        count = struct.unpack_from("<I", raw, 80)[0]
        if len(raw) == 84 + count * 50:
            for item in struct.iter_unpack("<12fH", memoryview(raw)[84:]):
                yield _point(item[3:6]), _point(item[6:9]), _point(item[9:12])
            return

    text = raw.decode("utf-8-sig")
    if not text.lstrip().lower().startswith("solid"):
        raise ValueError(f"{source} is not a supported STL")
    vertices: list[Vector] = []
    for line in text.splitlines():
        fields = line.split()
        if not fields:
            continue
        key = fields[0].lower()
        if key == "vertex":
            vertices.append(_point(fields[1:]))
        elif key == "endfacet":
            if len(vertices) != 3:
                raise ValueError(f"{source} contains an invalid STL facet")
            yield vertices[0], vertices[1], vertices[2]
            vertices.clear()
    if vertices:
        raise ValueError(f"{source} has an incomplete STL facet")


def _named(value: Any, label: str) -> str:
    if type(value) not in (str, int) or not str(value).strip():
        raise ValueError(f"{label} must be a nonempty string or integer")
    return str(value).strip()


def load_radiation_geometry(path: str | Path) -> Geometry:
    """Load explicitly indexed triangles and optional named STL surfaces."""
    source = Path(path).expanduser().resolve()
    data = load_json(source)
    if data.get("schema", "radiation_geometry_v1") != "radiation_geometry_v1":
        raise ValueError("Expected radiation_geometry_v1")
    for key in ("vertices", "faces", "stl"):
        if not isinstance(data.get(key, []), list):
            raise ValueError(f"{key} must be an array")
    length_unit = _named(data.get("length_unit"), "length_unit")
    vertices = [_point(point) for point in data.get("vertices", [])]
    faces: list[Face] = []
    groups: dict[str, list[int]] = defaultdict(list)
    face_ids: set[str] = set()

    def add(face_id: str, group: str, nodes: Nodes) -> None:
        if face_id in face_ids:
            raise ValueError(f"Duplicate face ID {face_id!r}")
        a, b, c = (vertices[index] for index in nodes)
        edge1, edge2 = subtract(b, a), subtract(c, a)
        vector_area = cross(edge1, edge2)
        area = math.hypot(*vector_area) / 2.0
        if not math.isfinite(area):
            raise ValueError(f"Face {face_id!r} has a nonfinite area")
        normal = scale(vector_area, 0.5 / area) if area > 0 else (0.0, 0.0, 0.0)
        center = _point(start + (d1 + d2) / 3 for start, d1, d2 in zip(a, edge1, edge2))
        lower, upper = _bounds((a, b, c))
        groups[group].append(len(faces))
        faces.append(Face(face_id, group, nodes, a, edge1, edge2, normal, area, center, lower, upper))
        face_ids.add(face_id)

    for entry in data.get("faces", []):
        if not isinstance(entry, dict):
            raise ValueError("Each face must be an object")
        face_id = _named(entry.get("id"), "face ID")
        group = _named(entry.get("group"), f"group for {face_id}")
        indices = entry.get("nodes", [])
        if not isinstance(indices, list) or len(indices) != 3 or any(
            type(index) is not int or not 0 <= index < len(vertices) for index in indices
        ):
            raise ValueError(f"Face {face_id!r} needs three zero-based vertex indices")
        add(face_id, group, (indices[0], indices[1], indices[2]))

    stl_vertices: dict[Vector, int] = {}
    for entry in data.get("stl", []):
        if not isinstance(entry, dict):
            raise ValueError("Each STL input must be an object")
        group = _named(entry.get("group"), "STL group")
        stl_path = source.parent / _named(entry.get("path"), "STL path")
        prefix = _named(entry.get("id_prefix", stl_path.stem), "STL face ID prefix")
        factor = float(entry.get("scale", 1.0))
        if not math.isfinite(factor) or factor <= 0:
            raise ValueError(f"Scale for {stl_path} must be finite and positive")
        count = 0
        for count, triangle in enumerate(_read_stl(stl_path), start=1):
            ids = []
            for point in triangle:
                xyz = _point(scale(point, factor))
                if xyz not in stl_vertices:
                    stl_vertices[xyz] = len(vertices)
                    vertices.append(xyz)
                ids.append(stl_vertices[xyz])
            add(f"{prefix}:{count}", group, (ids[0], ids[1], ids[2]))
        if count == 0:
            raise ValueError(f"No triangles found in {stl_path}")

    if not faces:
        raise ValueError("Geometry contains no triangles")
    lower, _ = _bounds(face.lower for face in faces)
    _, upper = _bounds(face.upper for face in faces)
    return Geometry(length_unit, faces, dict(groups), lower, upper)


def check_cavity_normals(
    geometry: Geometry,
    group_names: list[str] | None = None,
    expected: str | None = None,
) -> dict[str, Any]:
    """Check connected, closed surfaces by edge winding and signed volume."""
    groups = list(dict.fromkeys(group_names or geometry.groups))
    if missing := set(groups) - geometry.groups.keys():
        raise ValueError(f"Unknown enclosure groups: {', '.join(sorted(missing))}")
    selected = sorted(index for name in groups for index in geometry.groups[name])
    faces = geometry.faces
    edges: dict[tuple[int, int], list[tuple[int, bool]]] = defaultdict(list)
    for index in selected:
        a, b, c = faces[index].nodes
        for start, end in ((a, b), (b, c), (c, a)):
            edges[min(start, end), max(start, end)].append((index, start < end))

    adjacency: dict[int, list[int]] = defaultdict(list)
    for owners in edges.values():
        first = owners[0][0]
        for other, _ in owners[1:]:
            if other != first:
                adjacency[first].append(other)
                adjacency[other].append(first)

    membership: dict[int, int] = {}
    components: list[list[int]] = []
    for index in selected:
        if index in membership:
            continue
        component = [index]
        label = len(components)
        membership[index] = label
        for current in component:
            for neighbor in adjacency[current]:
                if neighbor not in membership:
                    membership[neighbor] = label
                    component.append(neighbor)
        components.append(component)

    edge_issues: list[Counter[str]] = [Counter() for _ in components]
    edge_examples: list[dict[str, list[dict[str, Any]]]] = [defaultdict(list) for _ in components]
    for edge, owners in edges.items():
        if len(owners) == 1:
            issue = "open"
        elif len(owners) > 2:
            issue = "nonmanifold"
        elif owners[0][1] == owners[1][1]:
            issue = "same_direction"
        else:
            continue
        component = membership[owners[0][0]]
        edge_issues[component][issue] += 1
        examples = edge_examples[component][issue]
        if len(examples) < 10:
            examples.append({"nodes": edge, "face_ids": [faces[index].id for index, _ in owners]})

    results = []
    for number, indices in enumerate(components, start=1):
        patch = [faces[index] for index in indices]
        invalid = [face.id for face in patch if face.area == 0]
        issues = edge_issues[number - 1]
        duplicates = len(patch) - len({tuple(sorted(face.nodes)) for face in patch})
        volume = None
        orientation = "indeterminate"
        if not issues and not invalid and not duplicates:
            reference = patch[0].origin
            volume = math.fsum(
                dot(subtract(face.origin, reference), cross(face.edge1, face.edge2))
                for face in patch
            ) / 6.0
            if volume:
                orientation = "outward" if volume > 0 else "inward"
        results.append({
            "component": number, "face_count": len(patch), "example_face_id": patch[0].id,
            "groups": sorted({face.group for face in patch}),
            "open_edges": issues["open"], "nonmanifold_edges": issues["nonmanifold"],
            "same_direction_shared_edges": issues["same_direction"],
            "example_edge_issues": edge_examples[number - 1],
            "duplicate_faces": duplicates, "degenerate_faces": len(invalid),
            "example_degenerate_face_ids": invalid[:10],
            "signed_volume": volume, "orientation": orientation,
            "matches_expected": orientation == expected if expected else None,
        })
    return {
        "analysis": "cavity_normals", "length_unit": geometry.length_unit,
        "groups": groups, "face_count": len(selected), "components": results,
        "expected_orientation": expected,
        "all_components_match": all(row["orientation"] == expected for row in results)
        if expected else None,
    }
