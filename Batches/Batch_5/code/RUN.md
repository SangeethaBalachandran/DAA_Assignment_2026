# Instructions to Run the Code (Batch 5)

This folder contains the complete, self-contained Python implementation for **Batch 5 – Satellite Knapsack Problem**.

## Prerequisites

- **Python**: Version 3.8 or later (tested on Python 3.10 to 3.15).
- **Standard Library**: Only standard Python modules (`heapq`, `dataclasses`, `time`, `csv`, `math`, `argparse`, `random`) are required to run all algorithms and benchmarks.
- **Optional**: `matplotlib` (only required if you want to regenerate `results/timing_plot.png` from scratch).

```bash
# Optional: install matplotlib for plot generation
pip install matplotlib
```

---

## 1. Running the Main Solution (Branch and Bound)

To solve the given satellite problem instance with the chosen **Best-First Branch and Bound** technique:

```bash
# Run from repository root or Batches/Batch_5:
python Batches/Batch_5/code/main_solution.py
```

To see the complete, step-by-step search tree exploration trace, node incumbent updates, and pruning actions:

```bash
python Batches/Batch_5/code/main_solution.py --trace
```

### Expected Output
- **Part 1 (15.0 kg mass limit)**:
  - Optimal selection: `('P2', 'P3', 'P4')`
  - Total scientific value: `174`
  - Mass consumed: `14.1 kg / 15.0 kg`
  - Nodes generated: `47` (expanded: `23`, pruned: `24`, infeasible: `1`)
- **Part 2 (+35 W power limit)**:
  - Old optimum `('P2', 'P3', 'P4')` requires `37 W` $\rightarrow$ infeasible.
  - New optimal selection: `('P1', 'P3', 'P4')`
  - Total scientific value: `172`
  - Mass: `13.4 kg`, Power: `33 W`

---

## 2. Running the Rejected Alternatives

To run the rejected techniques (Plain Backtracking, Dynamic Programming table, and Value Density Greedy):

```bash
python Batches/Batch_5/code/rejected_alternative.py
```

### Expected Output
- Demonstrates why **Plain Backtracking** is rejected (explores exponential state space without pruning).
- Demonstrates why **Dynamic Programming** is rejected (pseudo-polynomial $1,050,007$ cells on a $0.1\text{ g}$ mass grid; expands to $36.75\text{M}$ cells under power constraint).
- Demonstrates why **Greedy** is rejected (stops at value $142$ or $160$, failing to reach the optimal $174$).

---

## 3. Running Input Generation and Empirical Benchmarks

To generate synthetic weakly correlated test instances across 5 input sizes ($n \in \{8, 12, 16, 20, 24\}$) and update `results/timing.csv`:

```bash
python Batches/Batch_5/code/generate_inputs.py
```

To evaluate the pathological worst-case input family ($v_i = m_i$, even masses, odd capacity) showing the exponential growth of Branch and Bound:

```bash
python Batches/Batch_5/code/generate_inputs.py --worst-case
```

