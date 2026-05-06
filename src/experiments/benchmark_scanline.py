import time
import csv
from pathlib import Path
import numpy as np
from src.algorithms.scanline_rasterizer import scanline_fill_et_ael
from src.data.generate_polygons import generate_depth_curve_polygon


GRID_SIZES = [256, 512, 1024, 2048]
COMPLEXITIES = [20, 100, 300]
WARMUP_RUNS = 5
MEASURED_RUNS = 20

RESULTS_DIR = Path("results/raw")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def benchmark_scanline():
    output_file = RESULTS_DIR / "scanline_benchmark.csv"

    rows = []

    for size in GRID_SIZES:
        width = size
        height = size

        for complexity in COMPLEXITIES:
            xs, ys = generate_depth_curve_polygon(
                width=width,
                height=height,
                num_vertices=complexity,
                seed=42
            )

            for _ in range(WARMUP_RUNS):
                scanline_fill_et_ael(xs, ys, width, height)

            for run in range(MEASURED_RUNS):
                start = time.perf_counter()
                grid = scanline_fill_et_ael(xs, ys, width, height)
                end = time.perf_counter()

                elapsed_ms = (end - start) * 1000
                covered_cells = int(np.sum(grid))

                rows.append({
                    "algorithm": "scanline_et_ael_cpu",
                    "grid_width": width,
                    "grid_height": height,
                    "polygon_complexity": complexity,
                    "run": run + 1,
                    "execution_time_ms": elapsed_ms,
                    "covered_cells": covered_cells,
                    "num_vertices": len(xs),
                })

            print(
                f"size={size} run={run + 1}/{MEASURED_RUNS} "
                f"time={elapsed_ms:.3f} ms covered={covered_cells}"
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
                "covered_cells",
                "num_vertices",
            ]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to: {output_file}")


if __name__ == "__main__":
    benchmark_scanline()