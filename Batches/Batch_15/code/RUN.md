# How to Run the Code

## Requirements

- Python 3.8+
- `matplotlib` (for generating benchmark plots)

Install the plotting dependency:

```bash
pip install matplotlib
```

## Running the Components

Run all commands from the `Batches/Batch_15` directory.

### 1. Run the Main Solution (Branch & Bound)

```bash
python code/main_solution.py
```

Finds the exact optimal VM packing for the Batch 15 instance `[9, 8, 7, 6, 5, 4, 3, 2]` with server capacity `C = 16` vCPUs.

### 2. Run Heuristics & Segment Tree (5k Servers)

```bash
python code/heuristics.py
```

Runs First-Fit Decreasing, demonstrates the Segment Tree for 5,000 servers, and prints the FFD counterexample.

### 3. Run Rejected Alternative (Pure Backtracking)

```bash
python code/rejected_alternative.py
```

Runs pure exhaustive search without lower bounding, demonstrating the growth in search effort.

### 4. Run Changed Requirement (2D Vector Packing + Anti-Affinity) — Member 5

```bash
python code/changed_requirement.py
```

Solves the changed-requirement example by considering:

- CPU capacity per server.
- RAM capacity per server.
- Anti-affinity: VMs belonging to the same service cannot share a server.
- Backtracking with branch-and-bound pruning.
- A lower-bound estimate based on total CPU demand, total RAM demand, and the largest number of VMs belonging to one service.
- Validation of the resulting placement.

The program prints the estimated lower bound, number of servers used, VM placements, resource utilization, and whether the placement satisfies the constraints.

For the included sample, each server has a capacity of 10 vCPUs and 16 GB RAM. The expected minimum is two servers.

### 5. Reproduce Timing Benchmarks & Generate Plots

```bash
python code/generate_inputs.py
```

Generates random test instances of sizes `N = [6, 8, 10, 12, 14, 16]`, runs the configured timing comparisons, and saves:

- `results/timing.csv`
- `results/timing_plot.png`

The benchmark script measures the algorithms configured in `generate_inputs.py`. Check that script to confirm which algorithms are timed and that the results include at least five input sizes.

### 6. Check the Results

After running the benchmark, verify that the output files exist:

```text
results/
    timing.csv
    timing_plot.png
```

Use the CSV to compare measured running times with the theoretical complexity discussed in the report. Include the timing plot in the assignment presentation or analysis.

## Notes

- Run commands from the `Batches/Batch_15` directory unless otherwise stated.
- The changed-requirement implementation uses a different sample from the original one-dimensional instance.
- The lower-bound estimate is not guaranteed to equal the optimal server count for every input.
- Exact backtracking can become expensive for large instances because its worst-case search is exponential.
- Keep the report, code, benchmark results, and plots consistent with the actual implementation.
