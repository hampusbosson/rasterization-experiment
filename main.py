import argparse

FIGURE_COMMANDS = ("rasterization", "time-grid", "time-complexity", "speedup", "all")
RUN_COMMANDS = ("figures", "experiments", "analysis", "pipeline")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate thesis figures.")
    parser.add_argument(
        "--run",
        choices=RUN_COMMANDS,
        default="figures",
        help=(
            "What to run: figures only, raw benchmark experiments, analysis CSVs, "
            "or the full experiment-to-figure pipeline."
        ),
    )
    parser.add_argument(
        "--figure",
        choices=FIGURE_COMMANDS,
        default="speedup",
        help="Figure group to generate when running figures or pipeline.",
    )
    return parser.parse_args()


def run_experiments():
    from src.experiments.benchmark_scanline import benchmark_scanline
    from src.experiments.benchmark_triangle_cpu import benchmark_triangle_cpu

    benchmark_scanline()
    benchmark_triangle_cpu()


def run_analysis():
    from src.analysis.compare_cpu import main as compare_cpu
    from src.experiments.analyze_scanline import main as analyze_scanline
    from src.experiments.analyze_triangulation import main as analyze_triangulation

    analyze_scanline()
    analyze_triangulation()
    compare_cpu()


def plot_all_figures():
    from src.analysis.plot_execution_time_grid import plot_execution_time_by_grid
    from src.analysis.plot_execution_time_polygon import plot_execution_time_by_complexity
    from src.analysis.plot_rasterization_figures import plot_all_rasterization_figures
    from src.analysis.plot_relative_speedup import plot_relative_speedup

    plot_all_rasterization_figures()
    plot_execution_time_by_grid()
    plot_execution_time_by_complexity()
    plot_relative_speedup()


def run_figure_command(figure):
    if figure == "rasterization":
        from src.analysis.plot_rasterization_figures import plot_all_rasterization_figures

        plot_all_rasterization_figures()
    elif figure == "time-grid":
        from src.analysis.plot_execution_time_grid import plot_execution_time_by_grid

        plot_execution_time_by_grid()
    elif figure == "time-complexity":
        from src.analysis.plot_execution_time_polygon import plot_execution_time_by_complexity

        plot_execution_time_by_complexity()
    elif figure == "speedup":
        from src.analysis.plot_relative_speedup import plot_relative_speedup

        plot_relative_speedup()
    elif figure == "all":
        plot_all_figures()


def main():
    args = parse_args()

    if args.run == "experiments":
        run_experiments()
    elif args.run == "analysis":
        run_analysis()
    elif args.run == "pipeline":
        run_experiments()
        run_analysis()
        run_figure_command(args.figure)
    elif args.run == "figures":
        run_figure_command(args.figure)


if __name__ == "__main__":
    main()
