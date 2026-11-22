from __future__ import annotations

import math
import random
from bisect import bisect_right
from dataclasses import dataclass
from itertools import accumulate, combinations
from typing import Any

from .radiation_geometry import Face, Geometry, Vector, angle_degrees, cross, dot, scale, subtract


@dataclass(slots=True)
class _RayBox:
    lower: Vector
    upper: Vector
    faces: list[int]
    children: tuple[_RayBox, _RayBox] | None = None


class _RayScene:
    def __init__(self, geometry: Geometry, epsilon: float | None):
        self.faces = geometry.faces
        invalid = [face.id for face in self.faces if face.area == 0]
        if invalid:
            raise ValueError(f"Repair degenerate faces before tracing rays: {', '.join(invalid[:10])}")
        size = math.hypot(*subtract(geometry.upper, geometry.lower))
        coordinate_scale = max(abs(x) for x in (*geometry.lower, *geometry.upper))
        self.epsilon = max(size * 1e-10, 8 * math.ulp(coordinate_scale)) if epsilon is None else epsilon
        if not math.isfinite(self.epsilon) or self.epsilon <= 0:
            raise ValueError("Ray epsilon must be finite and positive")
        self.root = self._build(list(range(len(self.faces))))

    def _build(self, indices: list[int]) -> _RayBox:
        patch = [self.faces[index] for index in indices]
        lower = tuple(min(face.lower[axis] for face in patch) for axis in range(3))
        upper = tuple(max(face.upper[axis] for face in patch) for axis in range(3))
        if len(indices) <= 8:
            return _RayBox(lower, upper, indices)
        axis = max(range(3), key=lambda dim: upper[dim] - lower[dim])
        indices.sort(key=lambda index: self.faces[index].center[axis])
        middle = len(indices) // 2
        return _RayBox(lower, upper, [], (self._build(indices[:middle]), self._build(indices[middle:])))

    def _intersects(
        self, box: _RayBox, origin: Vector, inverse: tuple[float | None, ...], far: float
    ) -> bool:
        near = self.epsilon
        for position, reciprocal, low, high in zip(origin, inverse, box.lower, box.upper):
            if reciprocal is None:
                if position < low or position > high:
                    return False
            else:
                first = (low - position) * reciprocal
                second = (high - position) * reciprocal
                near = max(near, min(first, second))
                far = min(far, max(first, second))
                if far < near:
                    return False
        return True

    @staticmethod
    def _hit_distance(face: Face, origin: Vector, direction: Vector) -> float | None:
        cross_ray = cross(direction, face.edge2)
        determinant = dot(face.edge1, cross_ray)
        if abs(determinant) <= face.area * 2e-12:
            return None
        displacement = subtract(origin, face.origin)
        u = dot(displacement, cross_ray) / determinant
        if u < -1e-10 or u > 1.0 + 1e-10:
            return None
        cross_edge = cross(displacement, face.edge1)
        v = dot(direction, cross_edge) / determinant
        if v < -1e-10 or u + v > 1.0 + 1e-10:
            return None
        return dot(face.edge2, cross_edge) / determinant

    def first_hit(
        self, origin: Vector, direction: Vector, source: int, far: float = math.inf
    ) -> int | None:
        inverse = tuple(1.0 / value if value else None for value in direction)
        nearest = None
        pending = [self.root]
        while pending:
            box = pending.pop()
            if not self._intersects(box, origin, inverse, far):
                continue
            if box.children is not None:
                pending.extend(box.children)
                continue
            for index in box.faces:
                if index == source:
                    continue
                distance = self._hit_distance(self.faces[index], origin, direction)
                if distance is not None and self.epsilon < distance < far:
                    nearest = index
                    far = distance
        return nearest


def face_angle_pairs(
    geometry: Geometry, pairs: list[tuple[str, str]], ray_epsilon: float | None = None
) -> list[dict[str, Any]]:
    """Evaluate facing and visibility between the centers of two named faces."""
    lookup = {face.id: index for index, face in enumerate(geometry.faces)}
    scene = _RayScene(geometry, ray_epsilon)
    output = []
    for source_id, target_id in pairs:
        if source_id not in lookup or target_id not in lookup:
            raise ValueError(f"Unknown face ID in pair {source_id!r}, {target_id!r}")
        first, second = lookup[source_id], lookup[target_id]
        source, target = geometry.faces[first], geometry.faces[second]
        vector = subtract(target.center, source.center)
        distance = math.hypot(*vector)
        if distance <= scene.epsilon:
            raise ValueError(f"Pair {source_id!r}, {target_id!r} has coincident face centers")
        direction = scale(vector, 1.0 / distance)
        emission_cos = dot(source.normal, direction)
        incidence_cos = -dot(target.normal, direction)
        hit = scene.first_hit(source.center, direction, first, distance + scene.epsilon)
        output.append({
            "source_face": source_id, "target_face": target_id, "distance": distance,
            "source_normal": source.normal, "target_normal": target.normal,
            "emission_angle_deg": angle_degrees(emission_cos),
            "incidence_angle_deg": angle_degrees(incidence_cos),
            "mutually_facing": emission_cos > 0 and incidence_cos > 0,
            "centerline_reaches_target": hit == second,
            "first_hit_face": geometry.faces[hit].id if hit is not None else None,
            "first_hit_group": geometry.faces[hit].group if hit is not None else None,
        })
    return output


