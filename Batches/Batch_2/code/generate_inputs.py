"""
Generate deterministic random connected weighted graphs for timing tests.
Output: generated_inputs.json in the current directory.
Run: python generate_inputs.py
"""

import json
import random


def generate_graph(vertex_count, extra_edge_probability=0.35, seed=42):
    rng = random.Random(seed)
    vertices = [f"V{i}" for i in range(vertex_count)]
    edges = []

    # First create a connected backbone so an MST always exists.
    for i in range(1, vertex_count):
        parent = rng.randrange(i)
        edges.append([vertices[parent], vertices[i], rng.randint(1, 100)])

    # Then add some extra edges to make the graph more realistic.
    for i in range(vertex_count):
        for j in range(i + 1, vertex_count):
            if rng.random() < extra_edge_probability:
                pair = {vertices[i], vertices[j]}
                if not any({edge[0], edge[1]} == pair for edge in edges):
                    edges.append([vertices[i], vertices[j], rng.randint(1, 100)])

    return {"vertices": vertices, "edges": edges}


if __name__ == "__main__":
    data = {
        "description": "Generated weighted graphs for MST timing experiments",
        "graphs": [
            generate_graph(10, seed=42),
            generate_graph(25, seed=43),
            generate_graph(50, seed=44),
            generate_graph(100, seed=45),
        ],
    }

    with open("generated_inputs.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print("Generated generated_inputs.json")
    print("Graph sizes: 10, 25, 50, and 100 vertices")
