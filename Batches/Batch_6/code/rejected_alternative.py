#!/usr/bin/env python3
"""Rejected alternatives, kept for comparison.

1. recursive_cost : the straightforward recursion (backtracking over the last column).
                    Exponential: counts every call.
2. greedy_cost    : the "fast aligner": left to right, match if equal else substitute.
3. bnb_cost       : depth-first branch and bound with the bound g + |remaining length gap|.

Usage: python3 rejected_alternative.py
"""
import sys

sys.setrecursionlimit(10000)


def recursive_cost(ref, read):
    """Returns (cost, number_of_calls). No memoisation."""
    calls = [0]

    def f(i, j):
        calls[0] += 1
        if i == 0:
            return j
        if j == 0:
            return i
        diag = f(i - 1, j - 1) + (0 if ref[i - 1] == read[j - 1] else 1)
        up = f(i - 1, j) + 1
        left = f(i, j - 1) + 1
        return min(diag, up, left)

    c = f(len(ref), len(read))
    return c, calls[0]


def call_counts_per_cell(ref, read):
    """How many times the recursion visits each (i,j)."""
    m, n = len(ref), len(read)
    cnt = [[0] * (n + 1) for _ in range(m + 1)]

    def f(i, j):
        cnt[i][j] += 1
        if i == 0 or j == 0:
            return
        f(i - 1, j - 1)
        f(i - 1, j)
        f(i, j - 1)

    f(m, n)
    return cnt


def call_count_formula(m, n):
    """T(i,j) = 1 + T(i-1,j-1) + T(i-1,j) + T(i,j-1); T(0,*) = T(*,0) = 1."""
    T = [[1] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            T[i][j] = 1 + T[i - 1][j - 1] + T[i - 1][j] + T[i][j - 1]
    return T[m][n]


def greedy_cost(ref, read):
    """Left-to-right: match if equal else substitute; leftover bases are indels."""
    k = min(len(ref), len(read))
    ops = []
    for t in range(k):
        ops.append("M" if ref[t] == read[t] else "S")
    ops += ["D"] * (len(ref) - k) + ["I"] * (len(read) - k)
    return sum(o != "M" for o in ops), "".join(ops)


def bnb_cost(ref, read):
    """DFS branch and bound. Returns (cost, nodes_expanded)."""
    m, n = len(ref), len(read)
    best = [greedy_cost(ref, read)[0]]  # incumbent: a valid alignment
    nodes = [0]

    def go(i, j, g):
        nodes[0] += 1
        if i == m and j == n:
            if g < best[0]:
                best[0] = g
            return
        if g + abs((m - i) - (n - j)) >= best[0] and not (i == m and j == n):
            # cannot beat the incumbent (ties pruned: we already hold a solution of this cost)
            return
        if i < m and j < n:
            go(i + 1, j + 1, g + (0 if ref[i] == read[j] else 1))
        if i < m:
            go(i + 1, j, g + 1)
        if j < n:
            go(i, j + 1, g + 1)

    go(0, 0, 0)
    return best[0], nodes[0]


if __name__ == "__main__":
    for R, Q in [("GATTACA", "GCATGCA"), ("ACGT", "CGT")]:
        print("Reference=%s Read=%s" % (R, Q))
        print("  greedy :", greedy_cost(R, Q))
        print("  recursion (cost, calls):", recursive_cost(R, Q))
        print("  branch&bound (cost, nodes):", bnb_cost(R, Q))
    print("Calls for two strings of length 4:", recursive_cost("ACGT", "TGCA")[1])
    print("Calls per cell (ref=ACGT, read=TGCA):")
    for row in call_counts_per_cell("ACGT", "TGCA"):
        print("  ", row)
