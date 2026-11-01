# Batch 13 — EV Logistics

## Requirements
- Python 3
- Matplotlib (required for benchmark graph generation)

Install Matplotlib if needed by running:

python -m pip install matplotlib

## Run the Chosen Greedy Algorithm

python Batches/Batch_13/code/main_solution.py

## Generate Test Inputs

python Batches/Batch_13/code/generate_inputs.py

## Run the Benchmark

Run this command from the repository root folder:

python Batches/Batch_13/code/run_benchmark.py

The benchmark compares the chosen Greedy algorithm with the rejected Dynamic Programming (DP) algorithm. It calculates the average execution time over three runs for each input size.

## Output Files

- Batches/Batch_13/results/timing.csv — Contains the benchmark timing results.
- Batches/Batch_13/results/timing_plot.png — Contains the performance comparison graph.

## Time Complexity

- Chosen Greedy Algorithm: O(n log n), including sorting the charging stations.
- Rejected Dynamic Programming Algorithm: O(n²).