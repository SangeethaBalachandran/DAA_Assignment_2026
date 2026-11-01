"""Constrained pairwise (2-way) test-suite generation for binary feature models.

Part A: the REAL 7-feature ECU (all 19 valid configs enumerated; pairs checked exactly).
Part B: an ILLUSTRATIVE SYNTHETIC 200-feature product line (F001..F200, seeded). These are
        NOT real automotive features; they only demonstrate scale. Constraints are binary
        (requires / excludes / at-least-one-of-two) = a 2-CNF, so the feasibility of a pair of
        settings is decided exactly by implication propagation (see report, Sec. 11).
Greedy algorithm: repeatedly build one valid test that covers as many still-uncovered feasible
pairs as possible (AETG-style), until no feasible pair is uncovered.
"""
import itertools, random, sys, time
from main_solution import ECU, enumerate_valid, FEATURES_FIRST


# ---------------------------------------------------------------- 2-CNF model
class Model:
    def __init__(self, n, requires, excludes, atleast):
        self.n = n
        self.imp = [[] for _ in range(2 * n)]       # literal id = 2*i + value
        L = lambda i, v: 2 * i + v
        for a, b in requires:                       # a=1 -> b=1 ; b=0 -> a=0
            self.imp[L(a, 1)].append(L(b, 1)); self.imp[L(b, 0)].append(L(a, 0))
        for a, b in excludes:                       # a=1 -> b=0 ; b=1 -> a=0
            self.imp[L(a, 1)].append(L(b, 0)); self.imp[L(b, 1)].append(L(a, 0))
        for a, b in atleast:                        # a=0 -> b=1 ; b=0 -> a=1
            self.imp[L(a, 0)].append(L(b, 1)); self.imp[L(b, 0)].append(L(a, 1))
        self.requires, self.excludes, self.atleast = requires, excludes, atleast

    def assign(self, asg, lits):
        """Set literals and propagate implications. Returns new dict or None on conflict."""
        asg = dict(asg); stack = list(lits)
        while stack:
            l = stack.pop(); i, v = divmod(l, 2)
            if i in asg:
                if asg[i] != v: return None
                continue
            asg[i] = v
            stack.extend(self.imp[l])
        return asg

    def valid(self, cfg):
        return (all(not cfg[a] or cfg[b] for a, b in self.requires)
                and all(not (cfg[a] and cfg[b]) for a, b in self.excludes)
                and all(cfg[a] or cfg[b] for a, b in self.atleast))


def synthetic_model(n=200, seed=14):
    rng = random.Random(seed)
    planted = [rng.randint(0, 1) for _ in range(n)]          # guarantees satisfiability
    ones = [i for i in range(n) if planted[i]]; zeros = [i for i in range(n) if not planted[i]]
    requires = set(); excludes = set(); atleast = set()
    while len(requires) < int(0.6 * n):
        a = rng.randrange(n); b = rng.randrange(n)
        if a != b and not (planted[a] and not planted[b]): requires.add((a, b))
    while len(excludes) < n // 4:
        a, b = rng.sample(range(n), 2)
        if not (planted[a] and planted[b]): excludes.add((a, b))
    while len(atleast) < n // 20 + 1:
        a, b = rng.sample(range(n), 2)
        if planted[a] or planted[b]: atleast.add((a, b))
    return Model(n, sorted(requires), sorted(excludes), sorted(atleast))


# ---------------------------------------------------------------- feasibility + greedy
def feasible_pairs(m):
    """All (i,vi,j,vj), i<j, that are extendable to a valid configuration."""
    base = m.assign({}, [])
    out = set()
    for i, j in itertools.combinations(range(m.n), 2):
        for vi in (0, 1):
            a = m.assign(base, [2 * i + vi])
            if a is None: continue
            for vj in (0, 1):
                if m.assign(a, [2 * j + vj]) is not None:
                    out.add((i, vi, j, vj))
    return out


