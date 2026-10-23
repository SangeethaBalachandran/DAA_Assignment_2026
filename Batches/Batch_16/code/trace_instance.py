"""Batch 16 - print the full merge trace of the given instance (Markdown).

The hierarchy is the coordinator's bottom-up pairwise reduction
(leaves -> pairs -> blocks of four -> [1..8] with [9..12] carried -> root),
produced by main_solution.reduce_summaries.  All positions are 1-based.

Run:  python code/trace_instance.py > trace.md
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_inputs import GIVEN_INSTANCE           # noqa: E402
from main_solution import leaf, reduce_summaries     # noqa: E402


def v(x):
    return f"({x})" if x < 0 else str(x)


def fmt(s):
    return f"({s.total}, {s.prefix}, {s.suffix}, {s.best})"


def main():
    values = GIVEN_INSTANCE
    leaves = [leaf(x, i) for i, x in enumerate(values)]
    spans = {id(s): (i + 1, i + 1) for i, s in enumerate(leaves)}
    log: list = []
    root = reduce_summaries(leaves, log)

    print("**Level 0 - leaves** (each S(x) = (x, x, x, x))\n")
    print("| Pos | x | (total, prefix, suffix, best) | best window |")
    print("|---|---|---|---|")
    for i, s in enumerate(leaves):
        print(f"| {i + 1} | {values[i]} | {fmt(s)} | [{i + 1}, {i + 1}] |")

    names = {1: "adjacent pairs", 2: "blocks of four",
             3: "block of eight ([9, 12] carried forward unchanged)", 4: "root"}
    for level, merges in enumerate(log, start=1):
        print(f"\n**Level {level} - {names.get(level, '')}**\n")
        print("| Segment | L summary | R summary | total = L.t + R.t "
              "| prefix = max(L.p, L.t + R.p) | suffix = max(R.s, R.t + L.s) "
              "| best = max(L.b, R.b, L.s + R.p) | Result (t, p, s, b) "
              "| prefix ends | suffix starts | best window |")
        print("|---|---|---|---|---|---|---|---|---|---|---|")
        for L, R, M in merges:
            lo, _ = spans[id(L)]
            _, hi = spans[id(R)]
            spans[id(M)] = (lo, hi)
            print(
                f"| [{lo}, {hi}] | {fmt(L)} | {fmt(R)} "
                f"| {v(L.total)} + {v(R.total)} = **{M.total}** "
                f"| max({L.prefix}, {v(L.total)} + {v(R.prefix)} = {L.total + R.prefix}) = **{M.prefix}** "
                f"| max({R.suffix}, {v(R.total)} + {v(L.suffix)} = {R.total + L.suffix}) = **{M.suffix}** "
                f"| max({L.best}, {R.best}, {v(L.suffix)} + {v(R.prefix)} = {L.suffix + R.prefix}) = **{M.best}** "
                f"| {fmt(M)} | {M.prefix_end + 1} | {M.suffix_start + 1} "
                f"| [{M.best_start + 1}, {M.best_end + 1}] |")
    print(f"\nRoot: {fmt(root)}, best window = "
          f"[{root.best_start + 1}, {root.best_end + 1}], "
          f"values {values[root.best_start:root.best_end + 1]}, "
          f"sum = {sum(values[root.best_start:root.best_end + 1])}")


if __name__ == "__main__":
    main()
