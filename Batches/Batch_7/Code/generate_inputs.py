"""Input generators for Batch 7 (exam timetabling = graph colouring).
Graphs are lists of sets: adj[v] = set of conflicting courses.
CLI: python3 generate_inputs.py   -> writes edge lists to ./inputs/
"""
import random, os

COURSES = ["DAA", "OS", "DBMS", "ML", "CN", "SE", "Maths"]
CONFLICTS = [("DAA","OS"),("DAA","DBMS"),("DAA","ML"),("OS","CN"),("OS","DBMS"),
             ("DBMS","SE"),("CN","ML"),("ML","Maths"),("SE","Maths"),("CN","SE")]

def from_edges(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return adj

def instance7():
    idx = {c: i for i, c in enumerate(COURSES)}
    return from_edges(7, [(idx[a], idx[b]) for a, b in CONFLICTS])

def random_graph(n, p, seed=1):
    rnd = random.Random(seed)
    return from_edges(n, [(u, v) for u in range(n) for v in range(u+1, n) if rnd.random() < p])

def mycielski(adj):
    """Mycielskian: triangle-free-preserving, chromatic number +1. Hard 'no' instances."""
    n = len(adj)
    edges = [(u, v) for u in range(n) for v in adj[u] if u < v]
    new = list(edges)
    for u, v in edges:                 # shadow vertices n..2n-1
        new.append((u, n + v)); new.append((v, n + u))
    for u in range(n):
        new.append((n + u, 2 * n))     # apex 2n
    return from_edges(2 * n + 1, new)

def mycielski_k(k):
    """Graph with chromatic number k and clique number 2 (k>=2)."""
    g = from_edges(2, [(0, 1)])
    for _ in range(k - 2):
        g = mycielski(g)
    return g

def greedy_trap():
    """Tree (2-colourable). Welsh-Powell (descending degree, lowest free slot) uses 3 slots.
    u,v have degree 3; w,z degree 2; l1,l2 hang on u; m1,m2 hang on v. Path u-w-z-v."""
    names = ["u","v","w","z","l1","l2","m1","m2"]
    i = {s: k for k, s in enumerate(names)}
    e = [("u","w"),("w","z"),("z","v"),("u","l1"),("u","l2"),("v","m1"),("v","m2")]
    return names, from_edges(8, [(i[a], i[b]) for a, b in e])

def write_edgelist(path, adj):
    with open(path, "w") as f:
        f.write(f"{len(adj)}\n")
        for u in range(len(adj)):
            for v in adj[u]:
                if u < v: f.write(f"{u} {v}\n")

if __name__ == "__main__":
    os.makedirs("inputs", exist_ok=True)
    write_edgelist("inputs/instance7.txt", instance7())
    write_edgelist("inputs/greedy_trap.txt", greedy_trap()[1])
    write_edgelist("inputs/mycielski5.txt", mycielski_k(5))
    write_edgelist("inputs/random420.txt", random_graph(420, 0.05, seed=7))
    print("wrote inputs/*.txt")
