#!/usr/bin/env python3
"""Deterministic input generator for the timing experiments.

Usage: python3 generate_inputs.py N [--kind random|mutated|identical|mismatch] [--seed S]
Prints the reference on line 1 and the read on line 2.
"""
import argparse
import random

BASES = "ACGT"


def random_seq(n, rng):
    return "".join(rng.choice(BASES) for _ in range(n))


def make_pair(n, kind="random", seed=1):
    rng = random.Random(seed)
    if kind == "identical":
        s = random_seq(n, rng)
        return s, s
    if kind == "mismatch":                 # worst constant factor: no base ever matches
        return "A" * n, "C" * n
    if kind == "mutated":                  # realistic read: ~3% substitutions / indels
        ref = random_seq(n, rng)
        read = []
        for c in ref:
            r = rng.random()
            if r < 0.01:
                read.append(rng.choice(BASES))        # substitution
            elif r < 0.02:
                continue                              # deletion
            elif r < 0.03:
                read.append(c)
                read.append(rng.choice(BASES))        # insertion
            else:
                read.append(c)
        return ref, "".join(read)
    return random_seq(n, rng), random_seq(n, rng)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--kind", default="random")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    r, q = make_pair(a.n, a.kind, a.seed)
    print(r)
    print(q)
