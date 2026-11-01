# Running the Batch 12 code

Requirements: Python 3.9 or later. No third-party packages are needed for the algorithms.

From the `Batch_12` folder:

```bash
python code/main_solution.py
python code/rejected_alternative.py
```

To run the tests (merge sort and the weighted method compared with brute force, plus edge cases):

```bash
python -m unittest discover -s code -v
```

The benchmark data and plots are already supplied in `results/`. To reproduce the benchmark, run:

```bash
python code/benchmark.py
```

The benchmark uses identical deterministic permutations (random, sorted and
reverse-sorted) for both algorithms, checks that their answers agree, repeats each
measurement five times, and stores median times in `results/timing.csv` (random input)
and `results/timing_orders.csv` (all three orders). It then creates
`results/timing_plot.png`, `results/timing_orders_plot.png` and `results/environment.txt`.
The plots need `matplotlib`.

To generate sample inputs:

```bash
python code/generate_inputs.py
```

The main solution also includes a weighted inversion function. Its top-10 rule is:
a title is top-10 if it appears in Engine A's top 10 OR Engine B's top 10.
Confirm this interpretation with the instructor because the scenario does not
specify which engine defines top-10.
