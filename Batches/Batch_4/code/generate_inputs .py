import argparse
import random


def generate(mode, n, seed=1):
    
    if mode == "instance":
        from main_solution import INSTANCE
        return list(INSTANCE.values())
    if mode == "worst":
        return [(i + 1, (n - i) / 1000.0) for i in range(n)]
    rnd = random.Random(seed)
    if mode == "uniform":
        return [(rnd.randint(500, 20000), round(rnd.uniform(0.1, 15.0), 3)) for _ in range(n)]
    if mode == "anti":
        pts = []
        for _ in range(n):
            t = rnd.random()
            u = min(1.0, max(0.0, t + rnd.gauss(0, 0.08)))
            v = min(1.0, max(0.0, (1 - t) + rnd.gauss(0, 0.08)))
            pts.append((500 + int(19500 * u), round(0.1 + 14.9 * v, 3)))
        return pts
    raise ValueError(mode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="anti", choices=["uniform", "anti", "worst", "instance"])
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default=None)
    ap.add_argument("--rating", action="store_true", help="append a rating column (1.0-5.0)")
    a = ap.parse_args()
    pts = generate(a.mode, a.n, a.seed)
    rnd = random.Random(a.seed + 7)
    f = open(a.out, "w") if a.out else None
    out = f if f else __import__("sys").stdout
    out.write("price,distance" + (",rating" if a.rating else "") + "\n")
    for p in pts:
        out.write("%g,%g" % p + (",%.1f" % rnd.uniform(1, 5) if a.rating else "") + "\n")
    if f:
        f.close()
        print("wrote %d rows to %s" % (len(pts), a.out))


if __name__ == "__main__":
    main()
