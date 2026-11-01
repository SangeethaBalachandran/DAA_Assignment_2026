"""
rejected_alternative.py  --  Batch 17 (Digital Marketing, 0/1 Knapsack)

REJECTED TECHNIQUE: Greedy (conversions-per-lakh ratio).

Algorithm
---------
1. ratio_i = conversions_i / cost_i
2. sort campaigns by ratio, highest first (ties: original order)
3. walk through the sorted list and take a campaign whenever it still fits
4. report the total conversions

Time  : O(n log n)  (sorting dominates)
Space : O(n)
It is FAST but NOT guaranteed optimal for the indivisible 0/1 problem.
On the given instance it returns 125 conversions, the true optimum is 127.
"""
from fractions import Fraction
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_inputs import given_instance


def greedy_knapsack(costs, values, budget):
    """Return (total_value, selected_indices_in_pick_order, total_cost)."""
    n = len(costs)
    # Fraction keeps the ratio comparison exact (no floating point ties).
    order = sorted(range(n), key=lambda i: (-Fraction(values[i], costs[i]), i))
    remaining = budget
    chosen, total_value, total_cost = [], 0, 0
    for i in order:
        if costs[i] <= remaining:
            chosen.append(i)
            remaining -= costs[i]
            total_value += values[i]
            total_cost += costs[i]
    return total_value, chosen, total_cost


def main():
    names, costs, values, budget = given_instance()
    print("GREEDY (ratio) on the given instance, budget = Rs", budget, "lakh\n")
    print(f"{'Campaign':<9}{'Cost':>6}{'Conv.':>7}{'Ratio':>9}")
    for i in sorted(range(len(costs)), key=lambda i: (-Fraction(values[i], costs[i]), i)):
        print(f"{names[i]:<9}{costs[i]:>6}{values[i]:>7}{values[i] / costs[i]:>9.2f}")
    total, chosen, cost = greedy_knapsack(costs, values, budget)
    print("\nPick order :", [names[i] for i in chosen])
    print("Total cost :", cost, "lakh")
    print("Conversions:", total)


if __name__ == "__main__":
    main()
