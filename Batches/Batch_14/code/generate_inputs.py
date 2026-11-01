"""Reproducible synthetic product-line instances for benchmarking (seeded).
n = 7 returns the REAL 7-feature ECU instance. n > 7 returns SYNTHETIC instances
(not real automotive features) generated with random.Random(1000 + n)."""
import random
from main_solution import Instance, ECU


def make_instance(n):
    if n == 7:
        return ECU
    rng = random.Random(1000 + n)
    k = max(3, n // 3)                       # number of sensors
    names = [f"F{i:02d}" for i in range(n - k)] + [f"S{i:02d}" for i in range(k)]
    sensors, feats = names[n - k:], names[:n - k]
    cost = {s: rng.choice([5000, 8000, 12000]) for s in sensors}
    requires = [(f, rng.choice(sensors)) for f in feats if rng.random() < 0.7]
    excludes = [tuple(rng.sample(feats, 2)) for _ in range(max(1, len(feats) // 3))]
    atleast = [tuple(rng.sample(feats, 2))]
    budget = int(sum(cost.values()) * 0.6)
    # shuffle variable order of the instance so neither algorithm is helped by layout
    rng.shuffle(names)
    return Instance(names, cost, requires, excludes, atleast, budget)


if __name__ == "__main__":
    for n in (7, 9, 11, 13, 15):
        i = make_instance(n)
        print(n, len(i.requires), len(i.excludes), i.atleast, i.budget)
