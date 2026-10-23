"""Batch 16 - timing benchmark: chosen D&C vs rejected exhaustive search.

* Inputs come from generate_inputs.generate("mixed", n) with the fixed seed,
  so both algorithms see identical data.
* Before timing, both answers (sum and window) are checked for equality.
* Only the algorithm call is inside the timed region (time.perf_counter).
* Each (algorithm, n) is run once untimed, then REPEATS (7) times with the
  garbage collector paused; the median is recorded.

Outputs (relative to the Batch_16 folder):
    results/timing.csv       n,time_chosen_ms,time_rejected_ms
    results/timing_plot.png  plot drawn from the CSV that was just written
    results/large_scale.csv  optional (--large): chosen algorithm only,
                             n = 24k, 240k, 1.2M, 2.4M
"""

from __future__ import annotations

import argparse
import csv
import gc
import os
import platform
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from generate_inputs import generate                      # noqa: E402
from main_solution import best_window                     # noqa: E402
from rejected_alternative import best_window_exhaustive   # noqa: E402

RESULTS = os.path.join(os.path.dirname(HERE), "results")
SIZES = [100, 200, 400, 800, 1600, 3200]
REPEATS = 7


def time_ms(fn, values, repeats: int) -> float:
    """Median wall-clock ms of ``repeats`` calls, after one untimed warm-up.

    The garbage collector is paused while timing (as ``timeit`` does) so a
    collection triggered by earlier work does not land inside a sample.
    """
    fn(values)
    samples = []
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        for _ in range(repeats):
            start = time.perf_counter()
            fn(values)
            samples.append((time.perf_counter() - start) * 1000.0)
    finally:
        if gc_was_enabled:
            gc.enable()
    return statistics.median(samples)


def run(sizes, repeats):
    rows = []
    for n in sizes:
        values = generate("mixed", n)
        chosen, rejected = best_window(values), best_window_exhaustive(values)
        if chosen != rejected:
            raise AssertionError(f"n={n}: {chosen} != {rejected}")
        t_c = time_ms(best_window, values, repeats)
        t_r = time_ms(best_window_exhaustive, values, repeats)
        rows.append((n, t_c, t_r))
        print(f"n={n:6d}  chosen={t_c:10.3f} ms  rejected={t_r:12.3f} ms  "
              f"answer={chosen[0]} window=[{chosen[1] + 1}, {chosen[2] + 1}]")
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "time_chosen_ms", "time_rejected_ms"])
        for n, t_c, t_r in rows:
            w.writerow([n, f"{t_c:.4f}", f"{t_r:.4f}"])


def plot_from_csv(csv_path, png_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with open(csv_path, newline="", encoding="utf-8") as fh:
        data = list(csv.DictReader(fh))
    n = [int(r["n"]) for r in data]
    tc = [float(r["time_chosen_ms"]) for r in data]
    tr = [float(r["time_rejected_ms"]) for r in data]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), dpi=150)
    styles = dict(chosen=dict(color="#1f5f99", marker="o", lw=2),
                  rejected=dict(color="#c0392b", marker="s", lw=2))
    for ax, log in zip(axes, (False, True)):
        ax.plot(n, tc, label="Chosen: Divide & Conquer summary, O(n)",
                **styles["chosen"])
        ax.plot(n, tr, label="Rejected: exhaustive enumeration, O(n²)",
                **styles["rejected"])
        ax.set_xlabel("Input size n (number of price changes)")
        ax.set_ylabel("Median wall-clock time (ms)")
        ax.grid(True, which="both", alpha=0.3)
        if log:
            ax.set_xscale("log", base=2)
            ax.set_yscale("log")
            ax.set_xticks(n)
            ax.set_xticklabels([str(v) for v in n])
            ax.set_title("Log-log scale (log₂ x-axis, log₁₀ y-axis)")
        else:
            ax.set_title("Linear scale")
        ax.legend(fontsize=8, loc="upper left")
    fig.suptitle("Batch 16 - Best trading window: measured running time "
                 f"(median of {REPEATS} runs, Python {platform.python_version()})",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(png_path)
    plt.close(fig)


LARGE_SIZES = [24_000, 240_000, 1_200_000, 2_400_000]


def run_large(sizes=LARGE_SIZES, repeats=3):
    """Chosen algorithm only, up to the production scale n = 2.4 million."""
    path = os.path.join(RESULTS, "large_scale.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "time_chosen_ms", "us_per_value", "repeats"])
        for n in sizes:
            values = generate("mixed", n)
            ms = time_ms(best_window, values, repeats)
            w.writerow([n, f"{ms:.1f}", f"{ms * 1000 / n:.2f}", repeats])
            print(f"large scale: n={n} chosen median={ms:.1f} ms "
                  f"({ms * 1000 / n:.2f} us/value)")
    print(f"wrote {path}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repeats", type=int, default=REPEATS)
    parser.add_argument("--sizes", type=int, nargs="+", default=SIZES)
    parser.add_argument("--large", action="store_true",
                        help="also time the chosen algorithm from 24k up to n = 2.4 million")
    args = parser.parse_args(argv)

    os.makedirs(RESULTS, exist_ok=True)
    print(f"Python {platform.python_version()} on {platform.platform()}")
    rows = run(args.sizes, args.repeats)
    csv_path = os.path.join(RESULTS, "timing.csv")
    png_path = os.path.join(RESULTS, "timing_plot.png")
    write_csv(csv_path, rows)
    plot_from_csv(csv_path, png_path)
    print(f"wrote {csv_path}\nwrote {png_path}")
    if args.large:
        run_large()
    return 0


if __name__ == "__main__":
    sys.exit(main())
