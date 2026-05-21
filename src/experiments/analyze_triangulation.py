from pathlib import Path

import pandas as pd


INPUT_FILE = Path("results/raw/triangle_cpu_benchmark.csv")
OUTPUT_FILE = Path("results/raw/triangle_cpu_summary.csv")


def main():
    df = pd.read_csv(INPUT_FILE)

    summary = (
        df.groupby(["algorithm", "grid_width", "grid_height", "polygon_complexity"])
        .agg(
            mean=("execution_time_ms", "mean"),
            median=("execution_time_ms", "median"),
            std=("execution_time_ms", "std"),
            min=("execution_time_ms", "min"),
            max=("execution_time_ms", "max"),
            num_triangles=("num_triangles", "first"),
        )
        .reset_index()
    )

    summary["mean"] = summary["mean"].round(6)
    summary["median"] = summary["median"].round(6)
    summary["std"] = summary["std"].round(6)
    summary["min"] = summary["min"].round(6)
    summary["max"] = summary["max"].round(6)

    summary.to_csv(OUTPUT_FILE, index=False)

    print(summary)
    print(f"\nSaved summary to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
