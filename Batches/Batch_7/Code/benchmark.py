"""Produces results/timing.csv, timing_scale.csv, worst_case.csv, ordering.csv, timing_plot.png"""
import csv, time, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from generate_inputs import random_graph, mycielski_k
from main_solution import min_slots, colour
from rejected_alternative import chromatic_dp

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
def ms(f, reps=1):
    t = time.perf_counter()
    for _ in range(reps): out = f()
    return (time.perf_counter() - t) * 1000 / reps, out

# 1. chosen (backtracking) vs rejected (subset DP): minimum slots, same graphs
rows = []
for n in (6, 8, 10, 12, 14, 16):
    g = random_graph(n, 0.3, seed=1)
    tc, (kc, _) = ms(lambda: min_slots(g), reps=20)
    tr, kr = ms(lambda: chromatic_dp(g))
    assert kc == kr
    rows.append((n, round(tc, 3), round(tr, 3), kc))
with open(f"{R}/timing.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["n", "time_chosen_ms", "time_rejected_ms", "min_slots"]); w.writerows(rows)

# 2. scale of the chosen algorithm: feasibility in 9 colours (days) up to the real size 420
scale = []
for n in (50, 100, 150, 200, 300, 420):
    g = random_graph(n, 0.05, seed=7)
    t, (c, st) = ms(lambda: colour(g, 9), reps=3)
    assert c is not None
    scale.append((n, round(t, 2), st["nodes"]))
with open(f"{R}/timing_scale.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["n", "time_chosen_ms", "nodes"]); w.writerows(scale)

# 3. worst case: Mycielski graphs (clique number 2, chromatic number k) asked for k-1 slots -> NO instance
wc = []
for k in (4, 5, 6):
    g = mycielski_k(k)
    for order in ("mrv", "input"):
        t, (c, st) = ms(lambda: colour(g, k - 1, order=order, node_limit=3_000_000))
        wc.append((k, len(g), k - 1, order, st["nodes"], "aborted" if st.get("aborted") else "infeasible-proved", round(t, 1)))
with open(f"{R}/worst_case.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["chromatic_k", "n", "slots_asked", "ordering", "nodes", "result", "time_ms"]); w.writerows(wc)

# 4. ordering effect with the Q5 rules (pinned course + day rule), random hard-ish graphs
od = []
for n, p, days in ((30, 0.25, 5), (40, 0.2, 5), (50, 0.2, 6)):
    for seed in range(1, 6):
        g = random_graph(n, p, seed)
        for order in ("input", "mrv"):
            c, st = colour(g, days, allowed={0: [0]}, order=order, node_limit=2_000_000)
            od.append((n, p, days, seed, order, st["nodes"], "feasible" if c else ("aborted" if st.get("aborted") else "infeasible")))
with open(f"{R}/ordering.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["n", "p", "days", "seed", "ordering", "nodes", "result"]); w.writerows(od)

# plot
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ns = [r[0] for r in rows]
ax[0].semilogy(ns, [r[1] for r in rows], "o-", label="Backtracking (chosen)")
ax[0].semilogy(ns, [r[2] for r in rows], "s-", label="Subset DP (rejected)")
ax[0].set_xlabel("n (courses)"); ax[0].set_ylabel("time (ms, log)"); ax[0].set_title("Minimum slots: chosen vs rejected"); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].plot([r[0] for r in scale], [r[1] for r in scale], "o-")
ax[1].set_xlabel("n (courses)"); ax[1].set_ylabel("time (ms)"); ax[1].set_title("Chosen algorithm, feasibility in 9 days, up to n=420"); ax[1].grid(alpha=.3)
plt.tight_layout(); plt.savefig(f"{R}/timing_plot.png", dpi=150)
print("done")
