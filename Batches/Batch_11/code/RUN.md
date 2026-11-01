# RUN instructions

Run all commands from the `Batch_11/` directory.

Requirements:
- Python 3.9 or later
- Matplotlib (only needed to generate the timing plot)

## 1. Run the chosen algorithm

```bash
python code/main_solution.py
```

## 2. Run the rejected alternative

```bash
python code/rejected_alternative.py
```

## 3. Generate benchmark inputs and timing results

```bash
python code/generate_inputs.py
```

To choose benchmark sizes and line width:

```bash
python code/generate_inputs.py --sizes 100 250 500 1000 2000 --width 16
```

The script generates deterministic word inputs in memory, runs both methods,
and creates/overwrites:
- `results/timing.csv`
- `results/timing_plot.png`

No compiler, executable, virtual environment, or third-party package is
needed for the two algorithms. Matplotlib is required only for the plot.
