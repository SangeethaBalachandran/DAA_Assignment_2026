"""Batch 16 - Best trading window (maximum-sum contiguous subarray).

Chosen technique: Divide and Conquer over a composable segment summary.

Every non-empty segment is described by the four aggregates

    S = (total, prefix, suffix, best)

plus constant-size positional metadata (prefix_end, suffix_start,
best_start, best_end) that lets us reconstruct the winning windows.

Conventions
-----------
* Internally positions are 0-based, inclusive on both ends.  The report and
  the command-line output use 1-based positions (internal index + 1).
* A window must be non-empty.  Empty input raises ``ValueError``.
* Tie-breaking (identical everywhere in this project): maximise the sum,
  then prefer the earliest start, then the earliest end.
"""

from __future__ import annotations

import argparse
import sys
from typing import NamedTuple, Sequence


class Summary(NamedTuple):
    """Summary of a non-empty segment A[lo..hi] (0-based, inclusive)."""

    total: int
    prefix: int
    suffix: int
    best: int
    # positional metadata (kept apart from the four aggregates)
    prefix_end: int     # prefix window is [lo, prefix_end]
    suffix_start: int   # suffix window is [suffix_start, hi]
    best_start: int     # best window is [best_start, best_end]
    best_end: int


def leaf(x: int, i: int) -> Summary:
    """S(x) = (x, x, x, x) for the single value x at position i."""
    return Summary(x, x, x, x, i, i, i, i)


def merge(left: Summary, right: Summary) -> Summary:
    """Combine summaries of two ADJACENT segments, ``left`` before ``right``.

    total  = L.total + R.total
    prefix = max(L.prefix, L.total + R.prefix)
    suffix = max(R.suffix, R.total + L.suffix)
    best   = max(L.best, R.best, L.suffix + R.prefix)

    Ties are resolved by the project policy (earliest start, then earliest
    end), which is why the comparisons below use >= in a specific order.
    """
    total = left.total + right.total

    # prefix: both candidates start at the segment start; prefer earlier end.
    extended_prefix = left.total + right.prefix
    if left.prefix >= extended_prefix:
        prefix, prefix_end = left.prefix, left.prefix_end
    else:
        prefix, prefix_end = extended_prefix, right.prefix_end

    # suffix: both candidates end at the segment end; prefer earlier start.
    extended_suffix = left.suffix + right.total
    if extended_suffix >= right.suffix:
        suffix, suffix_start = extended_suffix, left.suffix_start
    else:
        suffix, suffix_start = right.suffix, right.suffix_start

    # best: entirely left, crossing the boundary, or entirely right.
    candidates = (
        (left.best, left.best_start, left.best_end),
        (left.suffix + right.prefix, left.suffix_start, right.prefix_end),
        (right.best, right.best_start, right.best_end),
    )
    best, best_start, best_end = max(candidates, key=_window_key)

    return Summary(total, prefix, suffix, best,
                   prefix_end, suffix_start, best_start, best_end)


def _window_key(window: tuple[int, int, int]) -> tuple[int, int, int]:
    total, start, end = window
    return (total, -start, -end)


def summarize(values: Sequence[int], lo: int, hi: int) -> Summary:
    """Balanced recursive Divide and Conquer over values[lo..hi] (inclusive).

    The array is split by index; no slices are copied.  The recursion depth
    is ceil(log2 n) + 1, so the stack holds O(log n) frames at any time.
    """
    if lo == hi:
        return leaf(values[lo], lo)
    mid = (lo + hi) // 2
    return merge(summarize(values, lo, mid), summarize(values, mid + 1, hi))


def best_window(values: Sequence[int]) -> tuple[int, int, int]:
    """Return (max_sum, start, end) with 0-based inclusive positions."""
    if len(values) == 0:
        raise ValueError("empty input: a non-empty trading window is required")
    s = summarize(values, 0, len(values) - 1)
    return s.best, s.best_start, s.best_end


def reduce_summaries(summaries: Sequence[Summary],
                     log: list | None = None) -> Summary:
    """Coordinator: combine ordered block summaries with a balanced tree.

    Each round merges neighbours (0,1), (2,3), ...; an odd block at the end is
    carried forward unchanged.  Because ``merge`` is associative, the result
    equals the summary of the concatenated blocks.  If ``log`` is given, one
    list of (left, right, merged) triples is appended per round.
    """
    if not summaries:
        raise ValueError("no summaries to reduce")
    level = list(summaries)
    while len(level) > 1:
        nxt, merges = [], []
        for k in range(0, len(level) - 1, 2):
            merged = merge(level[k], level[k + 1])
            merges.append((level[k], level[k + 1], merged))
            nxt.append(merged)
        if len(level) % 2:
            nxt.append(level[-1])
        if log is not None:
            log.append(merges)
        level = nxt
    return level[0]


def partition_bounds(n: int, p: int) -> list[tuple[int, int]]:
    """Split [0, n) into p contiguous, near-equal blocks (inclusive bounds)."""
    p = max(1, min(p, n))
    base, extra = divmod(n, p)
    bounds, lo = [], 0
    for k in range(p):
        size = base + (1 if k < extra else 0)
        bounds.append((lo, lo + size - 1))
        lo += size
    return bounds


def distributed_best_window(values: Sequence[int], servers: int = 8,
                            log: list | None = None) -> tuple[int, int, int]:
    """Simulate the eight-server design on one machine.

    Each "server" summarises its own contiguous block (O(n/p) work) and ships
    only its constant-size Summary; the coordinator performs p-1 merges in
    ceil(log2 p) rounds.  This is a model of the computation, not a
    measurement of a real cluster.
    """
    if len(values) == 0:
        raise ValueError("empty input: a non-empty trading window is required")
    local = [summarize(values, lo, hi)
             for lo, hi in partition_bounds(len(values), servers)]
    root = reduce_summaries(local, log)
    return root.best, root.best_start, root.best_end


def _parse_values(text: str) -> list[int]:
    cleaned = text.replace("[", " ").replace("]", " ").replace(",", " ")
    return [int(tok) for tok in cleaned.split()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Best trading window via Divide and Conquer summaries.")
    parser.add_argument("values", nargs="*",
                        help="price changes, e.g. 3 -5 8 or \"[3,-5,8]\"")
    parser.add_argument("--file", help="read whitespace/comma separated values")
    parser.add_argument("--servers", type=int, default=0,
                        help="also run the p-server simulation (e.g. 8)")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            values = _parse_values(fh.read())
    else:
        values = _parse_values(" ".join(args.values))

    try:
        total, start, end = best_window(values)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"n = {len(values)}")
    print(f"best sum = {total}")
    print(f"window (1-based, inclusive) = [{start + 1}, {end + 1}]")
    if len(values) <= 40:
        print(f"window values = {list(values[start:end + 1])}")
    if args.servers:
        d_total, d_start, d_end = distributed_best_window(values, args.servers)
        print(f"{args.servers}-server simulation: sum = {d_total}, "
              f"window = [{d_start + 1}, {d_end + 1}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
