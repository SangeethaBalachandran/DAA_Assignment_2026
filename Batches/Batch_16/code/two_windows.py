"""Batch 16 - changed requirement: AT MOST TWO non-overlapping windows.

P[i] = best non-empty window entirely inside A[0..i]   (forward scan)
Q[i] = best non-empty window entirely inside A[i..n-1] (backward scan)

answer = max( max_i P[i],                      # one window
              max_{i < n-1} P[i] + Q[i+1] )    # two windows split at i | i+1

O(n) time, O(n) extra space for the stored P and Q arrays.
Positions are 0-based inclusive; empty input raises ValueError.
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

Window = tuple[int, int]


def best_two_windows(values: Sequence[int]) -> tuple[int, list[Window]]:
    """Return (max_total, windows) using one or two disjoint windows."""
    n = len(values)
    if n == 0:
        raise ValueError("empty input: at least one non-empty window is required")

    # forward: P[i] and the window achieving it
    P: list[int] = [0] * n
    P_win: list[Window] = [(0, 0)] * n
    end_here, start_here = values[0], 0          # best window ending at i
    P[0], P_win[0] = values[0], (0, 0)
    for i in range(1, n):
        if end_here >= 0:
            end_here += values[i]
        else:
            end_here, start_here = values[i], i
        if end_here > P[i - 1]:
            P[i], P_win[i] = end_here, (start_here, i)
        else:
            P[i], P_win[i] = P[i - 1], P_win[i - 1]

    # backward: Q[i] and the window achieving it
    Q: list[int] = [0] * n
    Q_win: list[Window] = [(0, 0)] * n
    start_here_val, end_at = values[n - 1], n - 1  # best window starting at i
    Q[n - 1], Q_win[n - 1] = values[n - 1], (n - 1, n - 1)
    for i in range(n - 2, -1, -1):
        if start_here_val >= 0:
            start_here_val += values[i]
        else:
            start_here_val, end_at = values[i], i
        if start_here_val >= Q[i + 1]:
            Q[i], Q_win[i] = start_here_val, (i, end_at)
        else:
            Q[i], Q_win[i] = Q[i + 1], Q_win[i + 1]

    best, windows = P[n - 1], [P_win[n - 1]]
    for i in range(n - 1):
        if P[i] + Q[i + 1] > best:
            best, windows = P[i] + Q[i + 1], [P_win[i], Q_win[i + 1]]
    return best, windows


def best_k_windows(values: Sequence[int], k: int) -> int:
    """Generalisation: at most k disjoint non-empty windows, O(kn) time.

    open_[j]   = best total using j windows with the j-th still open at i
    closed[j]  = best total using exactly j windows, all closed by i
    Only the sum is returned; it is used to cross-check best_two_windows.
    """
    if not values:
        raise ValueError("empty input")
    if k < 1:
        raise ValueError("k must be >= 1")
    neg = float("-inf")
    open_ = [neg] * (k + 1)
    closed = [neg] * (k + 1)
    closed[0] = 0
    for x in values:
        for j in range(k, 0, -1):
            open_[j] = max(open_[j], closed[j - 1]) + x
            closed[j] = max(closed[j], open_[j])
    return int(max(closed[1:]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="At most two non-overlapping best windows (prefix/suffix DP).")
    parser.add_argument("values", nargs="*", help="price changes")
    args = parser.parse_args(argv)
    values = [int(t) for t in " ".join(args.values).replace("[", " ")
              .replace("]", " ").replace(",", " ").split()]
    try:
        total, windows = best_two_windows(values)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    shown = ", ".join(f"[{a + 1}, {b + 1}]" for a, b in windows)
    print(f"best total with at most two windows = {total}")
    print(f"windows (1-based, inclusive) = {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
