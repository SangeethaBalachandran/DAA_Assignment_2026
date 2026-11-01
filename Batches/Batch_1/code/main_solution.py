#!/usr/bin/env python3
"""
main_solution.py  --  Batch 1: Fintech Audit (find EVERY set of pending
transactions whose total equals a disputed debit).

Technique : recursive search over index-ordered subsets with two safe pruning
            rules (overshoot and unreachable).
Money     : always handled as INTEGER RUPEES internally (no floating point).

Quick start (runs the assignment instance, amounts in thousands of rupees):
    python main_solution.py
    python main_solution.py --tolerance 50          # accept +/- Rs 50
    python main_solution.py --trace                 # print every state/prune
"""
import argparse
import sys
from dataclasses import dataclass
from fractions import Fraction

# The instance given in the assignment (thousands of rupees).
DEFAULT_AMOUNTS = ["15", "22", "35", "40", "48", "53", "61"]
DEFAULT_TARGET = "110"
DEFAULT_SCALE = 1000          # 1 input unit = 1000 rupees


# --------------------------------------------------------------------------
# Input handling: exact conversion to integer rupees, with validation
# --------------------------------------------------------------------------
def to_rupees(value, scale, what="value"):
    """Convert `value` (int or decimal text like '0.05') * `scale` to an int.

    Fraction(str(value)) keeps decimals exact, so 0.05 thousand rupees
    becomes exactly 50 rupees. Raises ValueError if the result is not a whole
    number of rupees.
    """
    try:
        exact = Fraction(str(value).strip()) * scale
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"{what}: '{value}' is not a valid number")
    if exact.denominator != 1:
        raise ValueError(f"{what}: '{value}' x {scale} is not a whole number of rupees")
    return int(exact)


def validate(amounts, target, tolerance):
    """Check integer rupee inputs. Positivity of amounts is REQUIRED for pruning."""
    if not amounts:
        raise ValueError("at least one transaction amount is required")
    for i, a in enumerate(amounts):
        if not isinstance(a, int) or isinstance(a, bool):
            raise ValueError(f"amount #{i} must be an integer number of rupees")
        if a <= 0:
            raise ValueError(f"amount #{i} = {a}: amounts must be strictly positive "
                             "(the pruning rules are only safe for positive amounts)")
    if not isinstance(target, int) or target <= 0:
        raise ValueError("target must be a positive integer number of rupees")
    if not isinstance(tolerance, int) or tolerance < 0:
        raise ValueError("tolerance must be a non-negative integer number of rupees")


# --------------------------------------------------------------------------
# Result container
# --------------------------------------------------------------------------
@dataclass
class Result:
    amounts: list            # integer rupees, in ORIGINAL input order
    target: int
    tolerance: int
    solutions: list          # list of tuples of ORIGINAL indices (0-based)
    states: int              # recursive calls = subsets generated (incl. empty root)
    prune_overshoot: int     # cut-off events: next item would exceed target+tol
    prune_unreachable: int   # cut-off events: even all remaining items cannot reach target-tol
    skipped_children: int    # child branches never created because of a cut-off

    def values(self, sol):
        return [self.amounts[i] for i in sol]


