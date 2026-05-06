import pandas as pd

SCANLINE_PATH = "results/raw/scanline_benchmark.csv"
TRIANGLE_PATH = "results/raw/triangle_cpu_benchmark.csv"

OUTPUT_PATH = "results/processed/cpu_comparison.csv"


def main():
    scan_df = pd.read_csv(SCANLINE_PATH)
    tri_df = pd.read_csv(TRIANGLE_PATH)

    # Aggregate
    scan_agg = (
        scan_df
        .groupby(["grid_width", "polygon_complexity"])
        .agg(
            scanline_mean_ms=("execution_time_ms", "mean"),
            scanline_median_ms=("execution_time_ms", "median"),
        )
        .reset_index()
    )

    tri_agg = (
        tri_df
        .groupby(["grid_width", "polygon_complexity"])
        .agg(
            triangle_mean_ms=("execution_time_ms", "mean"),
            triangle_median_ms=("execution_time_ms", "median"),
        )
        .reset_index()
    )

    # Merge
    merged = pd.merge(
        scan_agg,
        tri_agg,
        on=["grid_width", "polygon_complexity"]
    )

    # Speedup (triangle / scanline)
    merged["speedup_mean"] = (
        merged["triangle_mean_ms"] / merged["scanline_mean_ms"]
    )
    merged["speedup_median"] = (
        merged["triangle_median_ms"] / merged["scanline_median_ms"]
    )

    # Save
    merged.to_csv(OUTPUT_PATH, index=False)

    print("\n=== CPU Comparison ===")
    print(merged)
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()