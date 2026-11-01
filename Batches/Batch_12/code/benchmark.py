"""Benchmark merge-sort inversion counting against the brute-force baseline.

Outputs (in ../results):
  timing.csv          random permutations, five sizes (same schema as before)
  timing_orders.csv   random, sorted and reverse-sorted permutations
  timing_plot.png     linear and log-log runtime plots for random input
  timing_orders_plot.png  merge-sort runtime by input order
  environment.txt     Python version and platform used for the run
"""
import csv
import platform
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
sys.path.insert(0, str(HERE))

from generate_inputs import generate_permutation
from main_solution import count_inversions
from rejected_alternative import count_inversions_brute

SIZES = [100, 500, 1000, 2000, 5000]
ORDERS = ["random", "sorted", "reverse"]
TRIALS = 5


def median_runtime(function, values, repeats=TRIALS):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(values)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def measure(n, order):
    values = generate_permutation(n, seed=2026 + n, order=order)
    _, fast_count = count_inversions(values)
    if fast_count != count_inversions_brute(values):
        raise AssertionError(f"Mismatch at n={n}, order={order}")
    return {
        "n": n,
        "order": order,
        "merge_sort_median_seconds": f"{median_runtime(count_inversions, values):.9f}",
        "brute_force_median_seconds": f"{median_runtime(count_inversions_brute, values):.9f}",
        "inversion_count": fast_count,
        "trials": TRIALS,
    }


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fields})


def main():
    all_rows = []
    for order in ORDERS:
        for n in SIZES:
            row = measure(n, order)
            all_rows.append(row)
            print(f"{order:8s} n={n}: merge={float(row['merge_sort_median_seconds']):.6f}s, "
                  f"brute={float(row['brute_force_median_seconds']):.6f}s")

    RESULTS.mkdir(exist_ok=True)
    random_rows = [r for r in all_rows if r["order"] == "random"]
    for r in random_rows:
        r["input"] = "deterministic_random_permutation"
    write_csv(RESULTS / "timing.csv", random_rows,
              ["n", "merge_sort_median_seconds", "brute_force_median_seconds",
               "inversion_count", "trials", "input"])
    write_csv(RESULTS / "timing_orders.csv", all_rows,
              ["n", "order", "merge_sort_median_seconds", "brute_force_median_seconds",
               "inversion_count", "trials"])
    (RESULTS / "environment.txt").write_text(
        f"Python {platform.python_version()} ({platform.python_implementation()})\n"
        f"Platform: {platform.platform()}\n"
        f"Trials per measurement: {TRIALS} (median reported)\n",
        encoding="utf-8")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = [r["n"] for r in random_rows]
    merge = [float(r["merge_sort_median_seconds"]) for r in random_rows]
    brute = [float(r["brute_force_median_seconds"]) for r in random_rows]

    fig, (lin, log) = plt.subplots(1, 2, figsize=(12, 5))
    for ax in (lin, log):
        ax.plot(x, merge, marker="o", label="Merge-sort inversion count")
        ax.plot(x, brute, marker="o", label="Brute-force pair scan")
        ax.set_xlabel("Number of titles (n)")
        ax.set_ylabel("Median runtime (seconds)")
        ax.grid(True, alpha=0.3, which="both")
    lin.set_title("Linear scale")
    log.set_xscale("log")
    log.set_yscale("log")
    log.set_title("Log-log scale (slope shows growth rate)")
    lin.legend()
    fig.suptitle("Batch 12: measured runtime on random permutations")
    fig.tight_layout()
    fig.savefig(RESULTS / "timing_plot.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    for order in ORDERS:
        rows = [r for r in all_rows if r["order"] == order]
        ax.plot([r["n"] for r in rows],
                [float(r["merge_sort_median_seconds"]) for r in rows],
                marker="o", label=f"Merge sort, {order} input")
    ax.set_xlabel("Number of titles (n)")
    ax.set_ylabel("Median runtime (seconds)")
    ax.set_title("Merge-sort runtime by input order")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS / "timing_orders_plot.png", dpi=180)
    plt.close(fig)
    print("Saved results to", RESULTS)


if __name__ == "__main__":
    main()
