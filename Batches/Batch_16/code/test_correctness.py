"""Batch 16 - correctness tests (standard-library unittest).

Run:  python code/test_correctness.py      (from the Batch_16 folder)
"""

from __future__ import annotations

import itertools
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_inputs import GIVEN_INSTANCE, generate          # noqa: E402
from main_solution import (best_window, distributed_best_window,  # noqa: E402
                           leaf, merge, partition_bounds, reduce_summaries,
                           summarize, main as cli_main)
from range_queries import (DisjointSparseTable, SegmentTree,  # noqa: E402
                           kadane_range)
from rejected_alternative import best_window_exhaustive       # noqa: E402
from two_windows import best_k_windows, best_two_windows       # noqa: E402

RNG_SEED = 16


def direct_summary(values, lo, hi):
    """Summary fields computed straight from the definitions (brute force)."""
    seg = values[lo:hi + 1]
    total = sum(seg)
    prefixes = [(sum(seg[:k + 1]), lo + k) for k in range(len(seg))]
    prefix = max(p for p, _ in prefixes)
    prefix_end = min(e for p, e in prefixes if p == prefix)
    suffixes = [(sum(seg[k:]), lo + k) for k in range(len(seg))]
    suffix = max(s for s, _ in suffixes)
    suffix_start = min(s0 for s, s0 in suffixes if s == suffix)
    best = best_window_exhaustive(seg)
    return (total, prefix, suffix, best[0], prefix_end, suffix_start,
            best[1] + lo, best[2] + lo)


def brute_two(values):
    """Best total over every one window or every pair of disjoint windows."""
    n = len(values)
    windows = [(i, j, sum(values[i:j + 1]))
               for i in range(n) for j in range(i, n)]
    best = max(w[2] for w in windows)
    for (a, b, s1), (c, d, s2) in itertools.product(windows, repeat=2):
        if b < c:
            best = max(best, s1 + s2)
    return best


class GivenInstance(unittest.TestCase):
    def test_given_answer_is_14_on_positions_3_to_8(self):
        total, start, end = best_window(GIVEN_INSTANCE)
        self.assertEqual(total, 14)
        self.assertEqual((start + 1, end + 1), (3, 8))   # 1-based in report
        self.assertEqual(sum(GIVEN_INSTANCE[start:end + 1]), 14)

    def test_all_methods_agree_on_given(self):
        expected = (14, 2, 7)
        self.assertEqual(best_window_exhaustive(GIVEN_INSTANCE), expected)
        self.assertEqual(kadane_range(GIVEN_INSTANCE), expected)
        self.assertEqual(distributed_best_window(GIVEN_INSTANCE, 8), expected)
        log = []
        root = reduce_summaries([leaf(x, i) for i, x in enumerate(GIVEN_INSTANCE)], log)
        self.assertEqual((root.best, root.best_start, root.best_end), expected)
        self.assertEqual([len(r) for r in log], [6, 3, 1, 1])

    def test_root_summary_of_given(self):
        s = summarize(GIVEN_INSTANCE, 0, 11)
        self.assertEqual((s.total, s.prefix, s.suffix, s.best), (10, 12, 12, 14))

    def test_cli_runs(self):
        self.assertEqual(cli_main(["[3,-5,8,-2,6,-9,4,7,-3,-6,5,2]"]), 0)
        self.assertEqual(cli_main([]), 2)    # empty input policy


class EdgeCases(unittest.TestCase):
    def test_empty_input_raises(self):
        for fn in (best_window, best_window_exhaustive, best_two_windows):
            with self.assertRaises(ValueError):
                fn([])

    def test_single_element(self):
        for x in (-7, 0, 5):
            self.assertEqual(best_window([x]), (x, 0, 0))
            self.assertEqual(best_window_exhaustive([x]), (x, 0, 0))

    def test_all_positive_takes_whole_array(self):
        values = generate("positive", 50)
        self.assertEqual(best_window(values), (50, 0, 49))
        self.assertEqual(best_window([4, 1, 9, 2]), (16, 0, 3))

    def test_all_negative_takes_largest_single_value(self):
        values = [-8, -3, -5, -3, -9]
        self.assertEqual(best_window(values), (-3, 1, 1))  # earliest of ties
        values = generate("negative", 64)
        self.assertEqual(best_window(values)[0], max(values))
        self.assertEqual(best_window(values), best_window_exhaustive(values))

    def test_alternating(self):
        values = [5, -6, 5, -6, 5, -6, 5]
        self.assertEqual(best_window(values), (5, 0, 0))
        values = [5, -1] * 6
        self.assertEqual(best_window(values), (25, 0, 10))

    def test_ties_and_repeated_values(self):
        self.assertEqual(best_window([0, 0, 0]), (0, 0, 0))
        self.assertEqual(best_window([2, -2, 2]), (2, 0, 0))
        self.assertEqual(best_window([1, -1, 1, -1, 1]), (1, 0, 0))
        self.assertEqual(best_window([-1, 3, -3, 3]), (3, 1, 1))
        self.assertEqual(best_window([7, 7, 7, 7]), (28, 0, 3))

    def test_optimum_at_endpoints(self):
        self.assertEqual(best_window([9, -20, 1, 2]), (9, 0, 0))
        self.assertEqual(best_window([1, 2, -20, 9]), (9, 3, 3))
        self.assertEqual(best_window([-5, -1, 4, 6]), (10, 2, 3))

    def test_optimum_crosses_middle_boundary(self):
        # balanced split of 8 values is [0..3] | [4..7]; best is [2..5]
        values = [-9, -9, 4, 5, 6, 3, -9, -9]
        self.assertEqual(best_window(values), (18, 2, 5))
        self.assertEqual(best_window_exhaustive(values), (18, 2, 5))

    def test_greedy_counterexample_from_report(self):
        self.assertEqual(best_window([5, -1, -1, -1, 5]), (7, 0, 4))


