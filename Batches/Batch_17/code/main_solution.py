"""
main_solution.py  --  Batch 17 (Digital Marketing, 0/1 Knapsack)

CHOSEN TECHNIQUE: Dynamic Programming.

State       dp[i][w] = max conversions using only the first i campaigns with a
                       budget of w lakh.
Recurrence  dp[i][w] = dp[i-1][w]                                   if cost_i > w
            dp[i][w] = max(dp[i-1][w], dp[i-1][w-cost_i] + value_i) otherwise
Base        dp[0][w] = 0 for all w   and   dp[i][0] = 0 for all i
Answer      dp[n][B]

Contents
--------
knapsack_2d      O(nB) time, O(nB) space, can reconstruct the chosen campaigns
knapsack_1d      O(nB) time, O(B)  space, value only (memory-optimised)
count_updates    exact number of cell updates the DP performs
fptas            profit-scaling approximation scheme  (changed requirement)
cost_scaled_dp   cost-rounding DP, always feasible      (changed requirement)
brute_force      reference answer used by --selftest
benchmark        timing DP vs Greedy -> ../results/timing.csv + timing_plot.png

Run  `python main_solution.py --help`  or read RUN.md.
"""
import argparse
import csv
import itertools
import os
import random
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from generate_inputs import (given_instance, generate, worst_case,  # noqa: E402
                             large_instance, BENCH_SIZES)
from rejected_alternative import greedy_knapsack                     # noqa: E402

RESULTS_DIR = os.path.join(HERE, "..", "results")


# =============================================================================
#  Core Dynamic Programming
# =============================================================================
def knapsack_2d(costs, values, budget):
    """
    Classic bottom-up table.  Returns (best_value, selected_indices, table).
    selected_indices are 0-based and in increasing order.
    """
    n = len(costs)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]       # base case: row 0 and column 0 are 0
    for i in range(1, n + 1):
        c, v = costs[i - 1], values[i - 1]
        prev, cur = dp[i - 1], dp[i]
        for w in range(budget + 1):
            cur[w] = prev[w]                              # option 1: reject campaign i
            if c <= w and prev[w - c] + v > cur[w]:       # option 2: select campaign i
                cur[w] = prev[w - c] + v
    # ---- traceback --------------------------------------------------------
    selected, w = [], budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:                      # value changed -> campaign i was taken
            selected.append(i - 1)
            w -= costs[i - 1]
    selected.reverse()
    return dp[n][budget], selected, dp


def knapsack_1d(costs, values, budget, history=False):
    """
    Space-optimised version: one array of B+1 cells.
    The inner loop runs from high budget to low budget so that each campaign
    is used at most once (0/1, not unbounded).
    If history=True the array after every campaign is also returned.
    """
    dp = [0] * (budget + 1)
    rows = [dp[:]] if history else None
    for c, v in zip(costs, values):
        for w in range(budget, c - 1, -1):
            cand = dp[w - c] + v
            if cand > dp[w]:
                dp[w] = cand
        if history:
            rows.append(dp[:])
    return (dp[budget], rows) if history else dp[budget]


def count_updates(costs, budget):
    """Number of (i, w) cells whose recurrence is evaluated in the 1-D DP."""
    return sum(max(0, budget - c + 1) for c in costs)


def brute_force(costs, values, budget):
    """Try all 2^n subsets (only for tiny n, used to verify the DP)."""
    best, best_set = 0, ()
    for r in range(len(costs) + 1):
        for combo in itertools.combinations(range(len(costs)), r):
            if sum(costs[i] for i in combo) <= budget:
                val = sum(values[i] for i in combo)
                if val > best:
                    best, best_set = val, combo
    return best, list(best_set)


# =============================================================================
#  Changed requirement: 300 campaigns, budget Rs 4,37,52,900 (precision Rs 1)
# =============================================================================
def fractional_upper_bound(costs, values, budget):
    """LP relaxation (fractional knapsack): an upper bound on OPT."""
    order = sorted(range(len(costs)), key=lambda i: -values[i] / costs[i])
    rem, ub = budget, 0.0
    for i in order:
        if costs[i] <= rem:
            rem -= costs[i]
            ub += values[i]
        else:
            ub += values[i] * rem / costs[i]
            break
    return ub


