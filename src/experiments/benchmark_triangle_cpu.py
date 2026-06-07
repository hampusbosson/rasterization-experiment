import time
import csv
from pathlib import Path

import numpy as np

from src.data.generate_polygons import generate_depth_curve_polygon
from src.algorithms.triangulation import triangulate_polygon
from src.algorithms.triangle_rasterizer import rasterize_triangles_edge_function


GRID_SIZES = [256, 512, 1024, 2048]
COMPLEXITIES = [20, 100, 300]
WARMUP_RUNS = 5
MEASURED_RUNS = 20

RESULTS_DIR = Path("results/raw")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def benchmark_triangle_cpu():
    output_file = RESULTS_DIR / "triangle_cpu_benchmark.csv"
    rows = []

    for size in GRID_SIZES:
        width = size
        height = size

        for complexity in COMPLEXITIES:
            xs, ys = generate_depth_curve_polygon(
                width=width,
                height=height,
                num_vertices=complexity,
                seed=42,
            )

            triangles = triangulate_polygon(xs, ys)

            # Numba compilation + warm-up
            for _ in range(WARMUP_RUNS):
                rasterize_triangles_edge_function(triangles, width, height)

            for run in range(MEASURED_RUNS):
                triangulation_start = time.perf_counter()
                triangles = triangulate_polygon(xs, ys)
                triangulation_end = time.perf_counter()

                rasterization_start = time.perf_counter()
                grid = rasterize_triangles_edge_function(triangles, width, height)
                rasterization_end = time.perf_counter()

                triangulation_ms = (
                    triangulation_end - triangulation_start
                ) * 1000
                rasterization_ms = (
                    rasterization_end - rasterization_start
                ) * 1000
                elapsed_ms = triangulation_ms + rasterization_ms
                covered_cells = int(np.sum(grid))

                rows.append({
                    "algorithm": "triangle_edge_function_cpu",
                    "grid_width": width,
                    "grid_height": height,
                    "polygon_complexity": complexity,
                    "run": run + 1,
                    "execution_time_ms": elapsed_ms,
                    "triangulation_time_ms": triangulation_ms,
                    "rasterization_time_ms": rasterization_ms,
                    "covered_cells": covered_cells,
                    "num_vertices": len(xs),
                    "num_triangles": len(triangles),
                })

                print(
                    f"size={size} complexity={complexity} "
                    f"run={run + 1}/{MEASURED_RUNS} "
                    f"triangulation={triangulation_ms:.3f} ms "
                    f"rasterization={rasterization_ms:.3f} ms "
                    f"total={elapsed_ms:.3f} ms "
                    f"covered={covered_cells} triangles={len(triangles)}"
                )

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "algorithm",
                "grid_width",
                "grid_height",
                "polygon_complexity",
                "run",
                "execution_time_ms",
                "triangulation_time_ms",
                "rasterization_time_ms",
                "covered_cells",
                "num_vertices",
                "num_triangles",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to: {output_file}")


if __name__ == "__main__":
    benchmark_triangle_cpu()
