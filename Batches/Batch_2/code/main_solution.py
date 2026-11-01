"""
Telecom: Fibre Rollout Connecting Towns
Chosen algorithm: Kruskal's Minimum Spanning Tree (MST)
Run: python main_solution.py
"""

from time import perf_counter


TOWNS = {
    "CBE": "Coimbatore",
    "TUP": "Tiruppur",
    "ERD": "Erode",
    "SLM": "Salem",
    "POL": "Pollachi",
    "MTP": "Mettupalayam",
    "UDM": "Udumalpet",
}

# Each edge: (town 1, town 2, cost in lakh rupees)
EDGES = [
    ("CBE", "TUP", 5),
    ("CBE", "POL", 4),
    ("CBE", "MTP", 3),
    ("CBE", "ERD", 9),
    ("TUP", "ERD", 5),
    ("TUP", "UDM", 6),
    ("POL", "UDM", 4),
    ("ERD", "SLM", 6),
    ("TUP", "SLM", 10),
    ("MTP", "ERD", 11),
    ("POL", "TUP", 7),
]


class DSU:
    """Disjoint Set Union with path compression and union by rank."""

    def __init__(self, vertices):
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}

    def find(self, vertex):
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, first, second):
        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return False

        if self.rank[root_first] < self.rank[root_second]:
            root_first, root_second = root_second, root_first

        self.parent[root_second] = root_first
        if self.rank[root_first] == self.rank[root_second]:
            self.rank[root_first] += 1
        return True


def kruskal(vertices, edges):
    """Return the MST edges and total cost using Kruskal's algorithm."""
    dsu = DSU(vertices)
    selected = []
    total_cost = 0

    for first, second, cost in sorted(edges, key=lambda edge: edge[2]):
        if dsu.union(first, second):
            selected.append((first, second, cost))
            total_cost += cost
            if len(selected) == len(vertices) - 1:
                break

    if len(selected) != len(vertices) - 1:
        raise ValueError("The graph is disconnected; no spanning tree exists.")

    return selected, total_cost


def main():
    vertices = list(TOWNS)
    start_time = perf_counter()
    tree, total_cost = kruskal(vertices, EDGES)
    elapsed_ms = (perf_counter() - start_time) * 1000

    print("TELECOM: FIBRE ROLLOUT CONNECTING TOWNS")
    print("Chosen algorithm: Kruskal's Minimum Spanning Tree")
    print("All costs are in lakh rupees.\\n")
    print("Selected fibre links:")
    for first, second, cost in tree:
        print(f"{TOWNS[first]} ({first}) -- {TOWNS[second]} ({second}): Rs. {cost} lakh")
    print(f"\\nMinimum total rollout cost: Rs. {total_cost} lakh")
    print(f"Execution time for this input: {elapsed_ms:.3f} ms")


if __name__ == "__main__":
    main()
