import csv
import time
from pathlib import Path

import matplotlib.pyplot as plt

from main_solution import min_charging_stops
from rejected_alternative import dp_min_stops

# Paths relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = RESULTS_DIR / "timing.csv"
PLOT_FILE = RESULTS_DIR / "timing_plot.png"

# Six input sizes: more than the required minimum of five
SIZES = [100, 250, 500, 1000, 2000, 3000]

rows = []

for n in SIZES:
    # Generate equally spaced charging stations
    chargers = [60 * (i + 1) for i in range(n)]
    destination = chargers[-1] + 60
    range_km = 120

    # Verify that both algorithms find the same minimum stop count
    chosen_result = min_charging_stops(
        chargers, destination, range_km
    )
    rejected_result = dp_min_stops(
        chargers, destination, range_km
    )

    if chosen_result is None or rejected_result is None:
        raise RuntimeError(f"No valid route for input size {n}")

    if len(chosen_result) != len(rejected_result):
        raise RuntimeError(
            f"Algorithms disagree for input size {n}"
        )

    # Measure average execution time over three runs
    chosen_times = []
    rejected_times = []

    for _ in range(3):
        start = time.perf_counter()
        min_charging_stops(chargers, destination, range_km)
        chosen_times.append(
            (time.perf_counter() - start) * 1000
        )

        start = time.perf_counter()
        dp_min_stops(chargers, destination, range_km)
        rejected_times.append(
            (time.perf_counter() - start) * 1000
        )

    chosen_ms = sum(chosen_times) / len(chosen_times)
    rejected_ms = sum(rejected_times) / len(rejected_times)

    rows.append([
        n,
        round(chosen_ms, 6),
        round(rejected_ms, 6)
    ])

    print(
        f"n={n}: Greedy={chosen_ms:.6f} ms, "
        f"DP={rejected_ms:.6f} ms"
    )

# Save CSV with the exact required column names
with CSV_FILE.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "n",
        "time_chosen_ms",
        "time_rejected_ms"
    ])
    writer.writerows(rows)

# Generate the timing graph from measured results
sizes = [row[0] for row in rows]
chosen_times = [row[1] for row in rows]
rejected_times = [row[2] for row in rows]

plt.figure(figsize=(9, 5))
plt.plot(sizes, chosen_times, marker="o", label="Chosen: Greedy")
plt.plot(sizes, rejected_times, marker="s", label="Rejected: DP")

plt.xlabel("Number of charging stations (n)")
plt.ylabel("Average execution time (ms)")
plt.title("Greedy vs Dynamic Programming: Benchmark")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=200)
plt.close()

print(f"\nCSV saved to: {CSV_FILE}")
print(f"Graph saved to: {PLOT_FILE}")