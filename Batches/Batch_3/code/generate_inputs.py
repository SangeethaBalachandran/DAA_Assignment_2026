import csv
import os
import random
import time
import statistics


def generate_input(n, seed=42):
    rng = random.Random(seed + n)
    return [rng.randint(10, 100) for _ in range(n + 1)]


# Dynamic Programming approach
def dp_solution(p):
    n = len(p) - 1
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")

            for k in range(i, j):
                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + p[i] * p[k + 1] * p[j + 1]
                )

                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]


# Greedy approach
def greedy_solution(p):
    dimensions = [
        (p[i], p[i + 1]) for i in range(len(p) - 1)
    ]

    total_cost = 0

    while len(dimensions) > 1:
        costs = []

        for i in range(len(dimensions) - 1):
            cost = (
                dimensions[i][0]
                * dimensions[i][1]
                * dimensions[i + 1][1]
            )
            costs.append((cost, i))

        minimum_cost, index = min(costs)
        total_cost += minimum_cost

        merged = (
            dimensions[index][0],
            dimensions[index + 1][1]
        )

        dimensions[index:index + 2] = [merged]

    return total_cost


def benchmark():
    input_sizes = [5, 10, 15, 20, 25]
    repeats = 5

    results_dir = os.path.join(
        os.path.dirname(__file__), "..", "results"
    )
    os.makedirs(results_dir, exist_ok=True)

    csv_path = os.path.join(results_dir, "timing.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "relations",
            "dp_median_seconds",
            "greedy_median_seconds",
            "repeats",
            "dp_cost",
            "greedy_cost"
        ])

        for n in input_sizes:
            dimensions = generate_input(n)

            dp_times = []
            greedy_times = []

            dp_cost = dp_solution(dimensions)
            greedy_cost = greedy_solution(dimensions)

            for _ in range(repeats):
                start = time.perf_counter()
                dp_solution(dimensions)
                dp_times.append(time.perf_counter() - start)

                start = time.perf_counter()
                greedy_solution(dimensions)
                greedy_times.append(time.perf_counter() - start)

            dp_median = statistics.median(dp_times)
            greedy_median = statistics.median(greedy_times)

            writer.writerow([
                n,
                dp_median,
                greedy_median,
                repeats,
                dp_cost,
                greedy_cost
            ])

            print(f"Relations: {n}")
            print(f"Dimensions: {dimensions}")
            print(f"DP Cost: {dp_cost}")
            print(f"Greedy Cost: {greedy_cost}")
            print(f"DP Time: {dp_median:.8f} seconds")
            print(f"Greedy Time: {greedy_median:.8f} seconds")
            print("-" * 40)

    print("Benchmark completed!")
    print("CSV saved at:", os.path.abspath(csv_path))


if __name__ == "__main__":
    benchmark()
