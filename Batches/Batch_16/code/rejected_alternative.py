"""Batch 16 - rejected alternative: exhaustive interval enumeration.

This is the Backtracking-style baseline: it visits every one of the
n(n+1)/2 non-empty windows [i, j] and keeps the best.  A running sum makes
each candidate O(1), so the whole search is Theta(n^2) on every input.

Same conventions as main_solution.py: 0-based inclusive positions
internally, empty input raises ValueError, ties go to the earliest start
and then the earliest end (achieved here by visiting windows in
(start, end) order and replacing only on a strictly larger sum).
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence


def best_window_exhaustive(values: Sequence[int]) -> tuple[int, int, int]:
    """Return (max_sum, start, end) by checking every non-empty window."""
    n = len(values)
    if n == 0:
        raise ValueError("empty input: a non-empty trading window is required")
    best, best_start, best_end = values[0], 0, 0
    for i in range(n):
        running = 0
        for j in range(i, n):
            running += values[j]
            if running > best:
                best, best_start, best_end = running, i, j
    return best, best_start, best_end


def count_windows(n: int) -> int:
    """Number of non-empty contiguous windows: n(n+1)/2."""
    return n * (n + 1) // 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Best trading window by exhaustive enumeration (O(n^2)).")
    parser.add_argument("values", nargs="*", help="price changes")
    parser.add_argument("--file", help="read whitespace/comma separated values")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = " ".join(args.values)
    values = [int(t) for t in text.replace("[", " ").replace("]", " ")
              .replace(",", " ").split()]

    try:
        total, start, end = best_window_exhaustive(values)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"n = {len(values)}  (windows examined = {count_windows(len(values))})")
    print(f"best sum = {total}")
    print(f"window (1-based, inclusive) = [{start + 1}, {end + 1}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
