"""Batch 5: Main Solution - Satellite Knapsack Problem.

Technique: Branch and Bound with Fractional (LP-relaxation) Upper Bounding.
Course: 23I501 - Design and Analysis of Algorithms (DAA)
Institution: PSG College of Technology

Problem Scenario:
    Select a subset of scientific instruments for a satellite to maximize
    scientific value subject to a strict total mass capacity of 15.0 kg
    (measured to 0.1 g precision). Later, a 35 W power constraint is also applied.

Usage:
    python main_solution.py [--trace]
"""

from __future__ import annotations

import argparse
import heapq
import itertools
import math
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any

UNITS_PER_KG = 10_000  # 1 unit = 0.1 gram (avoids floating-point errors)


def kg_to_units(kg: float) -> int:
    """Convert mass in kilograms to integer units of 0.1 gram."""
    return round(kg * UNITS_PER_KG)


def fmt_kg(units: int) -> str:
    """Format integer units back into kilogram string."""
    return f"{units / UNITS_PER_KG:g}"


@dataclass(frozen=True)
class Item:
    """Represents a satellite scientific instrument."""
    name: str
    mass: int     # units of 0.1 g
    value: int    # scientific value points
    power: int    # power consumption in Watts

    @property
    def kg(self) -> float:
        return self.mass / UNITS_PER_KG

    @property
    def density(self) -> float:
        """Value per kilogram."""
        return self.value / self.kg


# Given instance from Scenario Batch 5:
# P1: 2.5 kg, 40 value, 8 W
# P2: 3.2 kg, 42 value, 12 W
# P3: 4.8 kg, 60 value, 10 W
# P4: 6.1 kg, 72 value, 15 W
# P5: 1.7 kg, 18 value, 4 W
# P6: 5.4 kg, 54 value, 9 W
RAW_DATA = [
    ("P1", 2.5, 40, 8),
    ("P2", 3.2, 42, 12),
    ("P3", 4.8, 60, 10),
    ("P4", 6.1, 72, 15),
    ("P5", 1.7, 18, 4),
    ("P6", 5.4, 54, 9),
]

INSTANCE = [Item(name, kg_to_units(m), v, p) for name, m, v, p in RAW_DATA]
MASS_CAPACITY = kg_to_units(15.0)  # 150,000 units (15.0 kg)
POWER_CAPACITY = 35                 # 35 Watts


def branch_and_bound(
    items: List[Item],
    cap: int,
    pcap: Optional[int] = None,
    trace: bool = False
) -> Dict[str, Any]:
    """Solve 0/1 knapsack using Best-First Branch and Bound with Fractional LP bound.

    Args:
        items: List of scientific instruments.
        cap: Maximum mass capacity (integer units).
        pcap: Optional maximum power capacity (Watts).
        trace: Whether to capture execution trace log.

    Returns:
        Dictionary containing optimal value, selected items, stats, and trace log.
    """
    n = len(items)
    # Order items by value density descending for optimal fractional bounding
    mass_order = sorted(range(n), key=lambda i: -items[i].value / items[i].mass)
    pow_order = (
        sorted(range(n), key=lambda i: -items[i].value / items[i].power)
        if pcap is not None else None
    )

    def fractional_bound(order: List[int], attr: str, level: int, room: int) -> float:
        total = 0.0
        for i in order:
            if i < level:
                continue
            r = getattr(items[i], attr)
            if r <= room:
                room -= r
                total += items[i].value
            else:
                total += items[i].value * (room / r)
                break
        return total

    def compute_bound(level: int, current_val: int, current_mass: int, current_pow: int) -> float:
        b = current_val + fractional_bound(mass_order, "mass", level, cap - current_mass)
        if pcap is not None:
            # The intersection of two relaxation bounds is bounded by their minimum
            b = min(b, current_val + fractional_bound(pow_order, "power", level, pcap - current_pow))
        return b

    tick = itertools.count()
    frontier: List[Tuple[float, int, Tuple[int, int, int, int, Tuple[str, ...]]]] = []
    
    # Priority queue on upper bound (max-heap via negated bound)
    def push(node, b):
        heapq.heappush(frontier, (-b, next(tick), node))

    def pop():
        neg_b, _, node = heapq.heappop(frontier)
        return node, -neg_b

    stats = dict(
        generated=1,
        expanded=0,
        pruned=0,
        infeasible=0,
        best=0,
        best_set=(),
        gen_at_best=1,
        exp_at_best=0,
        max_frontier=1,
    )
    log = []

    def label(ch: Tuple[str, ...]) -> str:
        return "{" + ",".join(ch) + "}" if ch else "{}"

    def cannot_beat(b: float) -> bool:
        # Values are integers, so floor(bound) is an admissible upper integer bound
        return math.floor(b + 1e-9) <= stats["best"]

    root_bound = compute_bound(0, 0, 0, 0)
    push((0, 0, 0, 0, ()), root_bound)
    if trace:
        log.append(f"Root node initialized: upper bound = {root_bound:.2f}")

    while frontier:
        (level, v, m, p, chosen), b = pop()

        # Prune check on extraction
        if cannot_beat(b):
            stats["pruned"] += 1
            if trace:
                log.append(f"POP  {label(chosen):<18} v={v:<4} bound={b:7.2f} <= incumbent {stats['best']} -> PRUNED")
            # In best-first search, if current best in max-heap cannot beat incumbent, all remaining cannot beat it
            stats["pruned"] += len(frontier)
            if trace:
                log.append(f"     Best-first termination: {len(frontier)} nodes remaining in heap have bound <= {stats['best']}")
            break

        stats["expanded"] += 1
        if trace:
            log.append(f"POP  {label(chosen):<18} v={v:<4} mass={fmt_kg(m):>5} kg bound={b:7.2f} -> EXPAND {items[level].name if level < n else 'leaf'}")

        if level == n:
            continue

        item = items[level]
        children = []

        # 1. Branch Include item
        stats["generated"] += 1
        new_m = m + item.mass
        new_p = p + item.power
        if new_m <= cap and (pcap is None or new_p <= pcap):
            new_v = v + item.value
            new_chosen = chosen + (item.name,)
            if new_v > stats["best"]:
                stats["best"] = new_v
                stats["best_set"] = new_chosen
                stats["gen_at_best"] = stats["generated"]
                stats["exp_at_best"] = stats["expanded"]
                if trace:
                    log.append(f"     * New incumbent: {label(new_chosen)} with value {new_v} *")
            b_inc = compute_bound(level + 1, new_v, new_m, new_p)
            children.append(((level + 1, new_v, new_m, new_p, new_chosen), b_inc, "Include"))
        else:
            stats["infeasible"] += 1
            if trace:
                log.append(f"     Include {item.name}: exceeds capacity (mass={fmt_kg(new_m)} kg, pwr={new_p} W) -> INFEASIBLE")

        # 2. Branch Exclude item
        stats["generated"] += 1
        b_exc = compute_bound(level + 1, v, m, p)
        children.append(((level + 1, v, m, p, chosen), b_exc, "Exclude"))

        # Evaluate and queue children
        for node_data, child_bound, kind in children:
            if cannot_beat(child_bound):
                stats["pruned"] += 1
                if trace:
                    log.append(f"     {kind} {item.name}: bound={child_bound:7.2f} <= incumbent {stats['best']} -> PRUNED immediately")
            else:
                push(node_data, child_bound)
                if trace:
                    log.append(f"     {kind} {item.name}: bound={child_bound:7.2f} -> Enqueued")

        stats["max_frontier"] = max(stats["max_frontier"], len(frontier))

    return dict(best=stats["best"], best_set=stats["best_set"], stats=stats, log=log)