# --------------------------------------------------------------------------
# The algorithm
# --------------------------------------------------------------------------
def solve(amounts, target, tolerance=0, trace=None):
    """Return every NON-EMPTY subset (as original indices) whose sum s satisfies
    target - tolerance <= s <= target + tolerance.

    Each transaction is a separate item (identified by index), so equal amounts
    are never merged and no item is used twice.

    `trace`, if given, is called as trace(event, state_id, depth, chosen_values,
    current_sum, info) for visual tracing; pass None for timing runs.
    """
    validate(amounts, target, tolerance)
    n = len(amounts)
    # Sort ascending (ties broken by original index) so that, from any point,
    # later items are never smaller.  `order[p]` = original index at sorted slot p.
    order = sorted(range(n), key=lambda i: (amounts[i], i))
    vals = [amounts[i] for i in order]
    # suffix[j] = vals[j] + vals[j+1] + ... + vals[n-1]
    suffix = [0] * (n + 1)
    for j in range(n - 1, -1, -1):
        suffix[j] = suffix[j + 1] + vals[j]

    lo, hi = target - tolerance, target + tolerance
    solutions = []
    chosen = []                       # sorted-slot positions currently chosen
    counters = [0, 0, 0, 0]           # states, overshoot, unreachable, skipped

    def search(start, current, state_id, depth):
        # This call IS one candidate subset: `chosen` with total `current`.
        if trace:
            trace("visit", state_id, depth, [vals[p] for p in chosen], current, None)
        if chosen and lo <= current <= hi:
            solutions.append(tuple(sorted(order[p] for p in chosen)))
            if trace:
                trace("solution", state_id, depth, [vals[p] for p in chosen], current, None)
        for j in range(start, n):
            # Rule 2 (unreachable): even taking ALL items j..n-1 stays below lo.
            # Holds for every larger j as well (suffix shrinks) -> stop the loop.
            if current + suffix[j] < lo:
                counters[2] += 1
                counters[3] += n - j
                if trace:
                    trace("prune_unreachable", state_id, depth, [vals[p] for p in chosen],
                          current, (j, vals[j], current + suffix[j], n - j))
                break
            # Rule 1 (overshoot): adding vals[j] already exceeds hi.  Amounts are
            # positive and sorted ascending, so every later item overshoots too.
            if current + vals[j] > hi:
                counters[1] += 1
                counters[3] += n - j
                if trace:
                    trace("prune_overshoot", state_id, depth, [vals[p] for p in chosen],
                          current, (j, vals[j], current + vals[j], n - j))
                break
            chosen.append(j)
            counters[0] += 1
            search(j + 1, current + vals[j], counters[0], depth + 1)
            chosen.pop()

    counters[0] = 1                    # the empty subset is the root state (id 1)
    search(0, 0, 1, 0)
    solutions.sort()
    return Result(list(amounts), target, tolerance, solutions,
                  counters[0], counters[1], counters[2], counters[3])


# --------------------------------------------------------------------------
# Command-line interface
# --------------------------------------------------------------------------
def _make_printer():
    def printer(event, sid, depth, chosen_vals, cur, info):
        pad = "  " * depth
        if event == "visit":
            print(f"S{sid:<3} {pad}{chosen_vals} sum={cur}" + ("  (root, empty subset)" if sid == 1 else ""))
        elif event == "solution":
            print(f"     {pad}  ==> SOLUTION at S{sid}: {chosen_vals} sums to {cur}")
        else:
            j, v, val, skipped = info
            kind = "OVERSHOOT" if event == "prune_overshoot" else "UNREACHABLE"
            what = (f"adding {v} gives {val} > hi" if kind == "OVERSHOOT"
                    else f"max reachable {val} < lo")
            print(f"     {pad}  prune[{kind}] at S{sid}: {what}; skips {skipped} child branch(es)")
    return printer


def main(argv=None):
    p = argparse.ArgumentParser(description="Enumerate all subsets of transactions summing to a target.")
    p.add_argument("--amounts", nargs="+", default=DEFAULT_AMOUNTS,
                   help="transaction amounts in input units (default: assignment instance)")
    p.add_argument("--target", default=DEFAULT_TARGET, help="disputed amount in input units")
    p.add_argument("--scale", type=int, default=DEFAULT_SCALE,
                   help="rupees per input unit (1000 = amounts are in thousands; 1 = plain rupees)")
    p.add_argument("--tolerance", default="0", help="allowed difference, in RUPEES (e.g. 50)")
    p.add_argument("--trace", action="store_true", help="print every state and pruning event")
    args = p.parse_args(argv)
    try:
        amounts = [to_rupees(a, args.scale, f"amount #{i}") for i, a in enumerate(args.amounts)]
        target = to_rupees(args.target, args.scale, "target")
        tol = to_rupees(args.tolerance, 1, "tolerance")
        validate(amounts, target, tol)
    except ValueError as e:
        print("Input error:", e, file=sys.stderr)
        return 2

    res = solve(amounts, target, tol, trace=_make_printer() if args.trace else None)

    print(f"Transactions (Rs): {amounts}")
    print(f"Target = Rs {target}, tolerance = Rs {tol}  ->  accept sums in [{target - tol}, {target + tol}]")
    print(f"Solutions found: {len(res.solutions)}")
    for sol in res.solutions:
        vals = res.values(sol)
        print(f"  indices {[i + 1 for i in sol]} (1-based) amounts {vals} sum = {sum(vals)}")
    print(f"States visited (subsets generated, incl. empty root): {res.states}   (all subsets: 2^{len(amounts)} = {2 ** len(amounts)})")
    print(f"Prune events: overshoot={res.prune_overshoot}, unreachable={res.prune_unreachable}; "
          f"child branches skipped={res.skipped_children}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
