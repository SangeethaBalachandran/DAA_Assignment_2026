#!/usr/bin/env python3
"""
rejected_alternative.py -- brute-force enumeration of ALL 2^n subsets.

This is the rejected alternative used for the timing/correctness comparison.
It has no pruning: every subset is generated and its sum is tested.
Same input convention as main_solution.py (integer rupees internally).
"""
import argparse
import sys
from fractions import Fraction
from itertools import combinations


def to_rupees(value, scale):
    exact = Fraction(str(value).strip()) * scale
    if exact.denominator != 1:
        raise ValueError(f"'{value}' x {scale} is not a whole number of rupees")
    return int(exact)


def brute_force_solve(amounts, target, tolerance=0):
    """Return (solutions, subsets_tested).

    solutions: sorted list of tuples of ORIGINAL indices whose sum s satisfies
    target - tolerance <= s <= target + tolerance.  The empty subset is tested
    (it is one of the 2^n subsets) but is never reported.
    """
    if not amounts or any((not isinstance(a, int)) or a <= 0 for a in amounts):
        raise ValueError("amounts must be a non-empty list of positive integers")
    lo, hi = target - tolerance, target + tolerance
    n = len(amounts)
    solutions = []
    tested = 1                              # the empty subset
    for size in range(1, n + 1):
        for idx in combinations(range(n), size):   # idx is already increasing
            tested += 1
            s = sum(amounts[i] for i in idx)
            if lo <= s <= hi:
                solutions.append(idx)
    solutions.sort()
    return solutions, tested


def main(argv=None):
    p = argparse.ArgumentParser(description="Brute-force subset enumeration (rejected alternative).")
    p.add_argument("--amounts", nargs="+", default=["15", "22", "35", "40", "48", "53", "61"])
    p.add_argument("--target", default="110")
    p.add_argument("--scale", type=int, default=1000)
    p.add_argument("--tolerance", default="0", help="in rupees")
    a = p.parse_args(argv)
    try:
        amounts = [to_rupees(x, a.scale) for x in a.amounts]
        target, tol = to_rupees(a.target, a.scale), to_rupees(a.tolerance, 1)
        sols, tested = brute_force_solve(amounts, target, tol)
    except ValueError as e:
        print("Input error:", e, file=sys.stderr)
        return 2
    print(f"Subsets tested: {tested} (2^{len(amounts)} = {2 ** len(amounts)})")
    print(f"Solutions found: {len(sols)}")
    for s in sols:
        print(f"  indices {[i + 1 for i in s]} amounts {[amounts[i] for i in s]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
