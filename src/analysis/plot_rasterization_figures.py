from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.algorithms.scanline_rasterizer import scanline_fill_et_ael
from src.algorithms.triangulation import triangulate_polygon
from src.data.generate_polygons import generate_depth_curve_polygon


OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_triangulation(xs, ys, width, height):
    triangles = triangulate_polygon(xs, ys)

    plt.figure(figsize=(6, 6))

    colors = plt.cm.tab20(np.linspace(0, 1, len(triangles)))

    for i, tri in enumerate(triangles):
        tx = [tri[0][0], tri[1][0], tri[2][0], tri[0][0]]
        ty = [tri[0][1], tri[1][1], tri[2][1], tri[0][1]]

        plt.fill(
            tx,
            ty,
            color=colors[i],
            alpha=0.3,
            edgecolor="black",
            linewidth=0.6,
        )

    plt.plot(
        list(xs) + [xs[0]],
        list(ys) + [ys[0]],
        color="black",
        linewidth=2.5,
        label="Polygon boundary",
    )

    plt.xlim(0, width)
    plt.ylim(height, 0)
    plt.gca().set_aspect("equal")

    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "figure_4_6_triangulation.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()

    print("Vertices:", len(xs))
    print("Triangles:", len(triangles))


def plot_scanline_process(xs, ys, width, height):
    scanline_y = int(height * 0.5)

    plt.figure(figsize=(6, 6))

    plt.plot(list(xs) + [xs[0]], list(ys) + [ys[0]], linewidth=2)
    plt.axhline(y=scanline_y, linestyle="--", label="Scanline")

    intersections = []
    for i in range(len(xs)):
        x1, y1 = xs[i], ys[i]
        x2, y2 = xs[(i + 1) % len(xs)], ys[(i + 1) % len(xs)]

        if (y1 <= scanline_y < y2) or (y2 <= scanline_y < y1):
            t = (scanline_y - y1) / (y2 - y1)
            x = x1 + t * (x2 - x1)
            intersections.append(x)

    intersections.sort()

    for x in intersections:
        plt.scatter(x, scanline_y, color="red")

    for i in range(0, len(intersections), 2):
        if i + 1 < len(intersections):
            plt.plot(
                [intersections[i], intersections[i + 1]],
                [scanline_y, scanline_y],
                linewidth=4,
            )

    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.gca().set_aspect("equal")
    plt.gca().invert_yaxis()
    plt.legend()

    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "figure_4_5_scanline_process.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def plot_binary_rasterization(width=128, height=128):
    xs, ys = generate_depth_curve_polygon(
        width,
        height,
        num_vertices=100,
        seed=42,
    )

    grid = scanline_fill_et_ael(xs, ys, width, height)

    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap="gray", origin="upper")

    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "figure_4_4_binary_raster.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def plot_polygon_with_grid(width=128, height=128):
    xs, ys = generate_depth_curve_polygon(
        width,
        height,
        num_vertices=100,
        seed=42,
    )

    fig, ax = plt.subplots(figsize=(6, 6))

    for x in range(width):
        ax.axvline(x, color="gray", linewidth=0.7)
    for y in range(height):
        ax.axhline(y, color="gray", linewidth=0.7)

    ax.plot(
        list(xs) + [xs[0]],
        list(ys) + [ys[0]],
        color="black",
        linewidth=2,
    )

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect("equal")
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "figure_4_3_polygon_grid_overlay.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def plot_polygon(xs, ys, width, height, show_center=True, invert_y=True):
    plt.figure(figsize=(6, 6))

    plt.plot(
        list(xs) + [xs[0]],
        list(ys) + [ys[0]],
        linewidth=2,
        label="Polygon boundary",
    )
    plt.scatter(xs, ys, s=10, alpha=0.6, label="Vertices")

    if show_center:
        center_x = width * 0.5
        center_y = height * 0.5
        plt.scatter([center_x], [center_y], color="red", s=40, label="Center")

    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.gca().set_aspect("equal")

    if invert_y:
        plt.gca().invert_yaxis()

    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "figure_4_1_polygon.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def plot_polygon_complexity_comparison(width=512, height=512, seed=42):
    complexities = [20, 100, 300]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    for ax, complexity in zip(axes, complexities):
        xs, ys = generate_depth_curve_polygon(
            width=width,
            height=height,
            num_vertices=complexity,
            seed=seed,
        )

        ax.plot(list(xs) + [xs[0]], list(ys) + [ys[0]], linewidth=2)
        ax.scatter(xs, ys, s=6, alpha=0.5)

        ax.set_title(f"{complexity} vertices")
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_aspect("equal")
        ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "figure_4_2_polygon_complexity.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def plot_all_rasterization_figures(width=512, height=512):
    xs, ys = generate_depth_curve_polygon(
        width=width,
        height=height,
        num_vertices=100,
        seed=42,
    )

    plot_polygon(xs, ys, width, height)
    plot_polygon_complexity_comparison(width=width, height=height)
    plot_polygon_with_grid()
    plot_binary_rasterization()
    plot_scanline_process(xs, ys, width, height)
    plot_triangulation(xs, ys, width, height)


if __name__ == "__main__":
    plot_all_rasterization_figures()
