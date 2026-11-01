
"""Generate deterministic benchmark inputs and timing results.

Run from Batch_11/:
    python code/generate_inputs.py
    python code/generate_inputs.py --sizes 100 250 500 1000 2000 --width 16

This script creates word sequences, measures the chosen and rejected methods,
and writes results/timing.csv and results/timing_plot.png.
"""
import argparse
import csv
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from main_solution import word_wrap
from rejected_alternative import greedy_layout

WORDS = [
    "a", "of", "to", "is", "the", "book", "line", "text",
    "clear", "model", "reader", "layout", "problem", "answer"
]

def median_time(function, words, width, repeats=3):
    measurements = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        function(words, width)
        measurements.append((time.perf_counter_ns() - start) / 1_000_000)
    return statistics.median(measurements)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int,
                        default=[100, 250, 500, 1000, 2000])
    parser.add_argument("--width", type=int, default=16)
    parser.add_argument("--seed", type=int, default=11)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    rows = []

    for n in args.sizes:
        # Deterministic generated input used by both implementations.
        words = [rng.choice(WORDS) for _ in range(n)]
        chosen_ms = median_time(word_wrap, words, args.width)
        rejected_ms = median_time(greedy_layout, words, args.width)
        rows.append((n, chosen_ms, rejected_ms))
        print(f"n={n}: chosen={chosen_ms:.6f} ms; rejected={rejected_ms:.6f} ms")

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    with (results_dir / "timing.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "time_chosen_ms", "time_rejected_ms"])
        for n, chosen, rejected in rows:
            writer.writerow([n, f"{chosen:.6f}", f"{rejected:.6f}"])

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot([r[0] for r in rows], [r[1] for r in rows],
             marker="o", label="Chosen: Dynamic Programming")
    plt.plot([r[0] for r in rows], [r[2] for r in rows],
             marker="s", label="Rejected: Greedy")
    plt.xlabel("Number of words (n)")
    plt.ylabel("Median execution time (ms)")
    plt.title(f"Paragraph layout benchmark (W={args.width})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(results_dir / "timing_plot.png", dpi=160)
    plt.close()

if __name__ == "__main__":
    main()
