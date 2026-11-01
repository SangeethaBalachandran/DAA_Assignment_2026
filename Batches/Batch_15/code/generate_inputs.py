"""
DAA Assignment 2026 - Batch 15: Cloud VM Consolidation
Script: generate_inputs.py (Generates test inputs & executes empirical timing harness)
Author: Member 1 (Lead)
"""

import os
import random
import time
import csv
import math

# Configure matplotlib for headless environments
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_random_vm_demands(n: int, min_vcpu: int = 2, max_vcpu: int = 9) -> list:
    """Generates synthetic VM vCPU allocations in [min_vcpu, max_vcpu]."""
    return [random.randint(min_vcpu, max_vcpu) for _ in range(n)]

def run_ffd(items: list, capacity: int = 16) -> int:
    sorted_items = sorted(items, reverse=True)
    bins = []
    rem = []
    for item in sorted_items:
        placed = False
        for i in range(len(bins)):
            if rem[i] >= item:
                bins[i].append(item)
                rem[i] -= item
                placed = True
                break
        if not placed:
            bins.append([item])
            rem.append(capacity - item)
    return len(bins)

def solve_branch_and_bound(items: list, capacity: int = 16) -> dict:
    sorted_items = sorted(items, reverse=True)
    n = len(sorted_items)
    best_bins = run_ffd(sorted_items, capacity)
    best_sol = []
    nodes = 0
    t0 = time.perf_counter()

    suffix_sums = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sums[i] = suffix_sums[i + 1] + sorted_items[i]

    def search(idx, current_bins, bin_rem):
        nonlocal best_bins, best_sol, nodes
        nodes += 1
        if idx == n:
            if len(current_bins) < best_bins:
                best_bins = len(current_bins)
                best_sol = [list(b) for b in current_bins]
            return

        item = sorted_items[idx]
        open_slack = sum(bin_rem)
        needed = math.ceil(max(0, suffix_sums[idx] - open_slack) / capacity)
        if len(current_bins) + needed >= best_bins:
            return

        seen_rem = set()
        for b in range(len(current_bins)):
            if bin_rem[b] >= item:
                if bin_rem[b] in seen_rem:
                    continue
                seen_rem.add(bin_rem[b])
                current_bins[b].append(item)
                bin_rem[b] -= item
                search(idx + 1, current_bins, bin_rem)
                bin_rem[b] += item
                current_bins[b].pop()

        if len(current_bins) + 1 < best_bins:
            current_bins.append([item])
            bin_rem.append(capacity - item)
            search(idx + 1, current_bins, bin_rem)
            bin_rem.pop()
            current_bins.pop()

    search(0, [], [])
    elapsed = time.perf_counter() - t0
    return {"bins": best_bins, "nodes": nodes, "time_ms": elapsed * 1000}

def solve_pure_backtracking(items: list, capacity: int = 16, timeout_sec: float = 3.0) -> dict:
    n = len(items)
    best_bins = n + 1
    nodes = 0
    t0 = time.perf_counter()
    timed_out = False

    def search(idx, current_bins, bin_rem):
        nonlocal best_bins, nodes, timed_out
        if time.perf_counter() - t0 > timeout_sec:
            timed_out = True
            return
        nodes += 1
        if idx == n:
            if len(current_bins) < best_bins:
                best_bins = len(current_bins)
            return

        item = items[idx]
        for b in range(len(current_bins)):
            if bin_rem[b] >= item:
                current_bins[b].append(item)
                bin_rem[b] -= item
                search(idx + 1, current_bins, bin_rem)
                if timed_out: return
                bin_rem[b] += item
                current_bins[b].pop()

        current_bins.append([item])
        bin_rem.append(capacity - item)
        search(idx + 1, current_bins, bin_rem)
        if timed_out: return
        bin_rem.pop()
        current_bins.pop()

    search(0, [], [])
    elapsed = time.perf_counter() - t0
    return {"bins": best_bins, "nodes": nodes, "time_ms": elapsed * 1000, "timed_out": timed_out}

def main():
    random.seed(42)
    sizes = [6, 8, 10, 12, 14, 16]
    results = []

    print("Running DAA Batch 15 Empirical Benchmark Harness...")
    for n in sizes:
        bb_times, bt_times, ffd_times = [], [], []
        for _ in range(3):
            data = generate_random_vm_demands(n)
            
            t_start = time.perf_counter()
            run_ffd(data)
            ffd_times.append((time.perf_counter() - t_start) * 1000)

            bb_res = solve_branch_and_bound(data)
            bb_times.append(bb_res["time_ms"])

            if n <= 14:
                bt_res = solve_pure_backtracking(data)
                bt_times.append(bt_res["time_ms"])
            else:
                bt_times.append(3000.0)

        results.append({
            "n": n,
            "time_chosen_ms": sum(bb_times) / len(bb_times),
            "time_rejected_ms": sum(bt_times) / len(bt_times),
            "time_ffd_ms": sum(ffd_times) / len(ffd_times)
        })
        print(f"  N = {n:2d} -> B&B: {results[-1]['time_chosen_ms']:.3f} ms | Rejected BT: {results[-1]['time_rejected_ms']:.3f} ms")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    csv_path = os.path.join(results_dir, "timing.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "time_chosen_ms", "time_rejected_ms", "time_ffd_ms"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved: {csv_path}")

    # Plot
    plot_path = os.path.join(results_dir, "timing_plot.png")
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ns = [r["n"] for r in results]
    ax.plot(ns, [r["time_rejected_ms"] for r in results], 'r-o', linewidth=2, label="Pure Backtracking (Rejected Alternative)")
    ax.plot(ns, [r["time_chosen_ms"] for r in results], 'b-s', linewidth=2, label="Branch & Bound (Chosen Main Solution)")
    ax.plot(ns, [r["time_ffd_ms"] for r in results], 'g-^', linewidth=2, label="FFD Heuristic")
    ax.set_yscale('log')
    ax.set_xlabel('Number of VMs (n)', fontweight='bold')
    ax.set_ylabel('Execution Time in ms (Log Scale)', fontweight='bold')
    ax.set_title('DAA Batch 15: Empirical Scaling Analysis', fontweight='bold')
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    print(f"Saved: {plot_path}")

if __name__ == "__main__":
    main()
