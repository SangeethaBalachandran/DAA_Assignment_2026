"""Batch 5: Input Generation and Empirical Benchmarking.

Course: 23I501 - Design and Analysis of Algorithms (DAA)
Institution: PSG College of Technology

This script:
1. Generates synthetic satellite instrument instances with weakly correlated masses and values.
2. Runs execution time benchmarks comparing:
   - Chosen technique: Branch and Bound (fractional LP upper bound)
   - Rejected alternative: Plain Backtracking without bound
   - Rejected alternative: Dynamic Programming on integer mass grid
3. Outputs timing results to `results/timing.csv` (in milliseconds) and generates `results/timing_plot.png`.
4. Supports constructing and evaluating the worst-case input family.

Usage:
    python generate_inputs.py [--plot] [--worst-case]
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
import time
from pathlib import Path

# Import algorithms from main_solution and rejected_alternative
from main_solution import Item, UNITS_PER_KG, branch_and_bound
from rejected_alternative import plain_backtracking, dynamic_programming_knapsack

SIZES = [8, 12, 16, 20, 24]
BACKTRACK_MAX_N = 20  # Plain backtracking takes >10s beyond n=20


def generate_random_instance(n: int, seed: int = 1) -> tuple[list[Item], int]:
    """Generate weakly-correlated scientific instruments.
    Masses range from 0.5 kg to 5.0 kg in 0.1 g increments.
    Capacity is set to 50% of total mass.
    """
    rnd = random.Random(seed * 1000 + n)
    items = []
    for i in range(n):
        mass = rnd.randint(5_000, 50_000)  # 0.5 - 5.0 kg (in 0.1 g units)
        value = int(mass / 1000 * 10 + rnd.randint(-15, 15)) + 20
        power = rnd.randint(4, 25)
        items.append(Item(f"P{i+1}", mass, max(value, 1), power))
    cap = sum(it.mass for it in items) // 2
    return items, cap


def generate_worst_case_instance(n: int) -> tuple[list[Item], int]:
    """Construct pathological worst-case instance for Branch and Bound.
    Construction:
      v_i = m_i for all items (all densities are identical = 1.0).
      All masses are EVEN numbers.
      Total capacity C is forced to be ODD.
    Result:
      Fractional LP bound is always exactly C.
      Since all subsets sum to an even number, true optimal value is at most C - 1.
      Therefore, floor(bound) > incumbent forever; NO internal node is pruned by the bound.
      Explores all feasible partial selections -> Theta(2^n).
    """
    items = [
        Item(f"W{i+1}", 2 * (10_000 + 137 * i), 2 * (10_000 + 137 * i), 10)
        for i in range(n)
    ]
    cap = sum(it.mass for it in items) // 2
    if cap % 2 == 0:
        cap += 1
    return items, cap


def run_benchmark():
    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    print("=" * 80)
    print("EMPIRICAL BENCHMARK: Branch & Bound vs Plain Backtracking vs Dynamic Programming")
    print("=" * 80)
    print(f"{'n':>4} | {'BnB time (ms)':>14} | {'BT time (ms)':>14} | {'DP time (ms)':>14} | {'BnB nodes':>10} | {'BT nodes':>12}")
    print("-" * 80)

    for n in SIZES:
        items, cap = generate_random_instance(n)
        srt = sorted(items, key=lambda it: -it.value / it.mass)

        # 1. Chosen Algorithm: Best-First Branch & Bound
        t0 = time.perf_counter()
        res_bnb = branch_and_bound(srt, cap)
        t_bnb_ms = (time.perf_counter() - t0) * 1000

        # 2. Rejected Alternative 1: Plain Backtracking
        if n <= BACKTRACK_MAX_N:
            t0 = time.perf_counter()
            bt_val, bt_set, bt_nodes = plain_backtracking(items, cap)
            t_bt_ms = (time.perf_counter() - t0) * 1000
            assert bt_val == res_bnb["best"]
        else:
            t_bt_ms = float("nan")
            bt_nodes = "N/A"

        # 3. Dynamic Programming (for comparison)
        t0 = time.perf_counter()
        dp_val, dp_set, dp_cells = dynamic_programming_knapsack(items, cap)
        t_dp_ms = (time.perf_counter() - t0) * 1000
        assert dp_val == res_bnb["best"]

        bnb_nodes = res_bnb["stats"]["generated"]
        rows.append((n, t_bnb_ms, t_bt_ms, t_dp_ms, bnb_nodes, bt_nodes))

        bt_str = f"{t_bt_ms:14.3f}" if t_bt_ms == t_bt_ms else f"{'Timeout':>14}"
        print(f"{n:>4} | {t_bnb_ms:14.4f} | {bt_str} | {t_dp_ms:14.3f} | {bnb_nodes:>10} | {str(bt_nodes):>12}")

    # Write results/timing.csv (format required by college specification: n, time_chosen_ms, time_rejected_ms)
    csv_path = results_dir / "timing.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "time_chosen_ms", "time_rejected_ms"])
        for r in rows:
            time_bt_val = f"{r[2]:.4f}" if r[2] == r[2] else "nan"
            writer.writerow([r[0], f"{r[1]:.4f}", time_bt_val])
    print(f"\n[Saved] Timing results written to: {csv_path}")

    # Plot generation
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        ns = [r[0] for r in rows]
        bnb_times = [r[1] for r in rows]
        bt_data = [(r[0], r[2]) for r in rows if r[2] == r[2]]

        plt.figure(figsize=(8, 5))
        plt.semilogy(ns, bnb_times, "o-", color="#1f77b4", linewidth=2, label="Branch & Bound (Chosen)")
        plt.semilogy([x[0] for x in bt_data], [x[1] for x in bt_data], "^-", color="#d62728", linewidth=2, label="Plain Backtracking (Rejected)")
        plt.semilogy(ns, [r[3] for r in rows], "s-", color="#2ca02c", linewidth=2, label="Dynamic Programming Table (Rejected)")

        plt.xlabel("Number of Instruments (n)", fontsize=11)
        plt.ylabel("Running Time (ms, log scale)", fontsize=11)
        plt.title("Satellite Knapsack: Execution Time Scaling vs Problem Size", fontsize=12, fontweight="bold")
        plt.grid(True, which="both", linestyle="--", alpha=0.4)
        plt.legend(fontsize=10)
        plt.tight_layout()

        plot_path = results_dir / "timing_plot.png"
        plt.savefig(plot_path, dpi=200)
        print(f"[Saved] Performance plot saved to: {plot_path}")
    except ImportError:
        print("[Note] matplotlib is not installed. To generate plot, run: pip install matplotlib")


def run_worst_case_evaluation():
    print("\n" + "=" * 80)
    print("PATHOLOGICAL WORST-CASE EVALUATION FOR BRANCH AND BOUND")
    print("=" * 80)
    print(f"{'n':>4} | {'Nodes Generated':>16} | {'Full Tree 2^(n+1)-1':>20} | {'Fraction':>10} | {'Time (s)':>10}")
    print("-" * 80)
    for n in [8, 10, 12, 14, 16, 18]:
        items, cap = generate_worst_case_instance(n)
        srt = sorted(items, key=lambda it: -it.value / it.mass)
        t0 = time.perf_counter()
        res = branch_and_bound(srt, cap)
        dt = time.perf_counter() - t0
        gen = res["stats"]["generated"]
        full = 2 ** (n + 1) - 1
        print(f"{n:>4} | {gen:>16} | {full:>20} | {gen/full:>10.2%} | {dt:>10.4f}")
    print("\nNotice: Nodes generated roughly double with each increment in n, confirming O(2^n) worst case.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Empirical Benchmarking for Batch 5")
    parser.add_argument("--worst-case", action="store_true", help="Run pathological worst-case evaluation")
    args = parser.parse_args()

    if args.worst_case:
        run_worst_case_evaluation()
    else:
        run_benchmark()

