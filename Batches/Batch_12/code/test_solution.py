"""Correctness tests: optimized merge-sort counting vs the brute-force baseline.

Run from the Batch_12 folder:  python -m unittest discover -s code -v
"""
import random
import unittest

from generate_inputs import generate_permutation
from main_solution import count_inversions, count_weighted_inversions
from rejected_alternative import (count_inversions_brute,
                                  count_weighted_inversions_brute)


class InversionTests(unittest.TestCase):
    def test_given_instance(self):
        example = [3, 1, 6, 2, 8, 4, 7, 5]
        sorted_array, score = count_inversions(example)
        self.assertEqual(score, 9)
        self.assertEqual(sorted_array, sorted(example))

    def test_edge_cases(self):
        self.assertEqual(count_inversions([])[1], 0)
        self.assertEqual(count_inversions([7])[1], 0)
        self.assertEqual(count_inversions([1, 2, 3, 4])[1], 0)

    def test_reverse_sorted_is_maximum(self):
        for n in (2, 8, 50, 301):
            values = generate_permutation(n, order="reverse")
            self.assertEqual(count_inversions(values)[1], n * (n - 1) // 2)
        self.assertEqual(count_inversions(generate_permutation(8, order="reverse"))[1], 28)

    def test_input_is_not_modified(self):
        values = [3, 1, 2]
        count_inversions(values)
        self.assertEqual(values, [3, 1, 2])

    def test_random_permutations_match_brute_force(self):
        rng = random.Random(12)
        for _ in range(500):
            n = rng.randint(0, 80)
            values = generate_permutation(n, seed=rng.random())
            fast_sorted, fast = count_inversions(values)
            self.assertEqual(fast, count_inversions_brute(values))
            self.assertEqual(fast_sorted, sorted(values))


class WeightedTests(unittest.TestCase):
    def test_given_instance_all_titles_are_top10(self):
        example = [3, 1, 6, 2, 8, 4, 7, 5]
        inversions, weighted = count_weighted_inversions(example, top_k=10)
        self.assertEqual((inversions, weighted), (9, 45))
        self.assertEqual(count_weighted_inversions_brute(example, top_k=10), 45)

    def test_mixed_top_and_non_top_titles(self):
        # n > top_k, so both the weight-5 and the weight-1 paths are exercised.
        rng = random.Random(34)
        saw_weight_one = False
        for _ in range(500):
            n = rng.randint(11, 70)
            k = rng.choice([1, 3, 5, 10])
            values = generate_permutation(n, seed=rng.random())
            inversions, weighted = count_weighted_inversions(values, top_k=k)
            self.assertEqual(inversions, count_inversions_brute(values))
            self.assertEqual(weighted, count_weighted_inversions_brute(values, top_k=k))
            saw_weight_one |= weighted < 5 * inversions
        self.assertTrue(saw_weight_one, "tests never hit a weight-1 inversion")

    def test_weighted_bounds(self):
        values = generate_permutation(200, seed=5)
        inversions, weighted = count_weighted_inversions(values, top_k=10)
        self.assertGreaterEqual(weighted, inversions)
        self.assertLessEqual(weighted, 5 * inversions)


if __name__ == "__main__":
    unittest.main()
