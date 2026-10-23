# How to run — Batch 16 (Best Trading Window)

## Requirements

| Item | Version / note |
|---|---|
| Python | 3.10 or newer (developed and measured on CPython 3.14.4, Windows 11) |
| Algorithms and tests | standard library only |
| `benchmark.py` plot | `matplotlib` → `python -m pip install matplotlib` |
| `make_slides.py` (optional, rebuilds `slides.pdf`) | Microsoft Edge or Google Chrome for headless print-to-PDF, plus `pymupdf` → `python -m pip install pymupdf` (only for page previews) |

**Working directory:** every command below assumes you are in `Batches/Batch_16/`.
From the repository root, first run `cd Batches/Batch_16`.
Positions printed by the programs are **1-based and inclusive**, matching the report.

## Chosen solution (Divide and Conquer)

```bash
python code/main_solution.py 3 -5 8 -2 6 -9 4 7 -3 -6 5 2
python code/main_solution.py "[3,-5,8,-2,6,-9,4,7,-3,-6,5,2]" --servers 8
python code/main_solution.py --file input.txt
```

Expected output for the given instance: `best sum = 14`, `window (1-based, inclusive) = [3, 8]`.
`--servers 8` also runs the single-machine simulation of the eight-server summary/merge design.
Empty input prints an error and exits with status 2 (a non-empty window is required).

## Rejected alternative (exhaustive enumeration, O(n²))

```bash
python code/rejected_alternative.py 3 -5 8 -2 6 -9 4 7 -3 -6 5 2
```

## Changed requirement: at most two non-overlapping windows

```bash
python code/two_windows.py 3 -5 8 -2 6 -9 4 7 -3 -6 5 2
```

Expected: total 23 using windows [3, 5] and [7, 8].

## Generating inputs

```bash
python code/generate_inputs.py --kind mixed --n 1000 --out input.txt
python code/generate_inputs.py --kind positive --n 1000 --out ones.txt
python code/generate_inputs.py --kind negative --n 1000 --out neg.txt
python code/generate_inputs.py --kind given --out given.txt
```

The format is one integer per line. The default seed is `2026`, so the same `(kind, n, seed)` always produces the same file.

## Correctness tests

```bash
python -B code/test_correctness.py
```

There are 24 `unittest` tests: the given instance, edge cases, ties, randomized brute-force comparison, merge-versus-definition checks, associativity, the eight-server model, the segment tree and disjoint sparse table against direct scans, and the two-window and k-window algorithms against exhaustive search.

## Benchmark (regenerates the CSV and plot)

```bash
python -B code/benchmark.py
python -B code/benchmark.py --large
```

`--large` additionally times the chosen algorithm only, at n = 24,000, 240,000, 1,200,000 and 2,400,000 (median of 3). This takes about 2–3 minutes in CPython.

## Trace and slides

```bash
python -B code/trace_instance.py > results/trace_given_instance.md
python -B code/make_slides.py
```

## Generated files

| File | Produced by | Contents |
|---|---|---|
| `results/timing.csv` | `benchmark.py` | `n,time_chosen_ms,time_rejected_ms`, the median of 7 measured runs per size (after a warm-up, GC paused) |
| `results/timing_plot.png` | `benchmark.py` | Linear and log-log plots drawn from the CSV just written |
| `results/large_scale.csv` | `benchmark.py --large` | Chosen algorithm only, n from 24 k to 2.4 × 10⁶, with µs per value |
| `results/trace_given_instance.md` | `trace_instance.py` | Every merge of the given instance, generated from the code |
| `slides.pdf` | `make_slides.py` | Presentation deck, built from `slides.html` |

## Source files

| File | Role |
|---|---|
| `main_solution.py` | `Summary`, `leaf`, `merge`, recursive `summarize`, `best_window`, coordinator `reduce_summaries`, eight-server simulation, CLI |
| `rejected_alternative.py` | Exhaustive O(n²) enumeration with running sums |
| `range_queries.py` | Kadane range scan, segment tree, and disjoint sparse table for `[L, R]` queries |
| `two_windows.py` | Prefix/suffix DP for at most two windows, plus an O(kn) DP for k windows |
| `generate_inputs.py` | Deterministic inputs |
| `benchmark.py` | Timing, CSV, and plot |
| `test_correctness.py` | Automated tests |
| `trace_instance.py` | Generates the report's trace tables |
| `make_slides.py` | Prints `slides.html` to `slides.pdf` and renders preview images |
