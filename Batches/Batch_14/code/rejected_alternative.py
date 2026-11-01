"""Rejected alternative: exhaustive enumeration of all 2^n configurations (generate and test).
Constraints are re-implemented independently from the backtracking checker."""
from itertools import product
from main_solution import ECU, SENSORS_FIRST, FEATURES_FIRST, enumerate_valid


def is_valid(inst, cfg):
    """cfg: dict name->0/1. Full validation of every constraint."""
    for a, b in inst.requires:
        if cfg[a] and not cfg[b]:
            return False
    for a, b in inst.excludes:
        if cfg[a] and cfg[b]:
            return False
    for grp in inst.atleast:
        if not any(cfg[v] for v in grp):
            return False
    return sum(inst.cost.get(v, 0) for v in inst.names if cfg[v]) <= inst.budget


def exhaustive(inst):
    out, checked = [], 0
    for bits in product((0, 1), repeat=len(inst.names)):
        checked += 1
        if is_valid(inst, dict(zip(inst.names, bits))):
            out.append(bits)
    return out, checked


if __name__ == "__main__":
    sols, checked = exhaustive(ECU)
    print(f"Exhaustive: examined {checked} = 2^7 complete configurations, {len(sols)} valid")
    for i, s in enumerate(sols, 1):
        print(f"  {i}. {''.join(map(str, s))}  {{{', '.join(v for v, x in zip(ECU.names, s) if x)}}}")
    for name, order in (("sensors-first", SENSORS_FIRST), ("features-first", FEATURES_FIRST)):
        bt, _ = enumerate_valid(ECU, order)
        assert sorted(bt) == sorted(sols), name
        print(f"Identical to backtracking ({name}): True")
