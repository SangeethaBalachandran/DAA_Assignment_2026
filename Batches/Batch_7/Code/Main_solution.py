"""Chosen technique: BACKTRACKING with forward checking + most-constrained-first ordering.
Problem: can the courses be assigned to k slots so that conflicting courses never share
a slot (and, optionally, never share a DAY)?  Also min_slots() = smallest feasible k.
"""
import sys
from generate_inputs import COURSES, instance7

sys.setrecursionlimit(20000)

# ---------------------------------------------------------------- plain trace (Q2)
def plain_backtracking_trace(names, adj, k, order=None):
    """Static order, checks only already-assigned neighbours. Prints every rejection."""
    n = len(adj); order = order or list(range(n)); slot = {}
    rejected = []
    def rec(i):
        if i == n: return True
        v = order[i]
        for s in range(1, k + 1):
            clash = [names[u] for u in adj[v] if slot.get(u) == s]
            if clash:
                rejected.append((names[v], s, clash)); continue
            slot[v] = s
            if rec(i + 1): return True
            del slot[v]
            rejected.append((names[v], s, ["(subtree failed)"]))
        return False
    ok = rec(0)
    return ok, {names[v]: s for v, s in slot.items()}, rejected

# ---------------------------------------------------------------- main solver
def colour(adj, k, allowed=None, order="mrv", symmetry=None, node_limit=None):
    """Colour vertices with colours 0..k-1 so adjacent vertices differ.
    allowed[v] = iterable of permitted colours (unary constraints, e.g. Maths pinned).
    order = 'mrv' (smallest domain first, tie -> highest degree) or 'input'.
    Returns (colouring or None, stats)."""
    n = len(adj)
    full = (1 << k) - 1
    dom0 = [full] * n
    if allowed:
        for v, cs in allowed.items():
            dom0[v] = sum(1 << c for c in cs if c < k)
    if symmetry is None:
        symmetry = not allowed          # colour-permutation symmetry only if nothing is pinned
    stats = {"nodes": 0, "backtracks": 0}
    col = [-1] * n
    deg = [len(a) for a in adj]

    class Abort(Exception): pass

    def pick(dom):
        best = None
        for v in range(n):
            if col[v] != -1: continue
            if order == "input": return v
            key = (bin(dom[v]).count("1"), -deg[v])
            if best is None or key < best[0]: best = (key, v)
        return best[1]

    def rec(dom, done, maxc):
        if done == n: return True
        v = pick(dom)
        d = dom[v]
        for c in range(k):
            if not (d >> c) & 1: continue
            if symmetry and c > maxc + 1: break
            stats["nodes"] += 1
            if node_limit and stats["nodes"] > node_limit: raise Abort
            nd = dom[:]; nd[v] = 1 << c; ok = True
            for u in adj[v]:
                if col[u] == -1:
                    nd[u] &= ~(1 << c)
                    if nd[u] == 0: ok = False; break
            if ok:
                col[v] = c
                if rec(nd, done + 1, max(maxc, c)): return True
                col[v] = -1
            stats["backtracks"] += 1
        return False

    try:
        found = rec(dom0, 0, -1)
    except Abort:
        stats["aborted"] = True
        return None, stats
    return (col[:] if found else None), stats

def clique_lower_bound(adj):
    """Greedy clique: any clique of size q forces >= q slots."""
    best = 1
    for s in range(len(adj)):
        cl = [s]; cand = set(adj[s])
        while cand:
            v = max(cand, key=lambda x: len(adj[x] & cand))
            cl.append(v); cand &= adj[v]
        best = max(best, len(cl))
    return best

def min_slots(adj, node_limit=None):
    """Smallest k such that colour(adj,k) succeeds (iterates k from the clique bound)."""
    k = clique_lower_bound(adj); total = 0
    while True:
        c, st = colour(adj, k, node_limit=node_limit); total += st["nodes"]
        if st.get("aborted"): return None, total
        if c is not None: return k, total
        k += 1

# ---------------------------------------------------------------- Q5: Maths pinned + one exam/day
def timetable(names, adj, days, slots_per_day=2, pinned=None, order="mrv"):
    """Encode (a) pinned course -> fixed slot, (b) no two conflicting courses on the same DAY.
    Rule (b) means conflicting courses need different DAYS, so we colour with DAYS
    (domain of a pinned course = {day of its slot}); the slot inside a day is chosen after."""
    pinned = pinned or {}
    day_of = lambda s: (s - 1) // slots_per_day
    allowed = {names.index(c): [day_of(s)] for c, s in pinned.items()}
    colr, st = colour(adj, days, allowed=allowed or None, order=order)
    if colr is None: return None, st
    load = {}; out = {}
    for v in range(len(adj)):
        d = colr[v]
        if names[v] in pinned: s = pinned[names[v]]
        else:
            opts = [d * slots_per_day + j + 1 for j in range(slots_per_day)]
            s = min(opts, key=lambda x: load.get(x, 0))      # balance the two slots of a day
        load[s] = load.get(s, 0) + 1; out[names[v]] = s
    return out, st

if __name__ == "__main__":
    adj = instance7()
    print("== Q2: plain backtracking, listed order, k=3 slots ==")
    ok, sol, rej = plain_backtracking_trace(COURSES, adj, 3)
    for c, s, why in rej: print(f"  reject {c} -> slot {s}  (conflicts with {', '.join(why)})")
    print("  valid:", ok, sol)
    print("== min slots (no extra rules) ==", min_slots(adj))
    print("== Q5: Maths in slot 1 + one exam/day (2 slots/day) ==")
    for days in (2, 3):
        for od in ("input", "mrv"):
            t, st = timetable(COURSES, adj, days, 2, {"Maths": 1}, od)
            print(f"  days={days} ({days*2} slots) order={od:5s} -> {t}  nodes={st['nodes']} backtracks={st['backtracks']}")
