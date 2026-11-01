"""Benchmark: backtracking vs exhaustive enumeration. Writes ../results/timing.csv and timing_plot.png."""
import csv, os, statistics, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from generate_inputs import make_instance
from main_solution import enumerate_valid
from rejected_alternative import exhaustive

SIZES = [7, 9, 11, 13, 15, 17, 19, 21]
REPEATS = 5
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def best_median(fn):
    ts = []
    for _ in range(REPEATS):
        t = time.perf_counter(); r = fn(); ts.append((time.perf_counter() - t) * 1000)
    return statistics.median(ts), r


rows = []
for n in SIZES:
    inst = make_instance(n)
    order = list(inst.names)                 # features/instance order for backtracking
    tb, (sols, st) = best_median(lambda: enumerate_valid(inst, order))
    te, (ex, checked) = best_median(lambda: exhaustive(inst))
    assert sorted(sols) == sorted(ex), f"mismatch at n={n}"
    rows.append([n, round(tb, 3), round(te, 3), st["solutions"], st["calls"], st["tried"], checked])
    print(rows[-1])

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "timing.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["n", "time_chosen_ms", "time_rejected_ms", "valid_configs",
                "bt_recursive_calls", "bt_assignments_examined", "exhaustive_configs_checked"])
    w.writerows(rows)

ns = [r[0] for r in rows]
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].plot(ns, [r[1] for r in rows], "o-", label="Backtracking (chosen)")
ax[0].plot(ns, [r[2] for r in rows], "s-", label="Exhaustive 2^n (rejected)")
ax[0].set_yscale("log"); ax[0].set_xlabel("number of features n"); ax[0].set_ylabel("median time (ms, log)")
ax[0].set_title("Running time vs n"); ax[0].legend(); ax[0].grid(True, which="both", alpha=.3)
ax[1].plot(ns, [r[5] for r in rows], "o-", label="BT assignments examined")
ax[1].plot(ns, [r[6] for r in rows], "s-", label="Exhaustive configs checked (2^n)")
ax[1].plot(ns, [r[3] for r in rows], "^-", label="Valid configurations")
ax[1].set_yscale("log"); ax[1].set_xlabel("number of features n"); ax[1].set_ylabel("count (log)")
ax[1].set_title("Search effort vs n"); ax[1].legend(); ax[1].grid(True, which="both", alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "timing_plot.png"), dpi=150)
print("wrote results")

try:
    import update_docs
    rows_ = update_docs.load(); update_docs.update_readme(rows_); update_docs.update_script(rows_); update_docs.update_slides(rows_)
except Exception as e:
    print("doc update skipped:", e)
