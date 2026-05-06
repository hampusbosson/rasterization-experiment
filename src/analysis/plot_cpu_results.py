from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = Path("results/processed/cpu_comparison.csv")
PLOTS_DIR = Path("results/plots")
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def plot_execution_time_by_grid(df):
    for complexity in sorted(df["polygon_complexity"].unique()):
        subset = df[df["polygon_complexity"] == complexity]

        plt.figure()
        plt.plot(subset["grid_width"], subset["scanline_median_ms"], marker="o", label="Scanline CPU")
        plt.plot(subset["grid_width"], subset["triangle_median_ms"], marker="o", label="Triangle CPU")

        plt.xlabel("Grid resolution")
        plt.ylabel("Median execution time (ms)")
        plt.title(f"CPU execution time by grid size ({complexity} vertices)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(PLOTS_DIR / f"cpu_time_by_grid_{complexity}_vertices.png", dpi=300)
        plt.close()


def plot_execution_time_by_complexity(df):
    for grid_size in sorted(df["grid_width"].unique()):
        subset = df[df["grid_width"] == grid_size]

        plt.figure()
        plt.plot(subset["polygon_complexity"], subset["scanline_median_ms"], marker="o", label="Scanline CPU")
        plt.plot(subset["polygon_complexity"], subset["triangle_median_ms"], marker="o", label="Triangle CPU")

        plt.xlabel("Polygon complexity (vertices)")
        plt.ylabel("Median execution time (ms)")
        plt.title(f"CPU execution time by polygon complexity ({grid_size}×{grid_size})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(PLOTS_DIR / f"cpu_time_by_complexity_{grid_size}.png", dpi=300)
        plt.close()


def plot_speedup_by_grid(df):
    for complexity in sorted(df["polygon_complexity"].unique()):
        subset = df[df["polygon_complexity"] == complexity]

        plt.figure()
        plt.plot(subset["grid_width"], subset["speedup_median"], marker="o")

        plt.xlabel("Grid resolution")
        plt.ylabel("Relative execution time (Triangle CPU / Scanline CPU)")
        plt.title(f"Relative CPU execution time by grid size ({complexity} vertices)")
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(PLOTS_DIR / f"cpu_speedup_by_grid_{complexity}_vertices.png", dpi=300)
        plt.close()


def main():
    df = pd.read_csv(INPUT_PATH)

    plot_execution_time_by_grid(df)
    plot_execution_time_by_complexity(df)
    plot_speedup_by_grid(df)

    print(f"Saved plots to: {PLOTS_DIR}")


if __name__ == "__main__":
    main()