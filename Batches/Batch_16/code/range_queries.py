"""Batch 16 - repeated "best window between day L and day R" queries.

Three structures that answer the same query (0-based inclusive L..R, same
tie-breaking as main_solution.py):

* kadane_range        - direct scan, no preprocessing, O(R-L+1) per query
* SegmentTree         - O(n) build, O(log n) query, O(log n) point update
* DisjointSparseTable - O(n log n) build, O(1) merges per query, static data

The tree and the table reuse the associative but NON-idempotent summary
merge, so every query combines pieces strictly in left-to-right order.
"""

from __future__ import annotations

from typing import Sequence

from main_solution import Summary, leaf, merge


def kadane_range(values: Sequence[int], lo: int = 0,
                 hi: int | None = None) -> tuple[int, int, int]:
    """Kadane's single left-to-right scan over values[lo..hi].

    O(hi-lo+1) time, O(1) extra space.  Extending when the running sum is
    >= 0 (not > 0) keeps the earliest start on ties.
    """
    if hi is None:
        hi = len(values) - 1
    if lo > hi:
        raise ValueError("empty range")
    cur, cur_start = values[lo], lo
    best, best_start, best_end = cur, lo, lo
    for j in range(lo + 1, hi + 1):
        x = values[j]
        if cur >= 0:
            cur += x
        else:
            cur, cur_start = x, j
        if cur > best:
            best, best_start, best_end = cur, cur_start, j
    return best, best_start, best_end


class SegmentTree:
    """Segment tree whose nodes store the segment Summary."""

    def __init__(self, values: Sequence[int]):
        if len(values) == 0:
            raise ValueError("empty input")
        self.n = len(values)
        self.tree: list[Summary | None] = [None] * (4 * self.n)
        self._build(values, 1, 0, self.n - 1)

    def _build(self, values, node, lo, hi):
        if lo == hi:
            self.tree[node] = leaf(values[lo], lo)
            return
        mid = (lo + hi) // 2
        self._build(values, 2 * node, lo, mid)
        self._build(values, 2 * node + 1, mid + 1, hi)
        self.tree[node] = merge(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, index: int, value: int) -> None:
        """Point update A[index] = value in O(log n)."""
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, node, lo, hi, index, value):
        if lo == hi:
            self.tree[node] = leaf(value, lo)
            return
        mid = (lo + hi) // 2
        if index <= mid:
            self._update(2 * node, lo, mid, index, value)
        else:
            self._update(2 * node + 1, mid + 1, hi, index, value)
        self.tree[node] = merge(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, left: int, right: int) -> tuple[int, int, int]:
        """Best window inside [left, right]; O(log n) node visits."""
        if not 0 <= left <= right < self.n:
            raise IndexError("invalid range")
        s = self._query(1, 0, self.n - 1, left, right)
        return s.best, s.best_start, s.best_end

    def _query(self, node, lo, hi, left, right) -> Summary:
        if left <= lo and hi <= right:
            return self.tree[node]
        mid = (lo + hi) // 2
        if right <= mid:
            return self._query(2 * node, lo, mid, left, right)
        if left > mid:
            return self._query(2 * node + 1, mid + 1, hi, left, right)
        # left part strictly before right part: order matters
        return merge(self._query(2 * node, lo, mid, left, right),
                     self._query(2 * node + 1, mid + 1, hi, left, right))


class DisjointSparseTable:
    """Disjoint sparse table over Summary (static data only).

    For every level h and every block of size 2^(h+1) with midpoint m, it
    stores summaries of A[i..m-1] (left half) and A[m..j] (right half).  A
    query [l, r] with l != r uses the level of the highest differing bit of
    l and r, and answers with ONE ordered merge of two disjoint pieces.  The
    classic overlapping sparse table (used for min/max) would count the
    overlap twice, which is wrong here because merge is not idempotent.
    """

    def __init__(self, values: Sequence[int]):
        if len(values) == 0:
            raise ValueError("empty input")
        self.n = len(values)
        self.values = list(values)
        levels = max(1, (self.n - 1).bit_length())
        size = 1 << levels
        self.table: list[list[Summary | None]] = []
        for h in range(levels):
            half = 1 << h
            row: list[Summary | None] = [None] * size
            for mid in range(half, size, 2 * half):
                if mid - 1 < self.n:   # left half: suffixes ending at mid-1
                    acc = leaf(self.values[mid - 1], mid - 1)
                    row[mid - 1] = acc
                    for i in range(mid - 2, mid - half - 1, -1):
                        acc = merge(leaf(self.values[i], i), acc)
                        row[i] = acc
                if mid < self.n:       # right half: prefixes starting at mid
                    acc = leaf(self.values[mid], mid)
                    row[mid] = acc
                    for j in range(mid + 1, min(mid + half, self.n)):
                        acc = merge(acc, leaf(self.values[j], j))
                        row[j] = acc
            self.table.append(row)

    def query(self, left: int, right: int) -> tuple[int, int, int]:
        if not 0 <= left <= right < self.n:
            raise IndexError("invalid range")
        if left == right:
            s = leaf(self.values[left], left)
        else:
            h = (left ^ right).bit_length() - 1
            s = merge(self.table[h][left], self.table[h][right])
        return s.best, s.best_start, s.best_end
