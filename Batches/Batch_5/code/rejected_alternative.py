"""Batch 5: Rejected Alternatives - Satellite Knapsack Problem.

Course: 23I501 - Design and Analysis of Algorithms (DAA)
Institution: PSG College of Technology

This script implements and evaluates the REJECTED algorithm alternatives:
1. Plain Backtracking (no upper bounding) -> Suffers from exponential 2^n state explosion.
2. Dynamic Programming Table -> Suffers from pseudo-polynomial table size with real-valued masses (0.1 g grid) and memory multiplication under multiple constraints.
3. Greedy by Value Density -> Fails the greedy-choice property; gets trapped in sub-optimal solution.

Usage:
    python rejected_alternative.py
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

UNITS_PER_KG = 10_000


def kg_to_units(kg: float) -> int:
    return round(kg * UNITS_PER_KG)


def fmt_kg(units: int) -> str:
    return f"{units / UNITS_PER_KG:g}"


@dataclass(frozen=True)
class Item:
    name: str
    mass: int
    value: int
    power: int

    @property
    def kg(self) -> float:
        return self.mass / UNITS_PER_KG

    @property
    def density(self) -> float:
        return self.value / self.kg


RAW_DATA = [
    ("P1", 2.5, 40, 8),
    ("P2", 3.2, 42, 12),
    ("P3", 4.8, 60, 10),
    ("P4", 6.1, 72, 15),
    ("P5", 1.7, 18, 4),
    ("P6", 5.4, 54, 9),
]

INSTANCE = [Item(name, kg_to_units(m), v, p) for name, m, v, p in RAW_DATA]
MASS_CAPACITY = kg_to_units(15.0)
POWER_CAPACITY = 35


# -------------------------------------------------------------------------
# Rejected Alternative 1: Plain Backtracking without Upper Bounding
# -------------------------------------------------------------------------
def plain_backtracking(items: List[Item], cap: int) -> Tuple[int, Tuple[str, ...], int]:
    """Exhaustive recursive search with only feasibility pruning (no bounding)."""
    n = len(items)
    best_val = 0
    best_set: Tuple[str, ...] = ()
    nodes_visited = 0

    def search(index: int, current_val: int, current_mass: int, chosen: Tuple[str, ...]):
        nonlocal best_val, best_set, nodes_visited
        nodes_visited += 1

        if current_val > best_val:
            best_val = current_val
            best_set = chosen

        if index == n:
            return

        item = items[index]
        # Include branch if feasible
        if current_mass + item.mass <= cap:
            search(index + 1, current_val + item.value, current_mass + item.mass, chosen + (item.name,))
        # Exclude branch (always feasible)
        search(index + 1, current_val, current_mass, chosen)

    search(0, 0, 0, ())
    return best_val, best_set, nodes_visited


# -------------------------------------------------------------------------
# Rejected Alternative 2: Table-Based Dynamic Programming
# -------------------------------------------------------------------------
def dynamic_programming_knapsack(items: List[Item], cap: int) -> Tuple[int, Tuple[str, ...], int]:
    """Classical 0/1 knapsack DP over integer mass grid."""
    n = len(items)
    # 1D array for value, 2D bitmask table for reconstruction
    dp = [0] * (cap + 1)
    keep = [bytearray(cap + 1) for _ in range(n)]

    for i, item in enumerate(items):
        w = item.mass
        v = item.value
        row = keep[i]
        for j in range(cap, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
                row[j] = 1

    # Backtrack reconstruction
    curr_w = cap
    chosen = []
    for i in range(n - 1, -1, -1):
        if keep[i][curr_w]:
            chosen.append(items[i].name)
            curr_w -= items[i].mass

    total_cells = (n + 1) * (cap + 1)
    return dp[cap], tuple(reversed(chosen)), total_cells


# -------------------------------------------------------------------------
# Rejected Alternative 3: Greedy by Value Density
# -------------------------------------------------------------------------
def greedy_density(items: List[Item], cap: int, stop_at_first: bool = True) -> Tuple[int, Tuple[str, ...], int]:
    """Sort by value per kg and greedily take items."""
    sorted_items = sorted(items, key=lambda it: -it.value / it.mass)
    chosen = []
    tot_val = 0
    tot_mass = 0

    for it in sorted_items:
        if tot_mass + it.mass <= cap:
            chosen.append(it.name)
            tot_val += it.value
            tot_mass += it.mass
        elif stop_at_first:
            break

    return tot_val, tuple(chosen), tot_mass


def main():
    print("=" * 75)
    print("DAA ASSIGNMENT - BATCH 5: EVALUATION OF REJECTED ALTERNATIVES")
    print("=" * 75)

    print("\n--- 1. Plain Backtracking (Without Upper Bounding) ---")
    t0 = time.perf_counter()
    bt_val, bt_set, bt_nodes = plain_backtracking(INSTANCE, MASS_CAPACITY)
    bt_time = time.perf_counter() - t0
    print(f"Optimal Value Found: {bt_val}")
    print(f"Optimal Selection  : {bt_set}")
    print(f"Nodes Explored     : {bt_nodes} (explores all feasible subtrees)")
    print(f"Execution Time     : {bt_time * 1000:.3f} ms")
    print("Why Rejected       : Lacks bounding. For n=20, backtracking explores 1,224,390 nodes")
    print("                     while Branch & Bound explores only 1,909 nodes (a 641x reduction).")

    print("\n--- 2. Dynamic Programming on Discrete Mass Grid ---")
    t0 = time.perf_counter()
    dp_val, dp_set, dp_cells = dynamic_programming_knapsack(INSTANCE, MASS_CAPACITY)
    dp_time = time.perf_counter() - t0
    print(f"Optimal Value Found: {dp_val}")
    print(f"Optimal Selection  : {dp_set}")
    print(f"DP Table Dimensions: (n + 1) = {len(INSTANCE)+1} rows x (W + 1) = {MASS_CAPACITY+1} columns")
    print(f"Total Table Cells  : {dp_cells:,} cells ({dp_cells * 4 / (1024*1024):.2f} MB)")
    print(f"Execution Time     : {dp_time * 1000:.3f} ms")
    print("Why Rejected       : Pseudo-polynomial complexity O(nW). At 0.1 g precision, W = 150,000.")
    print("                     With the +35 W power limit, DP requires a 3D table: (n+1) x (W+1) x (P+1)")
    print(f"                     = 7 x 150,001 x 36 = {7 * 150001 * 36:,} cells (~147 MB),")
    print("                     rendering DP infeasible for multi-constrained continuous systems.")

    print("\n--- 3. Greedy Heuristic by Value Density ---")
    g1_val, g1_set, g1_mass = greedy_density(INSTANCE, MASS_CAPACITY, stop_at_first=True)
    g2_val, g2_set, g2_mass = greedy_density(INSTANCE, MASS_CAPACITY, stop_at_first=False)
    print(f"Variant A (Stop at first misfit) : Selection {g1_set}, Value {g1_val}, Mass {fmt_kg(g1_mass)} kg")
    print(f"Variant B (Skip misfits & scan)  : Selection {g2_set}, Value {g2_val}, Mass {fmt_kg(g2_mass)} kg")
    print(f"True Optimum                     : Selection {bt_set}, Value {bt_val}, Mass 14.1 kg")
    print(f"Suboptimality Deficit            : Greedy loses {bt_val - g2_val} value units ({((bt_val - g2_val) / bt_val)*100:.1f}% error)")
    print("Why Rejected       : Knapsack lacks matroid structure / greedy-choice property.")
    print("                     Greedy packs P1 (highest density, 16.0 val/kg), which prevents")
    print("                     packing the bulky, high-value instrument P4 (11.80 val/kg).")


if __name__ == "__main__":
    main()

