
"""
DAA Assignment 2026 - Batch 15: Cloud VM Consolidation
Module: Heuristics & Data Structures
"""

from typing import List, Tuple, Dict, Any


class SegmentTree:
    """Max Segment Tree for finding the first server with enough free space."""

    def __init__(self, size: int, initial_capacity: int):
        if size <= 0:
            raise ValueError("Size must be positive")

        self.n = size
        self.tree = [0] * (4 * size)
        self.build(1, 0, size - 1, initial_capacity)

    def build(self, node: int, start: int, end: int, capacity: int):
        if start == end:
            self.tree[node] = capacity
            return

        mid = (start + end) // 2
        self.build(2 * node, start, mid, capacity)
        self.build(2 * node + 1, mid + 1, end, capacity)
        self.tree[node] = max(
            self.tree[2 * node], self.tree[2 * node + 1]
        )

    def query_first_fit(self, node: int, start: int,
                        end: int, val: int) -> int:
        if self.tree[node] < val:
            return -1

        if start == end:
            return start

        mid = (start + end) // 2

        if self.tree[2 * node] >= val:
            return self.query_first_fit(
                2 * node, start, mid, val
            )

        return self.query_first_fit(
            2 * node + 1, mid + 1, end, val
        )

    def update(self, node: int, start: int, end: int,
               idx: int, new_val: int):
        if start == end:
            self.tree[node] = new_val
            return

        mid = (start + end) // 2

        if idx <= mid:
            self.update(2 * node, start, mid, idx, new_val)
        else:
            self.update(2 * node + 1, mid + 1, end, idx, new_val)

        self.tree[node] = max(
            self.tree[2 * node], self.tree[2 * node + 1]
        )


def validate(items: List[int], capacity: int):
    if capacity <= 0:
        raise ValueError("Bin capacity must be positive")

    if any(item <= 0 or item > capacity for item in items):
        raise ValueError("Each item must be between 1 and capacity")


def first_fit_decreasing(
    items: List[int], bin_capacity: int
) -> Tuple[List[List[int]], List[Dict[str, Any]]]:
    """FFD using a Segment Tree. Returns bins and trace log."""

    validate(items, bin_capacity)
    sorted_items = sorted(items, reverse=True)

    if not sorted_items:
        return [], []

    tree = SegmentTree(len(sorted_items), bin_capacity)
    bins = []
    bin_rem = []
    trace_log = []

    for item in sorted_items:
        idx = tree.query_first_fit(
            1, 0, tree.n - 1, item
        )

        step_info = {
            "item": item,
            "action": None,
            "bin_idx": None,
            "state_after": None
        }

        if idx == len(bins):
            bins.append([item])
            bin_rem.append(bin_capacity - item)
            step_info["action"] = (
                f"Opened new Server {idx + 1} with VM {item}"
            )
        else:
            bins[idx].append(item)
            bin_rem[idx] -= item
            step_info["action"] = (
                f"Placed {item} in existing Server {idx + 1}"
            )

        tree.update(
            1, 0, tree.n - 1, idx, bin_rem[idx]
        )

        step_info["bin_idx"] = idx + 1
        step_info["state_after"] = [
            {
                "server": i + 1,
                "vms": list(bins[i]),
                "used": bin_capacity - bin_rem[i],
                "free": bin_rem[i]
            }
            for i in range(len(bins))
        ]

        trace_log.append(step_info)

    return bins, trace_log


def best_fit_decreasing(
    items: List[int], bin_capacity: int
) -> List[List[int]]:
    """BFD: choose the server leaving the least free space."""

    validate(items, bin_capacity)
    sorted_items = sorted(items, reverse=True)
    bins = []
    bin_rem = []

    for item in sorted_items:
        best_idx = -1
        min_rem = bin_capacity + 1

        for i in range(len(bins)):
            if bin_rem[i] >= item and bin_rem[i] - item < min_rem:
                min_rem = bin_rem[i] - item
                best_idx = i

        if best_idx == -1:
            bins.append([item])
            bin_rem.append(bin_capacity - item)
        else:
            bins[best_idx].append(item)
            bin_rem[best_idx] -= item

    return bins


def get_ffd_counterexample() -> Dict[str, Any]:
    """Return the assignment's FFD counterexample."""

    items = [7, 6, 5, 5, 5, 4]
    capacity = 16

    bins_ffd, trace = first_fit_decreasing(items, capacity)
    optimal_packing = [[7, 5, 4], [6, 5, 5]]

    return {
        "capacity": capacity,
        "items": items,
        "optimal_bins": optimal_packing,
        "optimal_count": len(optimal_packing),
        "ffd_bins": bins_ffd,
        "ffd_count": len(bins_ffd),
        "trace": trace
    }


if __name__ == "__main__":
    test_instance = [9, 8, 7, 6, 5, 4, 3, 2]
    capacity = 16

    bins, trace = first_fit_decreasing(test_instance, capacity)

    print("=== Segment Tree FFD ===")
    print("Input:", test_instance)
    print("Total servers:", len(bins))

    for i, server in enumerate(bins, 1):
        print(
            f"Server {i}: {server}, "
            f"Used: {sum(server)}/{capacity}, "
            f"Free: {capacity - sum(server)}"
        )

    print("\n=== FFD Counterexample ===")
    result = get_ffd_counterexample()
    print("Optimal:", result["optimal_bins"])
    print("FFD:", result["ffd_bins"])
    print("Optimal server count:", result["optimal_count"])
    print("FFD server count:", result["ffd_count"])
