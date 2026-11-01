"""
DAA Assignment 2026 - Batch 15: Cloud VM Consolidation
Module: Rejected Alternative - Pure Unbounded Backtracking (Combinatorial Explosion)
"""

import time
from typing import List, Dict, Any

class PureBacktrackingBinPacking:
    """
    Pure Backtracking (Exhaustive Search without Lower Bounding or Symmetry Breaking).
    Examines all item-to-bin assignments without lower bound pruning.
    Suffers from exponential state explosion O(m^n), exploring redundant symmetric permutations.
    """
    def __init__(self, items: List[int], capacity: int):
        self.items = list(items)  # Note: unsorted or arbitrary order
        self.capacity = capacity
        self.n = len(self.items)
        self.nodes_explored = 0
        self.best_bin_count = self.n + 1
        self.best_solution: List[List[int]] = []

    def solve(self, time_limit_sec: float = 5.0) -> Dict[str, Any]:
        start_time = time.perf_counter()
        self.nodes_explored = 0
        self.best_bin_count = self.n + 1
        self.best_solution = []
        timed_out = False

        def search(item_idx: int, current_bins: List[List[int]], bin_remaining: List[int]):
            nonlocal timed_out
            if time.perf_counter() - start_time > time_limit_sec:
                timed_out = True
                return

            self.nodes_explored += 1

            if item_idx == self.n:
                if len(current_bins) < self.best_bin_count:
                    self.best_bin_count = len(current_bins)
                    self.best_solution = [list(b) for b in current_bins]
                return

            item = self.items[item_idx]

            # Try placing item in EVERY existing bin that can fit it
            # (No symmetry check for identical capacities)
            for b in range(len(current_bins)):
                if bin_remaining[b] >= item:
                    current_bins[b].append(item)
                    bin_remaining[b] -= item

                    search(item_idx + 1, current_bins, bin_remaining)
                    if timed_out:
                        return

                    bin_remaining[b] += item
                    current_bins[b].pop()

            # Also try placing in a new bin (no lower bound check against best_bin_count)
            current_bins.append([item])
            bin_remaining.append(self.capacity - item)

            search(item_idx + 1, current_bins, bin_remaining)
            if timed_out:
                return

            bin_remaining.pop()
            current_bins.pop()

        search(0, [], [])
        elapsed = time.perf_counter() - start_time

        return {
            "optimal_bins": self.best_solution,
            "optimal_count": self.best_bin_count,
            "nodes_explored": self.nodes_explored,
            "elapsed_seconds": elapsed,
            "timed_out": timed_out
        }


if __name__ == "__main__":
    instance = [9, 8, 7, 6, 5, 4, 3, 2]
    capacity = 16
    print(f"Solving Batch 15 Instance {instance} (C = {capacity}) with Pure Backtracking...")
    solver = PureBacktrackingBinPacking(instance, capacity)
    res = solver.solve()
    print(f"Best Servers Found: {res['optimal_count']}")
    print(f"Nodes Explored: {res['nodes_explored']} (vs Branch & Bound: 11 nodes!)")
    print(f"Time Taken: {res['elapsed_seconds']*1000:.3f} ms")
