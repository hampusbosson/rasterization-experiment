import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_PATH = "results/processed/cpu_comparison.csv"

OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_execution_time_by_grid():
    df = pd.read_csv(INPUT_PATH)

    complexities = sorted(df["polygon_complexity"].unique())

    # Vertical layout
    fig, axes = plt.subplots(
        len(complexities),
        1,
        figsize=(7, 10),
        sharex=True,
        sharey=True
    )

    fig.suptitle(
        "Execution time by grid resolution for different polygon complexities",
        fontsize=14
    )
    fig.patch.set_edgecolor("black")
    fig.patch.set_linewidth(0.5)

    for ax, complexity in zip(axes, complexities):
        subset = df[df["polygon_complexity"] == complexity]

        ax.plot(
            subset["grid_width"],
            subset["scanline_mean_ms"],
            marker="o",
            linewidth=2,
            label="Scanline"
        )

        ax.plot(
            subset["grid_width"],
            subset["triangle_mean_ms"],
            marker="o",
            linewidth=2,
            label="Triangulation + triangle rasterization"
        )

        ax.set_title(f"{complexity} vertices")

        ax.set_ylabel("Mean execution time (ms)")

        ax.grid(True, linestyle="--", alpha=0.5)

        ax.set_xticks(subset["grid_width"])
        ax.set_xticklabels(
            [f"{x}×{x}" for x in subset["grid_width"]]
        )

    axes[-1].set_xlabel("Grid resolution")

    axes[0].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    plt.savefig(
        OUTPUT_DIR / "figure_5_1_execution_time_by_grid.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()



if __name__ == "__main__":
    plot_execution_time_by_grid()