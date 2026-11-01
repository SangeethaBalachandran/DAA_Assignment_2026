#!/usr/bin/env python3
"""extra_experiments.py -- numbers quoted in the report (counts, tolerance study, worst cases)."""
from math import comb
from collections import Counter
from main_solution import solve
from rejected_alternative import brute_force_solve
from generate_inputs import random_instance, hard_instance

A = [15000, 22000, 35000, 40000, 48000, 53000, 61000]
r = solve(A, 110000)
print("== Instance ==")
print("solutions", r.solutions, "states", r.states, "overshoot", r.prune_overshoot,
      "unreachable", r.prune_unreachable, "skipped", r.skipped_children)
# states per subset size
depth = Counter()
def tr(ev, sid, d, vals, cur, info):
    if ev == "visit": depth[d] += 1
solve(A, 110000, 0, trace=tr)
print("states by subset size", dict(sorted(depth.items())))
K = max(k for k in range(8) if sum(sorted(A)[:k]) <= 110000)
print("K (max items that can fit) =", K, " bound sum C(7,k<=K) =", sum(comb(7, k) for k in range(K + 1)))
print("subsets of size>K =", sum(comb(7, k) for k in range(K + 1, 8)))
print("sum of all =", sum(A))

print("\n== Tolerance ==")
B = [15020, 22000, 35000, 39990, 48000, 53030, 61000]
for tol in (0, 50):
    rb = solve(B, 110000, tol)
    print("B tol", tol, "solutions", [(tuple(B[i] for i in s), sum(B[i] for i in s)) for s in rb.solutions], "states", rb.states)
for tol in (0, 50):
    rr = solve(A, 110000, tol); print("A tol", tol, len(rr.solutions), rr.states)
am, tg, _ = random_instance(22, 2026)
print("random n=22 target", tg)
for tol in (0, 50, 500, 5000, 50000):
    rr = solve(am, tg, tol)
    print(f"  tol={tol:>6}: solutions={len(rr.solutions):>6} states={rr.states:>8}")

print("\n== Worst cases ==")
n = 16
rr = solve([1000] * n, 8000, 0)
print("equal items n=16 target 8000: solutions", len(rr.solutions), "= C(16,8) =", comb(16, 8), "states", rr.states, "2^n", 2**n)
rr = solve([1000] * n, 8000, 10**9)
print("n=16 huge tolerance: solutions", len(rr.solutions), "states", rr.states, "2^n", 2**n)
for n in (10, 14, 18, 22):
    a, t, _ = hard_instance(n)
    rr = solve(a, t, 0)
    print(f"hard n={n}: states={rr.states} C(n,n/2)={comb(n, n//2)} 2^n={2**n} ratio={rr.states/2**n:.3f} "
          f"overshoot={rr.prune_overshoot} unreachable={rr.prune_unreachable} skipped={rr.skipped_children}")
print("\n== Scale numbers (scenario Q4) ==")
n, T = 40, 10**9
print("DP cells n*T =", n * T, " (n+1)*(T+1) =", (n + 1) * (T + 1))
print("bytes (1 byte/cell) =", (n + 1) * (T + 1) / 1e9, "GB;  bits =", (n + 1) * (T + 1) / 8 / 1e9, "GB; one row bitset =", T / 8 / 1e6, "MB")
print("2^40 =", 2**40, " 2^20 =", 2**20, " ratio 2^40/(n*T) =", 2**40 / (n * T))
