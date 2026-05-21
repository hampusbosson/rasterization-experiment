# Thesis rasterization experiments

This project compares scanline rasterization with triangulation followed by
per-triangle rasterization. The experiments use synthetically generated,
non-self-intersecting polygons and rasterize them onto binary grids.

The benchmark variables:

- grid resolution: `256x256`, `512x512`, `1024x1024`, `2048x2048`
- polygon complexity: `20`, `100`, and `300` vertices
- measured runs: `20`
- warm-up runs: `5`

## Setup

The thesis experiments were run with Python `3.12.3` and the dependency
versions listed in `requirements.txt`:

- NumPy `2.4.4`
- Numba `0.65.1`
- pandas `3.0.2`
- matplotlib `3.10.9`

Install the dependencies:

```bash
pip install -r requirements.txt
```

The reported experiments were executed on an Apple M1 machine with 8 CPU cores
and 16 GB RAM, running macOS Tahoe 26.2.

## Run experiments

Run both benchmark experiments and write raw CSV files to `results/raw`:

```bash
python main.py --run experiments
```

Generate summary and comparison CSV files from existing raw benchmark files:

```bash
python main.py --run analysis
```

Run the full pipeline: benchmarks, analysis, and figures:

```bash
python main.py --run pipeline --figure all
```

This regenerates the raw benchmark CSV files, summary/comparison CSV files, and
the figures used in the study.

## Generate figures only

Generate figures from existing CSV files:

```bash
python main.py --run figures --figure all
```

Available figure groups:

```text
rasterization
time-grid
time-complexity
speedup
all
```

The default command is:

```bash
python main.py
```

which is equivalent to:

```bash
python main.py --run figures --figure speedup
```
