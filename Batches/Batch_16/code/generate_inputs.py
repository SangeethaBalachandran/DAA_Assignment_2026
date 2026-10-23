"""Batch 16 - deterministic input generator.

Kinds
-----
mixed     signed integers in [-10, 10] (daily changes in rupees)
positive  all ones [1, 1, ..., 1]: the constructed worst case discussion
negative  integers in [-10, -1]: correctness check for non-empty windows
given     the 12-value instance from the assignment

File format (shared by every script): one integer per line.
The default seed is 2026; the same (kind, n, seed) always gives the same list.
"""

from __future__ import annotations

import argparse
import random
import sys

DEFAULT_SEED = 2026
GIVEN_INSTANCE = [3, -5, 8, -2, 6, -9, 4, 7, -3, -6, 5, 2]
KINDS = ("mixed", "positive", "negative", "given")


def generate(kind: str, n: int, seed: int = DEFAULT_SEED) -> list[int]:
    if kind == "given":
        return list(GIVEN_INSTANCE)
    if n < 0:
        raise ValueError("n must be non-negative")
    rng = random.Random(f"{seed}:{kind}:{n}")
    if kind == "mixed":
        return [rng.randint(-10, 10) for _ in range(n)]
    if kind == "positive":
        return [1] * n
    if kind == "negative":
        return [rng.randint(-10, -1) for _ in range(n)]
    raise ValueError(f"unknown kind {kind!r}; choose from {KINDS}")


def write_values(path: str, values: list[int]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(str(v) for v in values) + "\n")


def read_values(path: str) -> list[int]:
    with open(path, encoding="utf-8") as fh:
        return [int(tok) for tok in fh.read().replace(",", " ").split()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--kind", choices=KINDS, default="mixed")
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", help="output file (default: stdout)")
    args = parser.parse_args(argv)
    values = generate(args.kind, args.n, args.seed)
    if args.out:
        write_values(args.out, values)
        print(f"wrote {len(values)} values to {args.out}")
    else:
        sys.stdout.write("\n".join(map(str, values)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
