#!/usr/bin/env python3
"""
generate_inputs.py -- reproducible inputs for testing and timing.

All amounts are INTEGER RUPEES.  Two families:

1. "random"  (typical audit batch)
   amounts ~ uniform integers in [1000, 100000]; a hidden set of 4 transactions
   is chosen and its total becomes the target, so >= 1 solution always exists.
   Generator: random.Random(seed + n)  -> same n and seed => same input.

2. "hard"    (difficult search-only family; NO solution exists)
   a_i = M + i for i = 1..n, with M = 10*n*n, and target = (n//2 + 1)*M - 1.
   Every subset with k items has sum in [kM, kM + k*n], these ranges are
   disjoint for different k, and target lies in the gap just below (n//2+1)*M.
   So no subset hits the target, and the search must rule out ~C(n, n//2) subsets.

Usage:  python generate_inputs.py --family random --n 12 --seed 2026
"""
import argparse
import json
import random

DEFAULT_SEED = 2026


def random_instance(n, seed=DEFAULT_SEED, planted=4):
    rng = random.Random(seed + n)
    amounts = [rng.randint(1000, 100000) for _ in range(n)]
    pick = rng.sample(range(n), min(planted, n))
    return amounts, sum(amounts[i] for i in pick), 0


def hard_instance(n):
    M = 10 * n * n
    amounts = [M + i for i in range(1, n + 1)]
    return amounts, (n // 2 + 1) * M - 1, 0


def make_instance(family, n, seed=DEFAULT_SEED):
    if family == "random":
        return random_instance(n, seed)
    if family == "hard":
        return hard_instance(n)
    raise ValueError("family must be 'random' or 'hard'")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", choices=["random", "hard"], default="random")
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    a = ap.parse_args()
    amounts, target, tol = make_instance(a.family, a.n, a.seed)
    print(json.dumps({"family": a.family, "n": a.n, "seed": a.seed,
                      "amounts_rupees": amounts, "target_rupees": target, "tolerance_rupees": tol}))
