from pathlib import Path

import pandas as pd


INPUT_FILE = Path("results/raw/triangle_cpu_benchmark.csv")
OUTPUT_FILE = Path("results/raw/triangle_cpu_summary.csv")


def main():
    df = pd.read_csv(INPUT_FILE)

    aggregation = {
        "mean": ("execution_time_ms", "mean"),
        "median": ("execution_time_ms", "median"),
        "std": ("execution_time_ms", "std"),
        "min": ("execution_time_ms", "min"),
        "max": ("execution_time_ms", "max"),
        "num_triangles": ("num_triangles", "first"),
    }

    if "triangulation_time_ms" in df.columns:
        aggregation.update({
            "triangulation_mean_ms": ("triangulation_time_ms", "mean"),
            "triangulation_median_ms": ("triangulation_time_ms", "median"),
            "triangulation_std_ms": ("triangulation_time_ms", "std"),
            "triangulation_min_ms": ("triangulation_time_ms", "min"),
            "triangulation_max_ms": ("triangulation_time_ms", "max"),
        })

    if "rasterization_time_ms" in df.columns:
        aggregation.update({
            "rasterization_mean_ms": ("rasterization_time_ms", "mean"),
            "rasterization_median_ms": ("rasterization_time_ms", "median"),
            "rasterization_std_ms": ("rasterization_time_ms", "std"),
            "rasterization_min_ms": ("rasterization_time_ms", "min"),
            "rasterization_max_ms": ("rasterization_time_ms", "max"),
        })

    summary = (
        df.groupby(["algorithm", "grid_width", "grid_height", "polygon_complexity"])
        .agg(**aggregation)
        .reset_index()
    )

    time_columns = [
        column
        for column in summary.columns
        if column in {"mean", "median", "std", "min", "max"}
        or column.endswith("_ms")
    ]
    summary[time_columns] = summary[time_columns].round(6)

    summary.to_csv(OUTPUT_FILE, index=False)

    print(summary)
    print(f"\nSaved summary to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
