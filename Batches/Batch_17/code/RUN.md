# RUN.md — Batch 17 (Digital Marketing, 0/1 Knapsack)

Requirements: Python 3.8+. `numpy` and `matplotlib` are needed only for the
changed-requirement demo (`--large`) and for the benchmark plot.

```bash
pip install numpy matplotlib
cd Batches/Batch_17/code
```

| Purpose | Command |
|---|---|
| Solve the given instance (DP vs Greedy) | `python main_solution.py` |
| Show every intermediate DP table (Step 6 trace) | `python main_solution.py --trace` |
| Run the Greedy (rejected) algorithm alone | `python rejected_alternative.py` |
| Verify DP against brute force on 300 random cases | `python main_solution.py --selftest` |
| Benchmark DP vs Greedy, write `../results/timing.csv` and `timing_plot.png` | `python main_solution.py --benchmark` |
| Worst-case input (all costs = 1, B = 10n) | `python main_solution.py --worst` |
| Changed requirement: 300 campaigns, Rs 4,37,52,900 (FPTAS + cost scaling) | `python main_solution.py --large` |
| Print the given input / a random input | `python generate_inputs.py` / `python generate_inputs.py --n 50` |
| Save all benchmark datasets as JSON | `python generate_inputs.py --bench-dir data/` |

Expected output of `python main_solution.py`:

```
Dynamic Programming result
  selected   : ['C2', 'C4', 'C5']
  total cost : 9 lakh
  conversions: 127 (1-D check: 127 )
Greedy result
  selected   : ['C1', 'C2', 'C3']
  total cost : 9 lakh
  conversions: 125
Greedy loses 2 conversions (1.57% below optimal)
```

All random data uses seed 17, so results are reproducible. Timings (milliseconds)
will differ slightly between machines; the shape of the curves will not.