def greedy_suite(m, feas, seed=1):
    rng = random.Random(seed)
    unc = set(feas); suite = []
    while unc:
        i, vi, j, vj = next(iter(sorted(unc)))              # deterministic seed pair
        asg = m.assign({}, [2 * i + vi, 2 * j + vj])
        assert asg is not None
        order = list(range(m.n)); rng.shuffle(order)
        for x in order:
            if x in asg: continue
            best = None
            for v in (0, 1):
                trial = m.assign(asg, [2 * x + v])
                if trial is None: continue
                gain = sum(1 for y, w in asg.items()
                           if ((min(x, y), v if x < y else w, max(x, y), w if x < y else v) in unc))
                if best is None or gain > best[0]: best = (gain, v, trial)
            asg = best[2]                                   # one of the two values always works
        cfg = [asg[k] for k in range(m.n)]
        assert m.valid(cfg)
        suite.append(cfg)
        for a, b in itertools.combinations(range(m.n), 2):
            unc.discard((a, cfg[a], b, cfg[b]))
    return suite


def covered_pairs(suite):
    n = len(suite[0]); cov = set()
    for cfg in suite:
        for a, b in itertools.combinations(range(n), 2):
            cov.add((a, cfg[a], b, cfg[b]))
    return cov


def main():
    # ---------------- Part A: real ECU
    sols, _ = enumerate_valid(ECU, FEATURES_FIRST)
    n = 7
    feas = {(a, cfg[a], b, cfg[b]) for cfg in sols for a, b in itertools.combinations(range(n), 2)}
    allp = 4 * n * (n - 1) // 2
    print(f"PART A - real ECU (7 features): total pairs {allp}, feasible {len(feas)}, infeasible {allp - len(feas)}")
    # greedy over the 19 valid configs (set cover)
    unc, suite = set(feas), []
    while unc:
        cfg = max(sols, key=lambda c: len({(a, c[a], b, c[b]) for a, b in itertools.combinations(range(n), 2)} & unc))
        suite.append(cfg)
        unc -= {(a, cfg[a], b, cfg[b]) for a, b in itertools.combinations(range(n), 2)}
    assert covered_pairs(suite) >= feas
    print(f"  pairwise suite size = {len(suite)} (vs {len(sols)} valid, 128 total); coverage verified")
    print(f"  columns {ECU.names}")
    for c in suite: print("   ", ''.join(map(str, c)), "{" + ", ".join(v for v, x in zip(ECU.names, c) if x) + "}")
    # ---------------- self-test of propagation-based feasibility vs brute force (small synthetic)
    small = synthetic_model(12, seed=3)
    brute = set()
    for bits in itertools.product((0, 1), repeat=12):
        if small.valid(bits):
            brute |= {(a, bits[a], b, bits[b]) for a, b in itertools.combinations(range(12), 2)}
    assert brute == feasible_pairs(small)
    print(f"\nSELF-TEST: propagation feasibility == brute force on 12-feature synthetic model ({len(brute)} feasible pairs)")
    # ---------------- Part B: 200 synthetic features
    m = synthetic_model(200)
    t = time.perf_counter(); feas = feasible_pairs(m); t1 = time.perf_counter() - t
    t = time.perf_counter(); suite = greedy_suite(m, feas); t2 = time.perf_counter() - t
    allp = 4 * 200 * 199 // 2
    cov = covered_pairs(suite)
    assert feas <= cov and all(m.valid(c) for c in suite)
    # a pair that is covered but infeasible would be impossible, check:
    assert cov <= feas
    print(f"\nPART B - ILLUSTRATIVE SYNTHETIC 200 binary features F001..F200 (not real ECU features)")
    print(f"  constraints: {len(m.requires)} requires, {len(m.excludes)} excludes, {len(m.atleast)} at-least-one")
    print(f"  pair-settings total {allp}, feasible {len(feas)}, infeasible {allp - len(feas)}")
    print(f"  suite size = {len(suite)} tests; every feasible pair covered: {feas <= cov}; all tests valid: True")
    print(f"  uncovered feasible pairs = {len(feas - cov)}; time: feasibility {t1:.2f}s, generation {t2:.2f}s")
    print(f"  (listing all configurations is impossible; exhaustive would need up to 2^200 ~ {2 ** 200:.2e})")
    if "--dump" in sys.argv:
        for c in suite: print(''.join(map(str, c)))


if __name__ == "__main__":
    main()