class RandomAgainstBruteForce(unittest.TestCase):
    def test_random_small_arrays(self):
        rng = random.Random(RNG_SEED)
        for _ in range(2000):
            n = rng.randint(1, 18)
            lo = rng.choice([-3, -10])          # small range forces many ties
            values = [rng.randint(lo, 3 if lo == -3 else 10) for _ in range(n)]
            expected = best_window_exhaustive(values)
            self.assertEqual(best_window(values), expected, values)
            self.assertEqual(kadane_range(values), expected, values)
            p = rng.randint(1, 9)
            self.assertEqual(distributed_best_window(values, p), expected, values)

    def test_merge_matches_direct_computation(self):
        rng = random.Random(RNG_SEED + 1)
        for _ in range(500):
            n = rng.randint(1, 14)
            values = [rng.randint(-4, 4) for _ in range(n)]
            for lo in range(n):
                for hi in range(lo, n):
                    self.assertEqual(tuple(summarize(values, lo, hi)),
                                     direct_summary(values, lo, hi), (values, lo, hi))

    def test_merge_is_associative(self):
        rng = random.Random(RNG_SEED + 2)
        for _ in range(500):
            n = rng.randint(3, 12)
            values = [rng.randint(-5, 5) for _ in range(n)]
            i, j = sorted(rng.sample(range(1, n), 2))
            a = summarize(values, 0, i - 1)
            b = summarize(values, i, j - 1)
            c = summarize(values, j, n - 1)
            self.assertEqual(merge(merge(a, b), c), merge(a, merge(b, c)))


class DistributedModel(unittest.TestCase):
    def test_eight_servers_three_rounds(self):
        values = generate("mixed", 800)
        log = []
        result = distributed_best_window(values, 8, log)
        self.assertEqual([len(r) for r in log], [4, 2, 1])
        self.assertEqual(result, best_window_exhaustive(values))

    def test_partition_bounds_are_contiguous(self):
        for n in range(1, 40):
            for p in range(1, 10):
                b = partition_bounds(n, p)
                self.assertEqual(b[0][0], 0)
                self.assertEqual(b[-1][1], n - 1)
                for (l1, h1), (l2, _) in zip(b, b[1:]):
                    self.assertEqual(h1 + 1, l2)


class RangeQueries(unittest.TestCase):
    def test_segment_tree_and_sparse_table_against_scan(self):
        rng = random.Random(RNG_SEED + 3)
        for _ in range(60):
            n = rng.randint(1, 40)
            values = [rng.randint(-6, 6) for _ in range(n)]
            tree, table = SegmentTree(values), DisjointSparseTable(values)
            for lo in range(n):
                for hi in range(lo, n):
                    expected = kadane_range(values, lo, hi)
                    self.assertEqual(tree.query(lo, hi), expected)
                    self.assertEqual(table.query(lo, hi), expected)

    def test_segment_tree_point_updates(self):
        rng = random.Random(RNG_SEED + 4)
        values = [rng.randint(-6, 6) for _ in range(33)]
        tree = SegmentTree(values)
        for _ in range(300):
            k = rng.randrange(len(values))
            values[k] = rng.randint(-6, 6)
            tree.update(k, values[k])
            lo = rng.randrange(len(values))
            hi = rng.randrange(lo, len(values))
            self.assertEqual(tree.query(lo, hi), kadane_range(values, lo, hi))


class TwoWindows(unittest.TestCase):
    def test_given_instance(self):
        total, windows = best_two_windows(GIVEN_INSTANCE)
        self.assertEqual(total, 23)
        self.assertEqual(total, brute_two(GIVEN_INSTANCE))
        self.assertEqual(sum(sum(GIVEN_INSTANCE[a:b + 1]) for a, b in windows), total)

    def test_small_cases(self):
        self.assertEqual(best_two_windows([4])[0], 4)
        self.assertEqual(best_two_windows([-4])[0], -4)
        self.assertEqual(best_two_windows([-4, -1])[0], -1)   # one window is better
        self.assertEqual(best_two_windows([5, -9, 6])[0], 11)

    def test_random_against_exhaustive(self):
        rng = random.Random(RNG_SEED + 5)
        for _ in range(600):
            n = rng.randint(1, 9)
            values = [rng.randint(-6, 6) for _ in range(n)]
            total, windows = best_two_windows(values)
            self.assertEqual(total, brute_two(values), values)
            self.assertEqual(total, best_k_windows(values, 2), values)
            self.assertIn(len(windows), (1, 2))
            self.assertEqual(sum(sum(values[a:b + 1]) for a, b in windows), total)
            if len(windows) == 2:
                self.assertLess(windows[0][1], windows[1][0])  # non-overlapping

    def test_k_equals_one_matches_single_window(self):
        rng = random.Random(RNG_SEED + 6)
        for _ in range(300):
            values = [rng.randint(-6, 6) for _ in range(rng.randint(1, 15))]
            self.assertEqual(best_k_windows(values, 1), best_window(values)[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
