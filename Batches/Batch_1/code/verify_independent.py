#!/usr/bin/env python3
"""
verify_independent.py -- independent verification (Member 2's checks).

Written from the report's DESCRIPTIONS only; it deliberately uses different
methods from main_solution.py:
  * its own brute force: bitmask loop with an incremental subset-sum table
    (the shared rejected_alternative.py uses itertools.combinations)
  * its own generator for the hard family (README section 9)
Checks:
  1. assignment instance  -> exactly {22,35,53} and {22,40,48}
  2. 200 random small inputs (with duplicate amounts, tolerance 0/1/5) -> solution
     lists identical for: own brute force, shared brute force, main solver
  3. hard family: states == C(n, n//2) for n = 8, 12, 16, 20 and no solution
  4. an extra hard input of our own: equal amounts, target = half the total
  5. changed requirement examples from README section 11
  6. mutation test: break the overshoot rule (>  ->  >=) and confirm that the
     checker DETECTS the bug (so the checker is actually able to fail)
Run:  python verify_independent.py      (prints a summary, exit code 0 = all passed)
"""
import random
import re
from math import comb

import main_solution
from main_solution import solve
from rejected_alternative import brute_force_solve


# ---------------------------------------------------------------- own brute force
def my_brute(amounts, target, tol=0):
    """All non-empty index subsets with target-tol <= sum <= target+tol (bitmask method)."""
    n = len(amounts)
    lo, hi = target - tol, target + tol
    sums = [0] * (1 << n)                      # sums[m] = sum of items whose bit is set in m
    found = []
    for m in range(1, 1 << n):
        low = m & -m
        sums[m] = sums[m ^ low] + amounts[low.bit_length() - 1]
        if lo <= sums[m] <= hi:
            found.append(tuple(i for i in range(n) if m >> i & 1))
    return sorted(found)


# ---------------------------------------------------------------- own hard family
def my_hard(n):
    M = 10 * n * n
    return [M + i for i in range(1, n + 1)], (n // 2 + 1) * M - 1


def check(cond, msg):
    if not cond:
        raise SystemExit("FAILED: " + msg)


def main():
    # 1. assignment instance
    A = [15000, 22000, 35000, 40000, 48000, 53000, 61000]
    sol = my_brute(A, 110000)
    check([[A[i] // 1000 for i in s] for s in sol] == [[22, 35, 53], [22, 40, 48]], "instance solutions")
    check(solve(A, 110000).solutions == sol, "main solver vs own brute force on instance")
    print("1. instance: own brute force finds", [[A[i] // 1000 for i in s] for s in sol], "(2^7 = 128 subsets)")

    # 2. random cross-check
    rng = random.Random(4242)
    for case in range(200):
        n = rng.randint(1, 12)
        am = [rng.randint(1, 12) for _ in range(n)]          # small range -> many duplicates
        tgt = rng.randint(1, 40)
        tol = rng.choice([0, 1, 5])
        a, b, c = my_brute(am, tgt, tol), brute_force_solve(am, tgt, tol)[0], solve(am, tgt, tol).solutions
        check(a == b == c, f"random case {case}: {am} {tgt} {tol}")
    print("2. 200 random cases (duplicates, tolerance 0/1/5): own brute == shared brute == main solver")

    # 3. hard family
    for n in (8, 12, 16, 20):
        am, tgt = my_hard(n)
        r = solve(am, tgt, 0)
        check(r.solutions == [] and r.states == comb(n, n // 2), f"hard family n={n}")
        print(f"3. hard n={n:>2}: states={r.states:>7} = C({n},{n // 2}) = {comb(n, n // 2):>7}; 2^n={2 ** n}; no solution")
    am, tgt = my_hard(12)
    check(my_brute(am, tgt) == [], "own brute force also finds no solution for hard n=12")

    # 4. an extra difficult input of our own: all amounts equal, target = half of the total
    for n in (12, 16, 20):
        r = solve([1000] * n, 1000 * (n // 2), 0)
        check(len(r.solutions) == comb(n, n // 2), "equal amounts solutions")
        print(f"4. equal amounts n={n}: solutions={len(r.solutions)} = C({n},{n // 2}); states={r.states}; 2^n={2 ** n}"
              f"  (output-bound: every algorithm must produce {len(r.solutions)} subsets)")

    # 5. changed requirement
    check(solve(A, 110000, 50).solutions == sol and solve(A, 110000, 50).states == 35, "tolerance on instance")
    B = [15020, 22000, 35000, 39990, 48000, 53030, 61000]
    check(my_brute(B, 110000, 0) == [], "B, tol 0")
    got = my_brute(B, 110000, 50)
    check([sum(B[i] for i in s) for s in got] == [110030, 109990] or
          sorted(sum(B[i] for i in s) for s in got) == [109990, 110030], "B, tol 50 sums")
    check(solve(B, 110000, 50).solutions == got, "B, tol 50 main solver")
    print("5. tolerance: instance unchanged (2 solutions, 35 states); hypothetical amounts: 0 solutions at tol 0, sums",
          sorted(sum(B[i] for i in s) for s in got), "at tol 50")

    # 6. mutation test: overshoot rule  '>'  ->  '>='  must be detected
    src = open(main_solution.__file__).read()
    check("if current + vals[j] > hi:" in src, "overshoot line not found for mutation")
    ns = {"__name__": "mutant"}
    exec(compile(src.replace("if current + vals[j] > hi:", "if current + vals[j] >= hi:"), "mutant", "exec"), ns)
    bad = ns["solve"](A, 110000).solutions
    check(bad != sol, "mutation NOT detected (checker too weak)")
    print("6. mutation test: with '>=' in the overshoot rule the solver returns", bad, "-> bug detected, as it should be")

    print("\nALL INDEPENDENT CHECKS PASSED")


if __name__ == "__main__":
    main()
