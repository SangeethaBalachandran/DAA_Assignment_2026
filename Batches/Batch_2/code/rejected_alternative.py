"""
Rejected alternative: brute-force enumeration of spanning trees.

This is included for comparison only. It enumerates every combination of
|V|-1 edges and checks whether that combination forms a spanning tree.
It is suitable only for very small graphs because the number of combinations
grows rapidly.
"""

from itertools import combinations
from time import perf_counter


def brute_force_mst(vertices, edges):
    best_tree = None
    best_cost = float("inf")

    for candidate in combinations(edges, len(vertices) - 1):
        parent = {vertex: vertex for vertex in vertices}

        def find(vertex):
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        valid = True
        total_cost = 0

        for first, second, cost in candidate:
            root_first = find(first)
            root_second = find(second)

            if root_first == root_second:
                valid = False
                break

            parent[root_second] = root_first
            total_cost += cost

        if valid and len({find(vertex) for vertex in vertices}) == 1:
            if total_cost < best_cost:
                best_cost = total_cost
                best_tree = candidate

    if best_tree is None:
        raise ValueError("No spanning tree exists.")

    return list(best_tree), best_cost


if __name__ == "__main__":
    vertices = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 4),
        ("A", "C", 3),
        ("A", "D", 8),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 6),
    ]

    start = perf_counter()
    tree, cost = brute_force_mst(vertices, edges)
    elapsed_ms = (perf_counter() - start) * 1000

    print("REJECTED ALTERNATIVE: BRUTE-FORCE MST")
    print("Small demonstration graph only")
    for first, second, weight in tree:
        print(f"{first} -- {second}: cost {weight}")
    print(f"Minimum cost: {cost}")
    print(f"Execution time: {elapsed_ms:.3f} ms")
    print("Reason rejected: brute-force enumeration scales poorly as the graph grows.")
