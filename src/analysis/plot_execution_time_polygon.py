import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_PATH = "results/processed/cpu_comparison.csv"

OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_execution_time_by_complexity():
    df = pd.read_csv(INPUT_PATH)

    grid_sizes = sorted(df["grid_width"].unique())

    # Vertical layout
    fig, axes = plt.subplots(
        len(grid_sizes),
        1,
        figsize=(7, 12),
        sharex=True,
        sharey=True
    )

    fig.suptitle(
        "Execution time by polygon complexity for different grid resolutions",
        fontsize=14
    )

    fig.patch.set_edgecolor("black")
    fig.patch.set_linewidth(0.5)

    for ax, grid_size in zip(axes, grid_sizes):
        subset = df[df["grid_width"] == grid_size]

        ax.plot(
            subset["polygon_complexity"],
            subset["scanline_mean_ms"],
            marker="o",
            linewidth=2,
            label="Scanline"
        )

        ax.plot(
            subset["polygon_complexity"],
            subset["triangle_mean_ms"],
            marker="o",
            linewidth=2,
            label="Triangulation + triangle rasterization"
        )

        ax.set_title(f"{grid_size}×{grid_size} grid")

        ax.set_ylabel("Mean execution time (ms)")

        ax.grid(True, linestyle="--", alpha=0.5)

        ax.set_xticks(subset["polygon_complexity"])
        ax.set_xticklabels(
            [str(x) for x in subset["polygon_complexity"]]
        )

    axes[-1].set_xlabel("Polygon vertices")

    axes[0].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    plt.savefig(
        OUTPUT_DIR / "figure_5_2_execution_time_by_complexity.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    plot_execution_time_by_complexity()