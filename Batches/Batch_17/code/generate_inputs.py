"""
generate_inputs.py  --  Batch 17 (Digital Marketing, 0/1 Knapsack)

Generates every dataset used in the project so that the Dynamic Programming
solution and the Greedy (rejected) solution are always run on IDENTICAL input.

Datasets
--------
given_instance()      the six campaigns from the question, budget = 9 lakh
generate(n, seed)     random benchmark instance with n campaigns
worst_case(n, B)      input that maximises the DP work (all costs = 1)
large_instance(...)   the "changed requirement": 300 campaigns, budget in rupees

Usage
-----
    python generate_inputs.py                       # print the given instance
    python generate_inputs.py --n 50                # print a random 50-campaign instance
    python generate_inputs.py --n 50 --out in.json  # save it as JSON
    python generate_inputs.py --bench-dir data/     # save all benchmark sizes as JSON
"""
import argparse
import json
import os
import random

# Input sizes used in the benchmark (faculty asks for >= 5)
BENCH_SIZES = [10, 20, 50, 100, 200, 500, 1000]
SEED = 17  # batch number -> reproducible results

# ---- the instance given in the question ------------------------------------
GIVEN_NAMES = ["C1", "C2", "C3", "C4", "C5", "C6"]
GIVEN_COSTS = [2, 3, 4, 5, 1, 6]          # Rs lakh
GIVEN_VALUES = [30, 45, 50, 70, 12, 80]   # expected conversions
GIVEN_BUDGET = 9                          # Rs lakh


def given_instance():
    """Return (names, costs, values, budget) for the question's instance."""
    return list(GIVEN_NAMES), list(GIVEN_COSTS), list(GIVEN_VALUES), GIVEN_BUDGET


def generate(n, seed=SEED):
    """
    Random instance with n campaigns.
    cost  : integer in [1, 20]  (lakh)
    value : about 10 x cost +- noise (so cost and value are correlated but not
            perfectly - this is the hard case for greedy and a realistic one)
    budget: half of the total cost, so roughly half of the campaigns fit.
    """
    rng = random.Random(seed * 100003 + n)
    costs = [rng.randint(1, 20) for _ in range(n)]
    values = [max(1, 10 * c + rng.randint(-30, 30)) for c in costs]
    budget = sum(costs) // 2
    names = [f"C{i + 1}" for i in range(n)]
    return names, costs, values, budget


def worst_case(n, budget=None, seed=SEED):
    """
    Worst case for the DP: every campaign has the smallest possible cost (1),
    so for every campaign the inner loop touches (almost) all B+1 budget cells,
    giving n*B updates.  The budget is made large (10 n by default).
    """
    rng = random.Random(seed + n)
    if budget is None:
        budget = 10 * n
    costs = [1] * n
    values = [rng.randint(1, 100) for _ in range(n)]
    names = [f"C{i + 1}" for i in range(n)]
    return names, costs, values, budget


def large_instance(n=300, budget=43_752_900, seed=SEED):
    """
    Changed requirement (Question 4): 300 campaigns, budget Rs 4,37,52,900,
    precision = 1 rupee.  Costs: Rs 50,000 .. Rs 5,000,000 ; conversions
    roughly proportional to cost (+- noise).
    """
    rng = random.Random(seed)
    costs = [rng.randint(50_000, 5_000_000) for _ in range(n)]
    values = [max(1, int(c / 1000 * rng.uniform(0.6, 1.4))) for c in costs]
    names = [f"C{i + 1}" for i in range(n)]
    return names, costs, values, budget


def to_dict(names, costs, values, budget):
    return {"names": names, "costs": costs, "values": values, "budget": budget}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, help="number of campaigns for a random instance")
    ap.add_argument("--out", help="write the instance to this JSON file")
    ap.add_argument("--bench-dir", help="write all benchmark instances into this folder")
    args = ap.parse_args()

    if args.bench_dir:
        os.makedirs(args.bench_dir, exist_ok=True)
        for n in BENCH_SIZES:
            path = os.path.join(args.bench_dir, f"input_n{n}.json")
            with open(path, "w") as f:
                json.dump(to_dict(*generate(n)), f)
            print("wrote", path)
        return

    inst = generate(args.n) if args.n else given_instance()
    data = to_dict(*inst)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(data, f, indent=2)
        print("wrote", args.out)
    else:
        print(json.dumps(data, indent=2) if args.n is None or args.n <= 20 else
              f"n={len(data['costs'])}, budget={data['budget']} (use --out to save)")


if __name__ == "__main__":
    main()
