# How to run (Python 3.9+, no compilation)

All commands are run from inside the `code/` folder.

```bash
cd Batches/Batch_6/code

# Question 1: DP table, minimum cost, edit operations, all co-optimal alignments
python3 main_solution.py GATTACA GCATGCA

# Question 2 + 3: greedy aligner, plain recursion (with call counts), branch and bound
python3 rejected_alternative.py

# Question 4: linear-memory recovery of the alignment
python3 linear_space.py GATTACA GCATGCA

# Question 5: affine gaps (open 3, extend 1): prints the M, X and Y tables
python3 affine_gap.py GATTACA GCATGCA

# Inputs used for timing (reference on line 1, read on line 2)
python3 generate_inputs.py 20 --kind mutated --seed 1

# Timing experiments -> ../results/timing.csv, timing_scaling.csv, worst_case.csv,
#                       memory_demo.csv, timing_plot.png   (about 2-3 minutes)
pip install matplotlib        # only needed for the plot
python3 run_timing.py
python3 run_timing.py --quick # smoke test, about 10 seconds
```

Files

| File | Purpose |
|---|---|
| `main_solution.py` | chosen method: full table + traceback (Q1), also enumerates all co-optimal alignments |
| `linear_space.py` | linear-memory path recovery (Q4) |
| `affine_gap.py` | affine gap costs, three tables (Q5) |
| `rejected_alternative.py` | plain recursion, greedy aligner, branch and bound (Q2, Q3, rejection evidence) |
| `generate_inputs.py` | deterministic input generator (random / mutated / identical / mismatch) |
| `run_timing.py` | timing, worst-case and memory experiments, plot |

Timings in the report were measured with CPython on one machine; absolute numbers will differ on yours, the shapes should not.
