#!/usr/bin/env python3
"""Timing experiments -> results/*.csv and results/timing_plot.png

Usage: python3 run_timing.py            (full run, about 2-3 minutes)
       python3 run_timing.py --quick    (small sizes, for a smoke test)
Requires matplotlib for the plot (pip install matplotlib).
"""
import argparse
import csv
import os
import time
import tracemalloc

from generate_inputs import make_pair
from main_solution import align, fill_table
from linear_space import hirschberg
from rejected_alternative import recursive_cost, call_count_formula

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")


def timed(fn, *args, reps=1):
    t0 = time.perf_counter()
    for _ in range(reps):
        out = fn(*args)
    return (time.perf_counter() - t0) * 1000.0 / reps, out


def write_csv(name, header, rows):
    with open(os.path.join(RES, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    quick = ap.parse_args().quick
    os.makedirs(RES, exist_ok=True)

    # ---- A: chosen method vs plain recursion on the same inputs --------------------
    sizes_a = [4, 5, 6, 7, 8] if quick else [4, 5, 6, 7, 8, 9, 10, 11]
    rows = []
    for n in sizes_a:
        r, q = make_pair(n, "random", seed=n)
        t_dp, (c1, _) = timed(align, r, q, reps=2000 if n < 9 else 500)
        t_rec, (c2, calls) = timed(recursive_cost, r, q, reps=1)
        assert c1 == c2
        rows.append([n, "%.5f" % t_dp, "%.3f" % t_rec, calls, (n + 1) ** 2])
        print("A n=%2d  dp=%.5f ms  recursion=%.3f ms  calls=%d  cells=%d" % (n, t_dp, t_rec, calls, (n + 1) ** 2))
    write_csv("timing.csv", ["n", "time_chosen_ms", "time_rejected_ms", "calls_rejected", "cells_chosen"], rows)

    # ---- B: scaling of the chosen method (full table vs linear space) --------------
    sizes_b = [100, 200, 400] if quick else [100, 200, 400, 800, 1600, 3200]
    rows = []
    for n in sizes_b:
        r, q = make_pair(n, "mutated", seed=7)
        t_full, (c1, _) = timed(align, r, q, reps=3 if n <= 400 else 1)
        t_lin, ops = timed(hirschberg, r, q, reps=1)
        c2 = sum(o != "M" for o, _, _ in ops)
        assert c1 == c2
        cells = (len(r) + 1) * (len(q) + 1)
        rows.append([n, cells, "%.2f" % t_full, "%.2f" % t_lin, "%.3f" % (t_full * 1000.0 / cells), "%.2f" % (t_lin / t_full)])
        print("B n=%4d  full=%.1f ms  linear-space=%.1f ms  ratio=%.2f" % (n, t_full, t_lin, t_lin / t_full))
    write_csv("timing_scaling.csv", ["n", "cells", "time_full_ms", "time_linear_space_ms", "us_per_cell", "ratio_linear_over_full"], rows)

    # ---- C: worst-case / input-dependence at fixed n --------------------------------
    nw = 400 if quick else 1600
    rows = []
    for kind in ["identical", "random", "mutated", "mismatch"]:
        r, q = make_pair(nw, kind, seed=3)
        t, D = timed(fill_table, r, q, reps=1)
        c = D[-1][-1]
        rows.append([kind, nw, "%.1f" % t, c])
        print("C %-9s n=%d  fill=%.1f ms  cost=%s" % (kind, nw, t, c))
    write_csv("worst_case.csv", ["input_kind", "n", "fill_time_ms", "min_cost"], rows)

    # ---- D: memory, full table vs linear space (Python peak allocations) -----------
    nm = 400 if quick else 1000
    r, q = make_pair(nm, "mutated", seed=7)
    tracemalloc.start()
    align(r, q)
    full_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    tracemalloc.start()
    hirschberg(r, q)
    lin_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    write_csv("memory_demo.csv", ["n", "full_table_peak_KB", "linear_space_peak_KB"], [[nm, full_peak // 1024, lin_peak // 1024]])
    print("D n=%d peak: full=%d KB  linear=%d KB" % (nm, full_peak // 1024, lin_peak // 1024))

    make_plot(quick)


def make_plot(quick):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def rd(name):
        with open(os.path.join(RES, name)) as f:
            return list(csv.DictReader(f))

    A, B = rd("timing.csv"), rd("timing_scaling.csv")
    BLUE, ORANGE, INK, MUTED, GRID = "#2a6fb0", "#c8551f", "#1f2933", "#6b7785", "#e4e8ec"
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED, "axes.titlecolor": INK})
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6))
    for ax in (a1, a2):
        ax.grid(True, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    n = [int(r["n"]) for r in A]
    t_dp = [float(r["time_chosen_ms"]) for r in A]
    t_rec = [float(r["time_rejected_ms"]) for r in A]
    calls = [int(r["calls_rejected"]) for r in A]
    a1.semilogy(n, t_rec, "o-", color=ORANGE, lw=2, ms=6, label="Plain recursion (measured)")
    a1.semilogy(n, t_dp, "o-", color=BLUE, lw=2, ms=6, label="Table method (measured)")
    k = t_rec[-1] / calls[-1]
    a1.semilogy(n, [call_count_formula(x, x) * k for x in n], "--", color=ORANGE, lw=1, label="Predicted: calls x time per call")
    k2 = t_dp[-1] / (n[-1] + 1) ** 2
    a1.semilogy(n, [(x + 1) ** 2 * k2 for x in n], "--", color=BLUE, lw=1, label="Predicted: c x (n+1)^2")
    a1.set_xlabel("n (both strings have length n)")
    a1.set_ylabel("time per alignment (ms, log scale)")
    a1.set_title("Same inputs: exponential recursion vs quadratic table")
    a1.legend(frameon=False, fontsize=8.5)

    nb = [int(r["n"]) for r in B]
    full = [float(r["time_full_ms"]) for r in B]
    lin = [float(r["time_linear_space_ms"]) for r in B]
    a2.loglog(nb, full, "o-", color=BLUE, lw=2, ms=6, label="Full table + traceback")
    a2.loglog(nb, lin, "s-", color=ORANGE, lw=2, ms=6, label="Linear-memory version")
    c = full[0] / nb[0] ** 2
    a2.loglog(nb, [c * x * x for x in nb], "--", color=MUTED, lw=1, label="Reference slope: n^2")
    a2.set_xlabel("n (log scale)")
    a2.set_ylabel("time (ms, log scale)")
    a2.set_title("Chosen method: roughly n^2 growth (steeper at mid sizes, see report)")
    a2.legend(frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(os.path.join(RES, "timing_plot.png"), dpi=160)
    print("wrote timing_plot.png")


if __name__ == "__main__":
    main()
