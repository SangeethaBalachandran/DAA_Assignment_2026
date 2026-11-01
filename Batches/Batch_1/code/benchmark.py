#!/usr/bin/env python3
"""
benchmark.py -- reproducible timing of the main solution vs brute force.

* Random family: median over 5 inputs per n (different seeds).
* Same input object is given to both algorithms (families from generate_inputs.py).
* Statistic: MEDIAN of REPEATS timed runs (time.perf_counter); printing and file
  writing happen outside the timed region; gc.collect() before each repetition.
* Before timing each size, both algorithms' solution sets are compared; the
  benchmark stops with an error if they differ.
Outputs (in ../results): timing.csv, timing_large_n.csv, timing_plot.png
"""
import csv
import gc
import os
import statistics
import sys
import time
from math import comb

from generate_inputs import DEFAULT_SEED, make_instance
from main_solution import solve
from rejected_alternative import brute_force_solve

SIZES = [8, 10, 12, 14, 16, 18, 20, 22]
LARGE_SIZES = [24, 28, 32, 36, 40]
REPEATS = 5
INSTANCES = 5          # random family: 5 different inputs per n (hard family is deterministic)
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def median_ms(fn, repeats=REPEATS):
    times = []
    for _ in range(repeats):
        gc.collect()
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter() - t0) * 1000.0)
    return statistics.median(times)


def instances_for(family, n):
    """Random family: INSTANCES inputs (seed offsets 0, 1000, 2000, ...); hard: one input."""
    if family == "hard":
        return [make_instance("hard", n, DEFAULT_SEED)]
    return [make_instance("random", n, DEFAULT_SEED + 1000 * k) for k in range(INSTANCES)]


def measure(family, n, with_brute=True):
    """Return per-n summary (medians across instances of per-instance medians)."""
    t_main, t_brute, states, tested, over, unre, sols = [], [], [], [], [], [], []
    for amounts, target, tol in instances_for(family, n):
        res = solve(amounts, target, tol)
        if with_brute:
            bf_sols, bf_tested = brute_force_solve(amounts, target, tol)
            if res.solutions != bf_sols:                 # correctness gate
                sys.exit(f"MISMATCH for {family} n={n}")
            tested.append(bf_tested)
            t_brute.append(median_ms(lambda: brute_force_solve(amounts, target, tol),
                                     REPEATS if family == "hard" else 3))
        t_main.append(median_ms(lambda: solve(amounts, target, tol)))
        states.append(res.states); over.append(res.prune_overshoot)
        unre.append(res.prune_unreachable); sols.append(len(res.solutions))
    med = statistics.median
    return dict(n=n, t_main=med(t_main), t_brute=med(t_brute) if with_brute else None,
                states=med(states), states_max=max(states), tested=med(tested) if with_brute else 2 ** n,
                over=med(over), unre=med(unre), sols=med(sols))


def main():
    os.makedirs(RESULTS, exist_ok=True)
    rows = []
    for family in ("random", "hard"):
        for n in SIZES:
            m = measure(family, n)
            rows.append([n, round(m["t_main"], 3), round(m["t_brute"], 3), family, int(m["states"]),
                         int(m["tested"]), int(m["over"]), int(m["unre"]), int(m["sols"])])
            print(rows[-1], flush=True)
    with open(os.path.join(RESULTS, "timing.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["n", "time_chosen_ms", "time_rejected_ms", "family", "states_chosen",
                    "subsets_rejected", "prune_overshoot", "prune_unreachable", "solutions"])
        w.writerows(rows)

    # Larger n: main solution only (brute force would need 2^n subsets).
    big = []
    for n in LARGE_SIZES:
        m = measure("random", n, with_brute=False)
        big.append([n, round(m["t_main"], 3), int(m["states"]), m["states_max"], 2 ** n, int(m["sols"])])
        print("large", big[-1], flush=True)
    with open(os.path.join(RESULTS, "timing_large_n.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["n", "time_chosen_ms", "states_median", "states_max", "all_subsets", "solutions_median"])
        w.writerows(big)

    plot(rows)


def plot(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    for ax, fam, title in ((axes[0], "random", "Typical audit batch (random amounts, 4-item target)"),
                           (axes[1], "hard", "Difficult family (no solution, target near mid-sum)")):
        sub = [r for r in rows if r[3] == fam]
        ns = [r[0] for r in sub]
        ax.plot(ns, [r[1] for r in sub], "o-", label="Pruned search (chosen)")
        ax.plot(ns, [r[2] for r in sub], "s-", label="Brute force (rejected)")
        # theoretical shape: c * (states) scaled to match chosen time at the largest n
        c = sub[-1][1] / sub[-1][4]
        ax.plot(ns, [c * r[4] for r in sub], "k--", alpha=.6, label="c x measured states (theory shape)")
        c2 = sub[-1][2] / 2 ** ns[-1]
        ax.plot(ns, [c2 * 2 ** n for n in ns], ":", color="gray", label="c' x 2^n (brute-force shape)")
        ax.set_yscale("log")
        ax.set_xlabel("Number of transactions n")
        ax.set_ylabel("Median running time (ms, log scale)")
        ax.set_title(title, fontsize=10)
        ax.grid(True, which="both", alpha=.3)
        ax.legend(fontsize=8)
    fig.suptitle(f"Batch 1: running time vs n (medians; random family = 5 inputs per n; seed {DEFAULT_SEED})")
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "timing_plot.png"), dpi=150)


if __name__ == "__main__":
    main()
