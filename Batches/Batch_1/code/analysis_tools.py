#!/usr/bin/env python3
"""
analysis_tools.py -- helper algorithms used ONLY for the report's analysis and
for independent cross-checking (not part of the submitted solution path):
  * greedy_largest_fit : the proposed greedy strategy (scenario Q3)
  * dp_count           : counts subsets reaching each sum (DP over sums)
  * dp_enumerate       : enumerates all solutions from a full DP table
  * meet_in_middle     : divide-and-conquer style enumeration (2^(n/2) halves)
All work on integer rupees.
"""
from bisect import bisect_left, bisect_right
from itertools import combinations


def greedy_largest_fit(amounts, target):
    """Repeatedly take the largest remaining amount that still fits."""
    remaining, picked = target, []
    for i in sorted(range(len(amounts)), key=lambda i: -amounts[i]):
        if amounts[i] <= remaining:
            picked.append(i)
            remaining -= amounts[i]
    return picked, remaining          # remaining == 0 means greedy "found" a subset


def dp_count(amounts, target):
    """number of subsets (by index) with each sum 0..target; O(n*target) time."""
    ways = [0] * (target + 1)
    ways[0] = 1
    for a in amounts:
        for s in range(target, a - 1, -1):
            ways[s] += ways[s - a]
    return ways[target]


def dp_enumerate(amounts, target):
    """Full (n+1) x (target+1) reachability table, then walk back to list ALL subsets."""
    n = len(amounts)
    reach = [[False] * (target + 1) for _ in range(n + 1)]
    reach[0][0] = True
    for i in range(1, n + 1):
        a = amounts[i - 1]
        for s in range(target + 1):
            reach[i][s] = reach[i - 1][s] or (s >= a and reach[i - 1][s - a])
    out = []

    def walk(i, s, chosen):
        if s == 0:
            out.append(tuple(sorted(chosen)))   # remaining items all excluded
            return
        if i == 0:
            return
        if reach[i - 1][s]:
            walk(i - 1, s, chosen)
        a = amounts[i - 1]
        if s >= a and reach[i - 1][s - a]:
            walk(i - 1, s - a, chosen + [i - 1])
    walk(n, target, [])
    return sorted(set(out)), (n + 1) * (target + 1)


def meet_in_middle(amounts, target, tolerance=0):
    """Split items in two halves, list all subset sums of each, match with binary search."""
    n = len(amounts)
    half = n // 2
    L, R = list(range(half)), list(range(half, n))

    def subsets(idx):
        res = []
        for k in range(len(idx) + 1):
            for c in combinations(idx, k):
                res.append((sum(amounts[i] for i in c), c))
        res.sort()
        return res
    left, right = subsets(L), subsets(R)
    rsums = [s for s, _ in right]
    lo, hi = target - tolerance, target + tolerance
    out = []
    for s, c in left:
        a, b = bisect_left(rsums, lo - s), bisect_right(rsums, hi - s)
        for k in range(a, b):
            full = tuple(sorted(c + right[k][1]))
            if full:
                out.append(full)
    return sorted(out), len(left) + len(right)


if __name__ == "__main__":
    A = [15000, 22000, 35000, 40000, 48000, 53000, 61000]
    print("greedy:", greedy_largest_fit(A, 110000))
    print("dp_count:", dp_count([a // 1000 for a in A], 110))
    print("dp_enumerate:", dp_enumerate([a // 1000 for a in A], 110))
    print("meet_in_middle:", meet_in_middle(A, 110000))
