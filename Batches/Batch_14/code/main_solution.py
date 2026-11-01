"""Primary solution: recursive backtracking for valid ECU feature configurations.
Batch 14 - 23I501 DAA. Python 3, standard library only.

Usage:
  python main_solution.py            # 7-feature ECU: results + stats for both orders
  python main_solution.py --trace    # + full execution trace (features-first order)
  python main_solution.py --worst    # worst-case instances (real measured counts)
  python main_solution.py --bdd      # ROBDD node counts for both orders
"""
import sys
from collections import namedtuple

Instance = namedtuple("Instance", "names cost requires excludes atleast budget")
# names: list[str]; cost: dict name->int (0 for non-sensors)
# requires: [(a,b)] a=1 -> b=1 ; excludes: [(a,b)] not(a and b)
# atleast: [(names...)] at least one =1 ; budget: max total cost (global constraint)

CANON = ["ACC", "BC", "LKA", "PA", "RAD", "CAM", "US"]
ECU = Instance(
    names=CANON,
    cost={"ACC": 0, "BC": 0, "LKA": 0, "PA": 0, "RAD": 12000, "CAM": 8000, "US": 5000},
    requires=[("ACC", "RAD"), ("LKA", "CAM"), ("PA", "US")],
    excludes=[("ACC", "BC")],
    atleast=[("ACC", "BC")],
    budget=20000,
)
SENSORS_FIRST = ["RAD", "CAM", "US", "ACC", "BC", "LKA", "PA"]
FEATURES_FIRST = ["ACC", "BC", "LKA", "PA", "RAD", "CAM", "US"]


def build_checks(inst, order):
    """Map depth -> constraints whose LAST variable (in this order) is order[depth]."""
    pos = {v: i for i, v in enumerate(order)}
    checks = [[] for _ in order]
    for a, b in inst.requires:
        checks[max(pos[a], pos[b])].append(("requires", a, b))
    for a, b in inst.excludes:
        checks[max(pos[a], pos[b])].append(("excludes", a, b))
    for grp in inst.atleast:
        checks[max(pos[v] for v in grp)].append(("atleast", *grp))
    return checks


def violated(c, asg):
    kind = c[0]
    if kind == "requires":
        return asg[c[1]] == 1 and asg[c[2]] == 0
    if kind == "excludes":
        return asg[c[1]] == 1 and asg[c[2]] == 1
    return all(asg[v] == 0 for v in c[1:])  # atleast


def enumerate_valid(inst, order, trace=None):
    """Recursive backtracking. Returns (solutions, stats)."""
    n = len(order)
    checks = build_checks(inst, order)
    asg, sols = {}, []
    st = dict(calls=0, tried=0, pruned=0, pruned_cost=0, pruned_logic=0, solutions=0, by_depth={})

    def search(d, cost):
        st["calls"] += 1
        if d == n:
            st["solutions"] += 1
            sols.append(tuple(asg[v] for v in inst.names))
            if trace is not None:
                trace.append("  " * d + f"SOLUTION {fmt(inst, asg)}")
            return
        var = order[d]
        for val in (0, 1):
            st["tried"] += 1
            asg[var] = val
            ncost = cost + (inst.cost.get(var, 0) if val else 0)
            reason = None
            if ncost > inst.budget:                      # global (bound) constraint
                reason = f"sensor cost {ncost} > {inst.budget}"
                st["pruned_cost"] += 1
            else:
                for c in checks[d]:                      # constraints now fully assigned
                    if violated(c, asg):
                        reason = f"{c[0]}({', '.join(c[1:])}) violated"
                        st["pruned_logic"] += 1
                        break
            label = "  " * d + f"d{d + 1}: {var}={val}"
            if reason:
                st["pruned"] += 1
                st["by_depth"][d + 1] = st["by_depth"].get(d + 1, 0) + 1
                if trace is not None:
                    trace.append(f"{label}  [cost={ncost}]  PRUNE: {reason}")
            else:
                if trace is not None:
                    trace.append(f"{label}  [cost={ncost}]  ok")
                search(d + 1, ncost)
            del asg[var]

    search(0, 0)
    return sols, st


