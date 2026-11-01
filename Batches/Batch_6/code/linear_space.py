#!/usr/bin/env python3
"""Linear-memory recovery of the optimal alignment (Question 4).

Idea: keep only one DP row at a time.  To recover the path, split the reference at its
middle row, find where the optimal path crosses that row (forward scores + backward
scores), then recurse on the two halves.  Space O(n), time <= 2*m*n.

Usage: python3 linear_space.py REFERENCE READ
"""
import sys
from main_solution import fill_table, traceback, ops_cost, format_alignment


def last_row(a, b):
    """Costs of aligning all of a with every prefix of b, using two rows only."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            v = prev[j - 1] + (0 if ca == cb else 1)
            up = prev[j] + 1
            if up < v:
                v = up
            left = cur[j - 1] + 1
            if left < v:
                v = left
            cur[j] = v
        prev = cur
    return prev


def hirschberg(a, b):
    if len(a) == 0:
        return [("I", "-", c) for c in b]
    if len(b) == 0:
        return [("D", c, "-") for c in a]
    if len(a) == 1:                      # base case: one row, small table
        return traceback(fill_table(a, b), a, b)
    mid = len(a) // 2
    left = last_row(a[:mid], b)
    right = last_row(a[mid:][::-1], b[::-1])
    n = len(b)
    k = min(range(n + 1), key=lambda j: left[j] + right[n - j])
    return hirschberg(a[:mid], b[:k]) + hirschberg(a[mid:], b[k:])


if __name__ == "__main__":
    ref = sys.argv[1] if len(sys.argv) > 2 else "GATTACA"
    read = sys.argv[2] if len(sys.argv) > 2 else "GCATGCA"
    ops = hirschberg(ref, read)
    print("Cost:", ops_cost(ops))
    print(format_alignment(ops))
