"""
Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
Plotting script: Generates publication-ready running time plots from timing.csv.

Outputs:
  - results/timing_plot.png
  - results/timing_plot.pdf

Author: Vinothini (Roll No. 24I374)
"""

import csv
import math
import os
import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

def generate_plots(csv_path="results/timing.csv", output_prefix="results/timing_plot"):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist.")
        return

    out_dir = os.path.dirname(output_prefix)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    def get_series(algorithm, workload):
        points = []
        for r in rows:
            if r["algorithm"] == algorithm and r["workload"] == workload:
                points.append((int(r["n"]), float(r["median_ms"])))
        points.sort(key=lambda p: p[0])
        return [p[0] for p in points], [p[1] for p in points]

    # Palette & Typography styling
    BLUE = "#2a78d6"
    ORANGE = "#eb6834"
    AQUA = "#1baf7a"
    INK = "#0b0b0b"
    MUTED = "#52514e"
    GRID = "#e4e3df"
    SURFACE = "#fcfcfb"

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": GRID,
        "axes.facecolor": SURFACE,
        "figure.facecolor": SURFACE,
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED
    })

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13, 5.2))

    # Panel A: Small input sizes (n = 10 .. 30), both algorithms (log y)
    small_n = [10, 15, 20, 25, 30]
    gn, gt = get_series("greedy_dsu", "random")
    gn_small = [n for n in gn if n in small_n]
    gt_small = gt[:len(gn_small)]

    btn_rnd, btt_rnd = get_series("backtracking", "random")
    btn_same, btt_same = get_series("backtracking", "same_deadline")

    ax_a.plot(gn_small, gt_small, "-o", color=BLUE, lw=2, ms=6, mfc=SURFACE, mew=2, label="Greedy + DSU (random)")
    ax_a.plot(btn_rnd, btt_rnd, "-s", color=ORANGE, lw=2, ms=6, mfc=SURFACE, mew=2, label="Backtracking (random)")
    ax_a.plot(btn_same, btt_same, "--^", color=AQUA, lw=2, ms=7, mfc=SURFACE, mew=2, label="Backtracking (same deadline)")

    ax_a.set_yscale("log")
    ax_a.set_xticks(small_n)
    ax_a.set_xlabel("Number of jobs n")
    ax_a.set_ylabel("Running time (ms, log scale)")
    ax_a.set_title("A. Same inputs, both algorithms (n = 10 ... 30)", loc="left", fontsize=12, color=INK)

    if gt_small:
        ax_a.annotate(f"Greedy + DSU (random):\n{gt_small[-1]:.3f} ms at n = 30",
                      (30, gt_small[-1]), xytext=(11, 4e-2),
                      color=BLUE, fontsize=10, arrowprops=dict(arrowstyle="-", color=BLUE))
    if btt_rnd:
        ax_a.annotate(f"Backtracking, random\n{btt_rnd[-1]/1000.0:.1f} s at n = 30",
                      (30, btt_rnd[-1]), xytext=(11, 3e2),
                      color=ORANGE, fontsize=10, arrowprops=dict(arrowstyle="-", color=ORANGE))
    if btt_same:
        ax_a.annotate(f"Backtracking, worst case\n(all d = n): {btt_same[-1]/1000.0:.1f} s at n = 30",
                      (30, btt_same[-1]), xytext=(11, 3e3),
                      color=AQUA, fontsize=10, arrowprops=dict(arrowstyle="-", color=AQUA))

    ax_a.set_ylim(5e-4, 4e4)

    # Panel B: Greedy + DSU at scale (n = 10^3 .. 10^6), log-log
    for wl, col, mk, style in [("random", BLUE, "o", "-"), ("same_deadline", AQUA, "^", "--")]:
        n_vals, t_vals = get_series("greedy_dsu", wl)
        n_sub = [x for x in n_vals if x >= 1000]
        t_sub = t_vals[-len(n_sub):]
        ax_b.plot(n_sub, t_sub, style, marker=mk, color=col, lw=2, ms=6, mfc=SURFACE, mew=2, label=wl)

    n_all, t_all = get_series("greedy_dsu", "random")
    n_big = [x for x in n_all if x >= 1000]
    t_big = t_all[-len(n_big):]

    if n_big and t_big:
        c_ref = t_big[-1] / (n_big[-1] * math.log2(n_big[-1]))
        ax_b.plot(n_big, [c_ref * x * math.log2(x) for x in n_big], ":", color=MUTED, lw=1.5)

    ax_b.axhline(2000, color=ORANGE, lw=1.2, ls="-.")
    ax_b.text(1100, 2300, "2 s deadline limit", color=ORANGE, fontsize=10)

    ax_b.set_xscale("log")
    ax_b.set_yscale("log")
    ax_b.set_xlabel("Number of jobs n  (10^4 slots)")
    ax_b.set_ylabel("Running time (ms, log scale)")
    ax_b.set_title("B. Greedy + DSU scales to 10^6 jobs", loc="left", fontsize=12, color=INK)

    if t_big:
        ax_b.annotate(f"random: {t_big[-1]:.0f} ms at n = 10^6",
                      (1e6, t_big[-1]), xytext=(2e3, 25), color=BLUE, fontsize=10,
                      arrowprops=dict(arrowstyle="-", color=BLUE))

    sd_n, sd_t = get_series("greedy_dsu", "same_deadline")
    if sd_t:
        ax_b.annotate(f"same deadline (worst): {sd_t[-1]:.0f} ms",
                      (1e6, sd_t[-1]), xytext=(2e3, 6), color=AQUA, fontsize=10,
                      arrowprops=dict(arrowstyle="-", color=AQUA))

    ax_b.text(1.2e4, 0.18, "dotted: c * n log2 n reference", color=MUTED, fontsize=9)
    ax_b.set_ylim(0.03, 6000)

    for ax in (ax_a, ax_b):
        ax.grid(True, color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    fig.suptitle("Batch 18 - Running Time vs Input Size (Median of Repeated Runs)",
                 x=0.01, ha="left", fontsize=13, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    fig.savefig(output_prefix + ".png", dpi=200)
    fig.savefig(output_prefix + ".pdf")
    plt.close(fig)
    print(f"Generated plots: {output_prefix}.png and {output_prefix}.pdf")

if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "results/timing.csv"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "results/timing_plot"
    generate_plots(csv_file, out_file)