def fmt(inst, asg):
    on = [v for v in inst.names if asg.get(v) == 1]
    return "{" + ", ".join(on) + "}"


def fmt_tuple(inst, t):
    return "{" + ", ".join(v for v, x in zip(inst.names, t) if x) + "}"


def report(inst, order, name, trace=None):
    sols, st = enumerate_valid(inst, order, trace)
    n = len(order)
    print(f"[{name}] order = {order}")
    print(f"  valid configurations      : {st['solutions']}")
    print(f"  recursive calls           : {st['calls']}  (full tree would have {2 ** (n + 1) - 1})")
    print(f"  assignments examined      : {st['tried']}  (full tree: {2 ** (n + 1) - 2}; complete vectors 2^{n} = {2 ** n})")
    print(f"  assignments pruned        : {st['pruned']}  (cost bound {st['pruned_cost']}, logic {st['pruned_logic']})")
    print(f"  prunes by depth           : {dict(sorted(st['by_depth'].items()))}  "
          f"(mean prune depth {sum(k * v for k, v in st['by_depth'].items()) / max(1, st['pruned']):.2f})")
    return sols, st


# ---------------------------------------------------------------- worst cases
def worst_instances(n):
    names = [f"x{i}" for i in range(n)]
    free = Instance(names, {}, [], [], [], 0)
    # constraint only between FIRST and LAST variable in the order: nothing is pruned
    # until depth n, so the whole tree (except the last level's rejects) is explored.
    late = Instance(names, {}, [(names[0], names[-1])], [], [], 0)
    return names, free, late


def main():
    args = sys.argv[1:]
    if "--worst" in args:
        for n in (10, 15):
            names, free, late = worst_instances(n)
            for label, inst in (("unconstrained", free), ("late-detected requires(x0,x_last)", late)):
                sols, st = enumerate_valid(inst, names)
                print(f"n={n:2d} {label:36s} valid={st['solutions']:6d} calls={st['calls']:6d} "
                      f"examined={st['tried']:6d} pruned={st['pruned']:5d} (2^n={2 ** n})")
        return
    if "--bdd" in args:
        for name, order in (("sensors-first", SENSORS_FIRST), ("features-first", FEATURES_FIRST)):
            sols, _ = enumerate_valid(ECU, order)
            valid = {tuple(dict(zip(ECU.names, s))[v] for v in order) for s in sols}
            uniq = {}

            def mk(prefix):
                d = len(prefix)
                if d == len(order):
                    return 1 if tuple(prefix) in valid else 0
                lo, hi = mk(prefix + [0]), mk(prefix + [1])
                if lo == hi:
                    return lo
                key = (d, lo, hi)
                uniq.setdefault(key, len(uniq) + 2)
                return uniq[key]
            mk([])
            print(f"ROBDD {name}: {len(uniq)} internal nodes (+2 terminals)")
        return
    trace = [] if "--trace" in args else None
    res = {}
    for name, order in (("sensors-first", SENSORS_FIRST), ("features-first", FEATURES_FIRST)):
        tr = trace if (trace is not None and name == "features-first") else None
        if tr is not None:
            tr.append(f"TRACE (features-first): {order}")
        res[name] = report(ECU, order, name, tr)
    a, b = (sorted(res[k][0]) for k in res)
    assert a == b, "orders disagree"
    print("\nValid configurations (canonical order ACC,BC,LKA,PA,RAD,CAM,US):")
    for i, s in enumerate(a, 1):
        cost = sum(ECU.cost[v] for v, x in zip(ECU.names, s) if x)
        print(f"  {i}. {''.join(map(str, s))}  {fmt_tuple(ECU, s)}  sensor cost = {cost}")
    if trace is not None:
        print("\n" + "\n".join(trace))


if __name__ == "__main__":
    main()