def fptas(costs, values, budget, eps):
    """
    Profit-scaling FPTAS (Ibarra-Kim style).
      K  = eps * v_max / n
      v' = floor(v / K)                      (small integers, <= n/eps)
      DP over PROFIT:  mincost[p] = cheapest cost reaching scaled profit p
    Result value >= (1 - eps) * OPT.   Time O(n^2 * n/eps) = O(n^3/eps),
    independent of the budget B.   Returns (true_value, selected, scaled_total).
    """
    import numpy as np
    items = [i for i in range(len(costs)) if costs[i] <= budget]
    if not items:
        return 0, [], 0
    vmax = max(values[i] for i in items)
    K = eps * vmax / len(items)
    sv = [int(values[i] // K) for i in items]
    P = sum(sv)
    INF = np.iinfo(np.int64).max // 4
    mincost = np.full(P + 1, INF, dtype=np.int64)
    mincost[0] = 0
    take = np.zeros((len(items), P + 1), dtype=bool)
    reach = 0
    for k, i in enumerate(items):
        s, c = sv[k], costs[i]
        if s == 0:
            continue
        hi = reach + s
        cand = mincost[: hi + 1 - s] + c
        better = cand < mincost[s: hi + 1]
        take[k, s: hi + 1] = better
        mincost[s: hi + 1] = np.where(better, cand, mincost[s: hi + 1])
        reach = hi
    feasible = np.nonzero(mincost[: reach + 1] <= budget)[0]
    p = int(feasible.max())
    best_p, selected = p, []
    for k in range(len(items) - 1, -1, -1):
        if take[k, p]:
            selected.append(items[k])
            p -= sv[k]
    selected.sort()
    return sum(values[i] for i in selected), selected, best_p


def cost_scaled_dp(costs, values, budget, unit):
    """
    Round every cost UP to a multiple of `unit` rupees and the budget DOWN.
    The DP then has only budget//unit columns.  Rounding up guarantees the
    chosen set is feasible for the real budget; the value may be slightly
    below OPT (campaigns that only fit thanks to rounding are lost).
    Returns (true_value, selected, columns).
    """
    import numpy as np
    n = len(costs)
    sc = [-(-c // unit) for c in costs]      # ceil
    B = budget // unit                       # floor
    dp = np.zeros(B + 1, dtype=np.int64)
    take = np.zeros((n, B + 1), dtype=bool)
    for i in range(n):
        c, v = sc[i], values[i]
        if c > B:
            continue
        cand = dp[: B + 1 - c] + v
        better = cand > dp[c:]
        take[i, c:] = better
        dp[c:] = np.where(better, cand, dp[c:])
    w, selected = B, []
    for i in range(n - 1, -1, -1):
        if take[i, w]:
            selected.append(i)
            w -= sc[i]
    selected.sort()
    return int(dp[B]), selected, B + 1


# =============================================================================
#  Pretty printing / trace
# =============================================================================
def run_given(trace=False):
    names, costs, values, budget = given_instance()
    best, sel, table = knapsack_2d(costs, values, budget)
    best1, rows = knapsack_1d(costs, values, budget, history=True)
    g_val, g_sel, g_cost = greedy_knapsack(costs, values, budget)

    if trace:
        print("TRACE of the 1-D DP array  dp[w], w = 0..%d" % budget)
        print(f"{'after':<12}" + "".join(f"{w:>5}" for w in range(budget + 1)))
        print(f"{'init':<12}" + "".join(f"{x:>5}" for x in rows[0]))
        for i, r in enumerate(rows[1:]):
            lab = f"{names[i]}(c={costs[i]},v={values[i]})"
            print(f"{lab:<12}" + "".join(f"{x:>5}" for x in r))
        print("\n2-D table  dp[i][w]  (used for traceback)")
        print(f"{'':<5}" + "".join(f"{w:>5}" for w in range(budget + 1)))
        for i, row in enumerate(table):
            print(f"{('i=%d' % i):<5}" + "".join(f"{x:>5}" for x in row))
        print("\nTraceback from dp[%d][%d] = %d" % (len(costs), budget, best))
        w = budget
        for i in range(len(costs), 0, -1):
            took = table[i][w] != table[i - 1][w]
            print(f"  i={i} ({names[i-1]}): dp[{i}][{w}]={table[i][w]}, dp[{i-1}][{w}]={table[i-1][w]}"
                  f" -> {'TAKE' if took else 'skip'}")
            if took:
                w -= costs[i - 1]
        print()

    print("Dynamic Programming result")
    print("  selected   :", [names[i] for i in sel])
    print("  total cost :", sum(costs[i] for i in sel), "lakh")
    print("  conversions:", best, "(1-D check:", best1, ")")
    print("Greedy result")
    print("  selected   :", [names[i] for i in g_sel])
    print("  total cost :", g_cost, "lakh")
    print("  conversions:", g_val)
    print("Greedy loses", best - g_val, "conversions "
          f"({100 * (best - g_val) / best:.2f}% below optimal)")


# =============================================================================
#  Self test
# =============================================================================
def selftest():
    rng = random.Random(2026)
    for t in range(300):
        n = rng.randint(1, 11)
        costs = [rng.randint(1, 12) for _ in range(n)]
        values = [rng.randint(1, 60) for _ in range(n)]
        B = rng.randint(1, 40)
        bf, _ = brute_force(costs, values, B)
        v2, sel, _ = knapsack_2d(costs, values, B)
        v1 = knapsack_1d(costs, values, B)
        assert v2 == v1 == bf, (costs, values, B, v2, v1, bf)
        assert sum(costs[i] for i in sel) <= B and sum(values[i] for i in sel) == v2
        g, _, gc = greedy_knapsack(costs, values, B)
        assert g <= bf and gc <= B
    for t in range(60):
        n = rng.randint(5, 25)
        costs = [rng.randint(1, 50) for _ in range(n)]
        values = [rng.randint(1, 500) for _ in range(n)]
        B = rng.randint(20, 300)
        opt = knapsack_1d(costs, values, B)
        for eps in (0.5, 0.2, 0.1):
            fv, fs, _ = fptas(costs, values, B, eps)
            assert sum(costs[i] for i in fs) <= B
            assert fv >= (1 - eps) * opt - 1e-9, (fv, opt, eps)
    n, c, v, B = given_instance()[0], *given_instance()[1:]
    assert knapsack_2d(c, v, B)[0] == 127 and greedy_knapsack(c, v, B)[0] == 125
    print("selftest passed: DP(2D) == DP(1D) == brute force on 300 random cases;")
    print("FPTAS >= (1-eps)*OPT on 180 cases; given instance DP=127, Greedy=125.")


# =============================================================================
#  Benchmark
# =============================================================================
def time_ms(fn, repeats):
    """Median wall-clock time of fn() in milliseconds."""
    samples = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - t0) * 1000)
    return statistics.median(samples)


def benchmark(write=True):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows = []
    print(f"{'n':>6}{'B':>8}{'DP 2D ms':>12}{'DP 1D ms':>12}{'Greedy ms':>12}{'DP val':>9}{'Greedy val':>11}{'Gap %':>8}")
    for n in BENCH_SIZES:
        names, costs, values, B = generate(n)          # SAME dataset for both algorithms
        reps = 7 if n <= 200 else 3
        t_dp2 = time_ms(lambda: knapsack_2d(costs, values, B), reps)
        t_dp1 = time_ms(lambda: knapsack_1d(costs, values, B), reps)
        t_gr = time_ms(lambda: greedy_knapsack(costs, values, B), max(reps, 15))
        dp_val = knapsack_1d(costs, values, B)
        gr_val = greedy_knapsack(costs, values, B)[0]
        assert dp_val == knapsack_2d(costs, values, B)[0]
        gap = 100 * (dp_val - gr_val) / dp_val
        rows.append(dict(n=n, budget=B, dp_2d_ms=round(t_dp2, 4), dp_1d_ms=round(t_dp1, 4),
                         greedy_ms=round(t_gr, 4), dp_value=dp_val, greedy_value=gr_val,
                         greedy_gap_percent=round(gap, 3), dp_cell_updates=count_updates(costs, B)))
        print(f"{n:>6}{B:>8}{t_dp2:>12.3f}{t_dp1:>12.3f}{t_gr:>12.4f}{dp_val:>9}{gr_val:>11}{gap:>8.2f}")
    if write:
        path = os.path.join(RESULTS_DIR, "timing.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print("wrote", os.path.normpath(path))
        plot(rows)
    return rows


def plot(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = [r["n"] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for a, log in zip(ax, (False, True)):
        a.plot(n, [r["dp_2d_ms"] for r in rows], "o-", color="#1f5fbf", lw=2, label="Dynamic Programming (O(nB))")
        a.plot(n, [r["greedy_ms"] for r in rows], "s-", color="#d9531e", lw=2, label="Greedy (O(n log n))")
        a.set_xlabel("Number of campaigns (n)")
        a.set_ylabel("Execution time (ms)")
        a.grid(alpha=.3)
        if log:
            a.set_yscale("log")
            a.set_title("Same data, log scale")
        else:
            a.set_title("Execution time vs input size")
        a.legend()
    fig.tight_layout()
    path = os.path.join(RESULTS_DIR, "timing_plot.png")
    fig.savefig(path, dpi=160)
    print("wrote", os.path.normpath(path))


# =============================================================================
#  Worst case and large instance demos
# =============================================================================
def worst_demo():
    print(f"{'n':>6}{'B':>8}{'n*B':>12}{'cell updates':>14}{'time ms (1D)':>14}")
    for n in (50, 100, 200, 400):
        _, c, v, B = worst_case(n)
        t = time_ms(lambda: knapsack_1d(c, v, B), 3)
        print(f"{n:>6}{B:>8}{n * B:>12}{count_updates(c, B):>14}{t:>14.2f}")


def large_demo(eps=0.1, unit=1000):
    names, costs, values, B = large_instance()
    n = len(costs)
    print(f"n = {n}, B = Rs {B:,} (precision Rs 1)")
    print(f"  plain DP cells (n*B)          : {n * B:,}")
    print(f"  2-D table, 4 bytes/cell       : {n * (B + 1) * 4 / 1e9:,.1f} GB")
    print(f"  1-D array, 8 bytes/cell       : {(B + 1) * 8 / 1e6:,.0f} MB (time still ~{n * B / 1e9:.1f} x 10^9 updates)")
    ub = fractional_upper_bound(costs, values, B)
    print(f"  LP upper bound on OPT         : {ub:,.1f}")
    t0 = time.perf_counter()
    fv, fs, p = fptas(costs, values, B, eps)
    t1 = time.perf_counter()
    print(f"FPTAS eps={eps}: value {fv:,}  ({100 * fv / ub:.2f}% of LP bound), "
          f"{len(fs)} campaigns, cost Rs {sum(costs[i] for i in fs):,}, {t1 - t0:.2f}s")
    t0 = time.perf_counter()
    cv, cs, cols = cost_scaled_dp(costs, values, B, unit)
    t1 = time.perf_counter()
    print(f"Cost-scaled DP unit=Rs {unit}: value {cv:,}  ({100 * cv / ub:.2f}% of LP bound), "
          f"{cols:,} columns, cost Rs {sum(costs[i] for i in cs):,}, {t1 - t0:.2f}s")
    g, gs, gc = greedy_knapsack(costs, values, B)
    print(f"Greedy                       : value {g:,}  ({100 * g / ub:.2f}% of LP bound)")


# =============================================================================
def main():
    ap = argparse.ArgumentParser(description="0/1 Knapsack by Dynamic Programming (Batch 17)")
    ap.add_argument("--trace", action="store_true", help="print every DP table of the given instance")
    ap.add_argument("--selftest", action="store_true", help="verify DP against brute force")
    ap.add_argument("--benchmark", action="store_true", help="time DP vs Greedy, write ../results/")
    ap.add_argument("--worst", action="store_true", help="worst-case input demo")
    ap.add_argument("--large", action="store_true", help="changed requirement: 300 campaigns, Rs 4,37,52,900")
    args = ap.parse_args()

    if args.selftest:
        selftest()
    elif args.benchmark:
        benchmark()
    elif args.worst:
        worst_demo()
    elif args.large:
        large_demo()
    else:
        run_given(trace=args.trace)


if __name__ == "__main__":
    main()
