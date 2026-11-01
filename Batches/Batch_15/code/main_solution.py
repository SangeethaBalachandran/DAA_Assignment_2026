
"""
DAA Assignment 2026 - Batch 15
Branch and Bound for VM Consolidation / Bin Packing
"""

from math import ceil


def validate(items, capacity):
    if capacity <= 0:
        raise ValueError("Capacity must be positive.")
    if any(not isinstance(x, int) or x <= 0 or x > capacity for x in items):
        raise ValueError("Each item must be an integer from 1 to capacity.")


def first_fit_decreasing(items, capacity):
    """Return a valid First Fit Decreasing packing."""
    bins = []
    remaining = []

    for item in sorted(items, reverse=True):
        for i, free in enumerate(remaining):
            if free >= item:
                bins[i].append(item)
                remaining[i] -= item
                break
        else:
            bins.append([item])
            remaining.append(capacity - item)

    return bins


def branch_and_bound_bin_packing(items, capacity):
    """Return the optimal packing and number of search nodes explored."""
    validate(items, capacity)
    items = sorted(items, reverse=True)

    if not items:
        return [], 1

    # FFD provides both an upper bound and a valid initial solution.
    best_solution = first_fit_decreasing(items, capacity)
    best_bins = len(best_solution)
    nodes_explored = 0

    current_bins = []
    remaining = []

    suffix_sum = [0] * (len(items) + 1)
    for i in range(len(items) - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + items[i]

    def search(index):
        nonlocal best_solution, best_bins, nodes_explored
        nodes_explored += 1

        if index == len(items):
            if len(current_bins) < best_bins:
                best_bins = len(current_bins)
                best_solution = [b[:] for b in current_bins]
            return

        # Lower bound: remaining demand not covered by current free space.
        free_space = sum(remaining)
        excess = max(0, suffix_sum[index] - free_space)
        lower_bound = ceil(excess / capacity)

        # Equal solutions cannot improve the current best solution.
        if len(current_bins) + lower_bound >= best_bins:
            return

        item = items[index]
        seen_free_space = set()

        # Try placing the item into each distinct bin configuration.
        for i, free in enumerate(remaining):
            if free < item or free in seen_free_space:
                continue
            seen_free_space.add(free)

            current_bins[i].append(item)
            remaining[i] -= item

            search(index + 1)

            remaining[i] += item
            current_bins[i].pop()

        # Open a new bin only if it might improve the best solution.
        if len(current_bins) + 1 < best_bins:
            current_bins.append([item])
            remaining.append(capacity - item)

            search(index + 1)

            remaining.pop()
            current_bins.pop()

    search(0)
    return best_solution, nodes_explored


def packing_is_valid(items, capacity, packing):
    if any(sum(server) > capacity for server in packing):
        return False

    packed_items = sorted(
        item for server in packing for item in server
    )
    return packed_items == sorted(items)


def main():
    items = [9, 8, 7, 6, 5, 4, 3, 2]
    capacity = 16

    packing, nodes = branch_and_bound_bin_packing(items, capacity)

    print("=== Branch and Bound: VM Consolidation ===")
    print("Input VM sizes:", items)
    print("Server capacity:", capacity)
    print("Minimum servers found:", len(packing))

    for i, server in enumerate(packing, start=1):
        used = sum(server)
        print(
            f"Server {i}: {server} | "
            f"Used: {used}/{capacity} | Free: {capacity - used}"
        )

    print("Nodes explored:", nodes)
    print("Packing valid:", packing_is_valid(items, capacity, packing))

    # Example where First Fit Decreasing uses three bins,
    # while the optimal solution uses two.
    test_items = [7, 6, 5, 5, 5, 4]
    test_packing, _ = branch_and_bound_bin_packing(
        test_items, capacity
    )

    print("\n=== Greedy Counterexample Check ===")
    print("Input:", test_items)
    print("Optimal server count:", len(test_packing))

    for i, server in enumerate(test_packing, start=1):
        print(f"Server {i}: {server}")


if __name__ == "__main__":
    main()
