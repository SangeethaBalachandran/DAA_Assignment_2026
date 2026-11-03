import bisect
import sys

INF = float("inf")

def _cut(sr, m):
    
    return bisect.bisect_right(sr, -m, key=lambda p: -p[1])


def dc_skyline(pts, lo, hi, names=None, trace=None, depth=0):
    
    if hi - lo == 1:                                   
        return [pts[lo]]
    mid = (lo + hi) // 2                               
    sl = dc_skyline(pts, lo, mid, names, trace, depth + 1)   
    sr = dc_skyline(pts, mid, hi, names, trace, depth + 1)
    m = sl[-1][1]                                      
    cut = _cut(sr, m)                                  
    out = sl + sr[cut:]
    if trace is not None:
        f = (lambda L: "[" + ", ".join(names[p] for p in L) + "]") if names else str
        dropped = f(sr[:cut]) if cut else "[]"
        trace.append("%smerge SL=%s | SR=%s  m=%.1f  dropped=%s  -> %s"
                     % ("  " * depth, f(sl), f(sr), m, dropped, f(out)))
    return out


def _sorted_unique(points):
    pts = sorted(points)
    return [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]


def skyline(points, names=None, trace=None):
    pts = _sorted_unique(points)
    if not pts:
        return []
    return dc_skyline(pts, 0, len(pts), names, trace)


def sharded_skyline(points, k=16, timed=False, trace=None, names=None, bounds=None):
   
    import time
    t0 = time.perf_counter()
    if not points:
        return ([], 0.0, [], 0.0) if timed else []
    if bounds is None:
        pmin = min(p[0] for p in points)
        pmax = max(p[0] for p in points)
        w = (pmax - pmin) / k or 1.0
        bounds = [pmin + w * i for i in range(1, k)]          
    shards = [[] for _ in range(len(bounds) + 1)]
    for p in points:                                           
        shards[bisect.bisect_right(bounds, p[0])].append(p)
    t_part = time.perf_counter() - t0

    local, t_shard = [], []
    for j, sh in enumerate(shards):                            
        t1 = time.perf_counter()
        L = skyline(sh, names) if sh else []
        t_shard.append(time.perf_counter() - t1)
        local.append(L)
        if trace is not None:
            f = (lambda L_: "[" + ", ".join(names[p] for p in L_) + "]") if names else str
            trace.append("shard %d (price %s): local skyline %s" % (j, _range(bounds, j), f(L)))

    t2 = time.perf_counter()
    result, m = [], INF
    for j, L in enumerate(local):
        if not L:
            continue
        cut = _cut(L, m)
        kept = L[cut:]
        result += kept
        if trace is not None:
            f = (lambda L_: "[" + ", ".join(names[p] for p in L_) + "]") if names else str
            trace.append("combine shard %d: m_in=%s  keep %s  drop %s"
                         % (j, "inf" if m == INF else "%.1f" % m, f(kept), f(L[:cut])))
        m = min(m, L[-1][1])
    t_merge = time.perf_counter() - t2
    return (result, t_part, t_shard, t_merge) if timed else result


def _range(bounds, j):
    lo = "-inf" if j == 0 else "%g" % bounds[j - 1]
    hi = "+inf" if j == len(bounds) else "%g" % bounds[j]
    return "[%s, %s)" % (lo, hi)


def brute_force(points):
    pts = set(points)
    return sorted(g for g in pts
                  if not any(h != g and h[0] <= g[0] and h[1] <= g[1] for h in pts))


def _dc3(pts, lo, hi):
    
    if hi - lo == 1:
        return [pts[lo]]
    mid = (lo + hi) // 2
    sl = _dc3(pts, lo, mid)
    sr = _dc3(pts, mid, hi)
    out, i, j, best = [], 0, 0, -INF       
    while i < len(sl) or j < len(sr):
        take_left = j == len(sr) or (i < len(sl) and sl[i][1] <= sr[j][1])   
        if take_left:
            best = max(best, sl[i][2])
            out.append(sl[i]); i += 1
        else:
            if sr[j][2] > best:           
                out.append(sr[j])
            j += 1
    return out


def dc_skyline_3d(points):
    pts = sorted(set(points), key=lambda p: (p[0], p[1], -p[2]))
    if not pts:
        return []
    return sorted(_dc3(pts, 0, len(pts)))


def brute_force_3d(points):
    pts = set(points)
    def dom(h, g):
        return h != g and h[0] <= g[0] and h[1] <= g[1] and h[2] >= g[2]
    return sorted(g for g in pts if not any(dom(h, g) for h in pts))



INSTANCE = {"H1": (4200, 1.9), "H2": (3100, 2.5), "H3": (5600, 0.4), "H4": (2800, 4.0),
            "H5": (3900, 1.8), "H6": (2500, 5.5), "H7": (4600, 0.9), "H8": (3300, 2.8),
            "H9": (6100, 0.3), "H10": (3000, 4.2)}


def read_csv(path):
    pts = []
    with open(path) as f:
        next(f)
        for line in f:
            a = line.strip().split(",")
            pts.append(tuple(float(x) for x in a))
    return pts


def _instance():
    names = {v: k for k, v in INSTANCE.items()}
    pts = list(INSTANCE.values())
    print("Sorted by (price, dist):", [names[p] for p in sorted(pts)])
    print("\n--- Recursive divide and conquer (split index = (lo+hi)//2) ---")
    tr = []
    res = skyline(pts, names, tr)
    print("\n".join(tr))
    print("ANSWER:", [names[p] for p in res])
    print("Dominated:", sorted((names[p] for p in pts if p not in res), key=lambda s: int(s[1:])))
    print("\n--- Same instance, 3 price shards: <3200 | 3200-4500 | >=4500 (Q3 illustration) ---")
    tr = []
    res2 = sharded_skyline(pts, trace=tr, names=names, bounds=[3200, 4500])
    print("\n".join(tr))
    print("ANSWER:", [names[p] for p in res2])
    assert res == res2 == sorted(res2) == brute_force(pts)


def _selftest():
    import random
    rnd = random.Random(1)
    for trial in range(3000):
        n = rnd.randint(0, 40)
        pts = [(rnd.randint(1, 12), rnd.randint(1, 12)) for _ in range(n)]   # many ties/duplicates
        assert skyline(pts) == brute_force(pts), pts
        for k in (1, 2, 3, 16):
            assert sorted(sharded_skyline(pts, k)) == brute_force(pts), (k, pts)
        p3 = [(rnd.randint(1, 8), rnd.randint(1, 8), rnd.randint(1, 8)) for _ in range(n)]
        assert dc_skyline_3d(p3) == brute_force_3d(p3), p3
    
    for _ in range(200):
        pts = [(rnd.random(), rnd.random()) for _ in range(200)]
        s = skyline(pts)
        assert all(a[0] < b[0] and a[1] > b[1] for a, b in zip(s, s[1:]))
    print("selftest passed: 3000 random 2-D and 3-D cases agree with the O(n^2) oracle")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--instance" in a:
        _instance()
    elif "--selftest" in a:
        _selftest()
    elif "--input" in a:
        pts = read_csv(a[a.index("--input") + 1])
        s = sharded_skyline([p[:2] for p in pts])
        print("n=%d  skyline size=%d" % (len(pts), len(s)))
        for p in s[:20]:
            print("%g,%g" % p)
    else:
        print(__doc__)
