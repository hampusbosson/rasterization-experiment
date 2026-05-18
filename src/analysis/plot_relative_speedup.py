import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_PATH = "results/processed/cpu_comparison.csv"

OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_relative_speedup():
    df = pd.read_csv(INPUT_PATH)

    df["configuration"] = (
        df["grid_width"].astype(str)
        + "×"
        + df["grid_width"].astype(str)
        + "\n"
        + df["polygon_complexity"].astype(str)
        + " vertices"
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    fig.suptitle(
        "Relative speedup of scanline-based rasterization",
        fontsize=14
    )

    fig.patch.set_edgecolor("black")
    fig.patch.set_linewidth(0.5)

    ax.bar(
        df["configuration"],
        df["speedup_mean"]
    )

    ax.set_ylabel("Relative speedup (×)")
    ax.set_xlabel("Experiment configuration")
    ax.set_title("Triangle mean time / scanline mean time")

    ax.grid(True, axis="y", linestyle="--", alpha=0.5)

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout(rect=[0, 0, 1, 0.92])

    plt.savefig(
        OUTPUT_DIR / "figure_5_3_relative_speedup.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    plot_relative_speedup()