def solve_and_display(trace: bool = False):
    print("=" * 75)
    print("DAA ASSIGNMENT - BATCH 5: SATELLITE KNAPSACK PROBLEM")
    print("Technique: Best-First Branch and Bound with Fractional LP Bound")
    print("=" * 75)
    
    # Sort items by value density for the decision tree
    sorted_items = sorted(INSTANCE, key=lambda it: -it.value / it.mass)
    print("\nInstruments sorted by value-to-mass density:")
    print(f"{'Item':<6}{'Mass (kg)':<12}{'Value':<10}{'Power (W)':<12}{'Density (val/kg)':<18}")
    print("-" * 58)
    for it in sorted_items:
        print(f"{it.name:<6}{fmt_kg(it.mass):<12}{it.value:<10}{it.power:<12}{it.density:<18.3f}")

    # --- Part 1: Question 2 (Mass constraint: 15.0 kg) ---
    print("\n" + "-" * 75)
    print("Part 1: Primary Selection (Mass capacity = 15.0 kg)")
    print("-" * 75)
    res1 = branch_and_bound(sorted_items, MASS_CAPACITY, pcap=None, trace=trace)
    
    if trace:
        print("\n--- Step-by-Step Exploration Trace ---")
        print("\n".join(res1["log"]))
        print("-" * 50)

    chosen1 = [it for it in INSTANCE if it.name in set(res1["best_set"])]
    tot_val1 = sum(it.value for it in chosen1)
    tot_mass1 = sum(it.mass for it in chosen1)
    tot_pwr1 = sum(it.power for it in chosen1)
    s1 = res1["stats"]

    print(f"\nOptimal Solution: {res1['best_set']}")
    print(f"Total Scientific Value : {tot_val1}")
    print(f"Total Mass Consumed    : {fmt_kg(tot_mass1)} kg / 15.0 kg")
    print(f"Total Power Consumed   : {tot_pwr1} W")
    print(f"Nodes Generated        : {s1['generated']} (vs 2^6 = 64 complete subsets; 127 total tree nodes)")
    print(f"Nodes Expanded         : {s1['expanded']}")
    print(f"Nodes Pruned           : {s1['pruned']}")
    print(f"Infeasible Nodes       : {s1['infeasible']}")

    # --- Part 2: Question 5 (Changed requirement: +35 W power limit) ---
    print("\n" + "-" * 75)
    print("Part 2: Changed Requirement (+35 W Power Constraint)")
    print("-" * 75)
    print(f"Checking old optimum {res1['best_set']}: power consumed = {tot_pwr1} W > 35 W limit -> INFEASIBLE.")
    
    res2 = branch_and_bound(sorted_items, MASS_CAPACITY, pcap=POWER_CAPACITY, trace=trace)
    chosen2 = [it for it in INSTANCE if it.name in set(res2["best_set"])]
    tot_val2 = sum(it.value for it in chosen2)
    tot_mass2 = sum(it.mass for it in chosen2)
    tot_pwr2 = sum(it.power for it in chosen2)
    s2 = res2["stats"]

    print(f"\nNew Optimal Solution   : {res2['best_set']}")
    print(f"Total Scientific Value : {tot_val2}")
    print(f"Total Mass Consumed    : {fmt_kg(tot_mass2)} kg / 15.0 kg")
    print(f"Total Power Consumed   : {tot_pwr2} W / 35 W")
    print(f"Nodes Generated        : {s2['generated']}")
    print(f"Nodes Expanded         : {s2['expanded']}")
    print(f"Nodes Pruned           : {s2['pruned']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve Satellite Knapsack via Branch & Bound")
    parser.add_argument("--trace", action="store_true", help="Print step-by-step branch and bound execution trace")
    args = parser.parse_args()
    solve_and_display(trace=args.trace)

