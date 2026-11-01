#!/usr/bin/env python3
"""test_all.py -- self-checks. Run:  python test_all.py   (prints PASS or fails loudly)"""
import random
from math import comb

from main_solution import solve, to_rupees, validate
from rejected_alternative import brute_force_solve
from analysis_tools import dp_count, meet_in_middle, greedy_largest_fit
from generate_inputs import hard_instance, random_instance

A = [15000, 22000, 35000, 40000, 48000, 53000, 61000]

# 1. The assignment instance
r = solve(A, 110000)
assert r.solutions == [(1, 2, 5), (1, 3, 4)], r.solutions
assert (r.states, r.prune_overshoot, r.prune_unreachable) == (35, 28, 7)
assert brute_force_solve(A, 110000) == ([(1, 2, 5), (1, 3, 4)], 128)
assert greedy_largest_fit(A, 110000) == ([6, 4], 1000)

# 2. Tolerance: exact integer arithmetic, 0.05 thousand = 50 rupees
assert to_rupees("0.05", 1000) == 50
assert solve(A, 110000, 50).solutions == r.solutions
B = [15020, 22000, 35000, 39990, 48000, 53030, 61000]      # not multiples of 1000
assert len(solve(B, 110000, 0).solutions) == 0
rt = solve(B, 110000, 50)
assert rt.solutions == brute_force_solve(B, 110000, 50)[0] and len(rt.solutions) >= 1

# 3. Duplicates are separate items, never reused
D = [5, 5, 5, 10]
assert solve(D, 10).solutions == [(0, 1), (0, 2), (1, 2), (3,)]
assert solve([7, 7], 14).solutions == [(0, 1)]
assert solve([7], 14).solutions == []

# 4. Randomised cross-check vs brute force, DP count and meet-in-the-middle
rng = random.Random(1)
for _ in range(400):
    n = rng.randint(1, 12)
    am = [rng.randint(1, 30) for _ in range(n)]
    tgt = rng.randint(1, 80)
    tol = rng.choice([0, 0, 0, 1, 3, 10])
    got = solve(am, tgt, tol)
    exp, tested = brute_force_solve(am, tgt, tol)
    assert got.solutions == exp, (am, tgt, tol)
    assert meet_in_middle(am, tgt, tol)[0] == exp
    if tol == 0:
        assert dp_count(am, tgt) == len(exp)
    assert got.states <= 2 ** n and tested == 2 ** n
    assert len(set(got.solutions)) == len(got.solutions)       # no duplicates

# 5. Hard family: no solution and EXACT state count C(n, n//2)
for n in range(4, 19):
    am, tgt, tol = hard_instance(n)
    res = solve(am, tgt, tol)
    assert res.solutions == [] and res.states == comb(n, n // 2), (n, res.states)

# 6. Input validation
for bad in ([[0, 5], 5, 0], [[-1, 5], 5, 0], [[], 5, 0], [[5], 0, 0], [[5], 5, -1]):
    try:
        validate(*bad); raise SystemExit("validation missed " + str(bad))
    except ValueError:
        pass
try:
    to_rupees("0.0005", 1000); raise SystemExit("fraction of rupee accepted")
except ValueError:
    pass
print("ALL TESTS PASS")
