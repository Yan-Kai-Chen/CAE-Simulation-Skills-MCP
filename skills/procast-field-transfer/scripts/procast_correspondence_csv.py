#!/usr/bin/env python
"""Generic tabular point correspondence helper for ProCAST-derived workflows.

This script is intentionally data-format agnostic: it reads CSV/Parquet point
tables, applies a known or landmark-fitted rigid transform, performs k-nearest
neighbor lookup in the target cloud, and writes a correspondence table plus a
JSON manifest. ProCAST-specific parsers should prepare clean coordinate/field
tables before calling this helper.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported table format: {path}")


def write_table(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        frame.to_csv(path, index=False)
        return
    if suffix in {".parquet", ".pq"}:
        frame.to_parquet(path, index=False)
        return
    raise ValueError(f"Unsupported output table format: {path}")


def xyz(frame: pd.DataFrame, columns: Iterable[str]) -> np.ndarray:
    cols = list(columns)
    missing = [col for col in cols if col not in frame.columns]
    if missing:
        raise KeyError(f"Missing coordinate columns: {missing}")
    return frame[cols].to_numpy(dtype=np.float64)


def kabsch(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if source.shape != target.shape or source.ndim != 2 or source.shape[1] != 3:
        raise ValueError("Landmark source/target arrays must both be N x 3")
    if source.shape[0] < 3:
        raise ValueError("At least three landmark pairs are required")

    source_centroid = source.mean(axis=0)
    target_centroid = target.mean(axis=0)
    source_centered = source - source_centroid
    target_centered = target - target_centroid
    covariance = source_centered.T @ target_centered
    u, _, vt = np.linalg.svd(covariance)
    correction = np.eye(3)
    if np.linalg.det(vt.T @ u.T) < 0.0:
        correction[2, 2] = -1.0
    rotation = vt.T @ correction @ u.T
    translation = target_centroid - rotation @ source_centroid
    return rotation, translation


def load_transform(path: Path | None) -> tuple[np.ndarray, np.ndarray, dict]:
    if path is None:
        return np.eye(3), np.zeros(3), {"source": "identity_default"}
    data = json.loads(path.read_text(encoding="utf-8"))
    rotation = np.asarray(data.get("R", data.get("rotation")), dtype=np.float64)
    translation = np.asarray(data.get("t", data.get("translation")), dtype=np.float64)
    if rotation.shape != (3, 3):
        raise ValueError("Transform JSON must contain R/rotation as a 3x3 matrix")
    if translation.shape != (3,):
        raise ValueError("Transform JSON must contain t/translation as a length-3 vector")
    return rotation, translation, data


def load_landmark_transform(path: Path) -> tuple[np.ndarray, np.ndarray, dict]:
    frame = read_table(path)
    source_cols = ["source_x", "source_y", "source_z"]
    target_cols = ["target_x", "target_y", "target_z"]
    rotation, translation = kabsch(xyz(frame, source_cols), xyz(frame, target_cols))
    fitted = (rotation @ xyz(frame, source_cols).T).T + translation
    residual = np.linalg.norm(fitted - xyz(frame, target_cols), axis=1)
    meta = {
        "source": "landmark_kabsch",
        "landmark_count": int(len(frame)),
        "landmark_rms_distance": float(np.sqrt(np.mean(residual**2))),
        "landmark_p95_distance": float(np.percentile(residual, 95.0)),
        "landmark_max_distance": float(np.max(residual)),
    }
    return rotation, translation, meta


def query_knn(target_xyz: np.ndarray, query_xyz: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    try:
        from scipy.spatial import cKDTree
    except ImportError as exc:
        raise RuntimeError("scipy is required for kNN lookup; install scipy or run in the project Conda env") from exc

    tree = cKDTree(target_xyz)
    distances, indices = tree.query(query_xyz, k=k, workers=-1)
    if k == 1:
        distances = distances[:, None]
        indices = indices[:, None]
    return distances.astype(np.float64), indices.astype(np.int64)


def idw_sample(values: np.ndarray, indices: np.ndarray, distances: np.ndarray, power: float) -> np.ndarray:
    safe_distances = np.maximum(distances, 1.0e-12)
    weights = 1.0 / np.power(safe_distances, power)
    exact = distances <= 1.0e-12
    out = np.empty(indices.shape[0], dtype=np.float64)
    for row in range(indices.shape[0]):
        if exact[row].any():
            out[row] = values[indices[row][exact[row]][0]]
        else:
            w = weights[row]
            out[row] = float(np.sum(w * values[indices[row]]) / np.sum(w))
    return out


def confidence_from_distance(distance: np.ndarray, strict: float, max_distance: float | None) -> np.ndarray:
    confidence = np.full(distance.shape, "interpolated", dtype=object)
    confidence[distance <= strict] = "rigid_high"
    if max_distance is not None:
        confidence[distance > max_distance] = "failed"
    return confidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-points", required=True, type=Path)
    parser.add_argument("--target-points", required=True, type=Path)
    parser.add_argument("--query-points", type=Path, help="Defaults to --source-points")
    parser.add_argument("--source-xyz", nargs=3, default=["x", "y", "z"])
    parser.add_argument("--target-xyz", nargs=3, default=["x", "y", "z"])
    parser.add_argument("--query-xyz", nargs=3, default=None)
    parser.add_argument("--target-field", action="append", default=[], help="Target scalar field column to sample")
    parser.add_argument("--transform-json", type=Path)
    parser.add_argument("--landmark-pairs", type=Path, help="CSV/Parquet with source_x/source_y/source_z/target_x/target_y/target_z")
    parser.add_argument("--unit-scale", type=float, default=1.0, help="Scale applied to source/query coordinates before transform")
    parser.add_argument("--k", type=int, default=8)
    parser.add_argument("--power", type=float, default=2.0)
    parser.add_argument("--strict-distance", type=float, default=1.0)
    parser.add_argument("--max-distance", type=float)
    parser.add_argument("--out-table", required=True, type=Path)
    parser.add_argument("--out-manifest", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.k < 1:
        raise ValueError("--k must be >= 1")

    source = read_table(args.source_points)
    target = read_table(args.target_points)
    query = read_table(args.query_points) if args.query_points else source
    query_cols = args.query_xyz if args.query_xyz is not None else args.source_xyz

    missing_fields = [field for field in args.target_field if field not in target.columns]
    if missing_fields:
        raise KeyError(f"Missing target field columns: {missing_fields}")

    if args.landmark_pairs:
        rotation, translation, transform_meta = load_landmark_transform(args.landmark_pairs)
    else:
        rotation, translation, transform_meta = load_transform(args.transform_json)

    source_query_xyz = xyz(query, query_cols) * args.unit_scale
    target_points_xyz = xyz(target, args.target_xyz)
    predicted = (rotation @ source_query_xyz.T).T + translation
    distances, indices = query_knn(target_points_xyz, predicted, args.k)
    nearest_distance = distances[:, 0]
    nearest_index = indices[:, 0]
    confidence = confidence_from_distance(nearest_distance, args.strict_distance, args.max_distance)

    output = pd.DataFrame(
        {
            "query_row": np.arange(len(query), dtype=np.int64),
            "target_match_row": nearest_index,
            "source_x": source_query_xyz[:, 0],
            "source_y": source_query_xyz[:, 1],
            "source_z": source_query_xyz[:, 2],
            "target_pred_x": predicted[:, 0],
            "target_pred_y": predicted[:, 1],
            "target_pred_z": predicted[:, 2],
            "target_match_x": target_points_xyz[nearest_index, 0],
            "target_match_y": target_points_xyz[nearest_index, 1],
            "target_match_z": target_points_xyz[nearest_index, 2],
            "nearest_distance": nearest_distance,
            "interpolation_k": args.k,
            "method": "rigid_transform_knn_idw",
            "confidence": confidence,
        }
    )

    for field in args.target_field:
        values = target[field].to_numpy(dtype=np.float64)
        output[f"sampled_{field}"] = idw_sample(values, indices, distances, args.power)
        output[f"nearest_{field}"] = values[nearest_index]

    write_table(output, args.out_table)

    manifest = {
        "source_points": str(args.source_points),
        "target_points": str(args.target_points),
        "query_points": str(args.query_points or args.source_points),
        "out_table": str(args.out_table),
        "transform": {
            "R": rotation.tolist(),
            "t": translation.tolist(),
            "unit_scale": args.unit_scale,
            "metadata": transform_meta,
        },
        "knn": {
            "k": args.k,
            "power": args.power,
            "strict_distance": args.strict_distance,
            "max_distance": args.max_distance,
        },
        "distance_stats": {
            "count": int(len(output)),
            "p50": float(np.percentile(nearest_distance, 50.0)),
            "p95": float(np.percentile(nearest_distance, 95.0)),
            "max": float(np.max(nearest_distance)),
        },
        "confidence_counts": output["confidence"].value_counts().to_dict(),
        "target_fields": args.target_field,
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