def _basis(normal: Vector) -> tuple[Vector, Vector]:
    axis = (0.0, 0.0, 1.0) if abs(normal[2]) < 0.9 else (0.0, 1.0, 0.0)
    tangent = cross(axis, normal)
    tangent = scale(tangent, 1.0 / math.hypot(*tangent))
    return tangent, cross(normal, tangent)


def _emit_ray(face: Face, basis: tuple[Vector, Vector], rng: random.Random) -> tuple[Vector, Vector]:
    root = math.sqrt(rng.random())
    fraction = rng.random()
    w1, w2 = root * (1 - fraction), root * fraction
    radial_sq = rng.random()
    radial = math.sqrt(radial_sq)
    phi = math.tau * rng.random()
    x, y, z = radial * math.cos(phi), radial * math.sin(phi), math.sqrt(1 - radial_sq)
    tangent, bitangent = basis
    origin = tuple(p + w1 * e1 + w2 * e2 for p, e1, e2 in zip(face.origin, face.edge1, face.edge2))
    direction = tuple(x * a + y * b + z * n for a, b, n in zip(tangent, bitangent, face.normal))
    return origin, direction


def _wilson95(hits: int, trials: int) -> list[float]:
    p = hits / trials
    z = 1.959963984540054
    den = 1 + z*z / trials
    center = (p + z*z / (2 * trials)) / den
    radius = z / den * math.sqrt(p * (1 - p) / trials + z*z / (4 * trials*trials))
    return [max(0.0, center - radius), min(1.0, center + radius)]


def reciprocity_checks(
    factors: dict[str, dict[str, float]], areas: dict[str, float]
) -> list[dict[str, Any]]:
    result = []
    for source, target in combinations(sorted(factors.keys() & areas.keys()), 2):
        if target not in factors[source] or source not in factors[target]:
            continue
        forward = areas[source] * factors[source][target]
        reverse = areas[target] * factors[target][source]
        magnitude = max(abs(forward), abs(reverse))
        result.append({
            "first_group": source, "second_group": target,
            "area_times_forward": forward, "area_times_reverse": reverse,
            "absolute_difference": abs(forward - reverse),
            "relative_difference": abs(forward - reverse) / magnitude if magnitude else 0.0,
        })
    return result


def estimate_view_factors(
    geometry: Geometry,
    sources: list[str],
    rays: int = 8192,
    seed: int = 0,
    ray_epsilon: float | None = None,
) -> dict[str, Any]:
    """Estimate diffuse direct view factors by area and cosine-weighted first-hit sampling."""
    if rays < 1:
        raise ValueError("Rays per source must be positive")
    names = list(dict.fromkeys(sources))
    if not names:
        raise ValueError("Select at least one source group")
    if missing := set(names) - geometry.groups.keys():
        raise ValueError(f"Unknown radiation groups: {', '.join(sorted(missing))}")
    scene = _RayScene(geometry, ray_epsilon)
    faces = geometry.faces
    rng = random.Random(seed)
    areas = {name: math.fsum(faces[index].area for index in ids) for name, ids in geometry.groups.items()}
    factors: dict[str, dict[str, float]] = {}
    rows = {}
    for name in names:
        indices = geometry.groups[name]
        cumulative = list(accumulate(faces[index].area for index in indices))
        bases = [_basis(faces[index].normal) for index in indices]
        hit_counts = dict.fromkeys(geometry.groups, 0)
        emission_angles = dict.fromkeys(geometry.groups, 0.0)
        incidence_angles = dict.fromkeys(geometry.groups, 0.0)
        escaped = back_side = 0
        for _ in range(rays):
            slot = bisect_right(cumulative, rng.random() * cumulative[-1], hi=len(indices) - 1)
            index = indices[slot]
            origin, direction = _emit_ray(faces[index], bases[slot], rng)
            nearest = scene.first_hit(origin, direction, index)
            if nearest is None:
                escaped += 1
                continue
            receiver = faces[nearest]
            cosine = -dot(direction, receiver.normal)
            if cosine <= 0.0:
                back_side += 1
                continue
            target = receiver.group
            hit_counts[target] += 1
            emission_angles[target] += angle_degrees(dot(direction, faces[index].normal))
            incidence_angles[target] += angle_degrees(cosine)

        ordered_targets = sorted(hit_counts, key=lambda group: (-hit_counts[group], group))
        factors[name] = {target: hit_counts[target] / rays for target in ordered_targets}
        rows[name] = {
            "source_area": areas[name],
            "sum_view_factors": (rays - escaped - back_side) / rays,
            "escaped_rays": escaped, "escaped_fraction": escaped / rays,
            "back_side_hits": back_side, "back_side_fraction": back_side / rays,
            "receivers": {
                target: {
                    "view_factor": factors[name][target],
                    "hit_count": hit_counts[target],
                    "sampling_interval_95": _wilson95(hit_counts[target], rays),
                    "mean_emission_angle_deg": emission_angles[target] / hit_counts[target]
                    if hit_counts[target] else None,
                    "mean_incidence_angle_deg": incidence_angles[target] / hit_counts[target]
                    if hit_counts[target] else None,
                }
                for target in ordered_targets
            },
        }
    return {
        "analysis": "diffuse_first_hit_view_factor_estimate", "length_unit": geometry.length_unit,
        "area_unit": f"{geometry.length_unit}^2", "rays_per_source": rays, "seed": seed,
        "ray_epsilon": scene.epsilon, "group_areas": areas, "sources": rows,
        "reciprocity": reciprocity_checks(factors, areas),
    }
