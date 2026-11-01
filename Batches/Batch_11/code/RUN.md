
# RUN Instructions

Run all commands from the `Batch_11/` directory.

## Requirements

- Python 3.9 or later
- Matplotlib (required only for generating the timing plot)

## 1. Run the Chosen Algorithm

The chosen algorithm uses Dynamic Programming to find the minimum paragraph layout penalty.

```bash
python code/main_solution.py
```

## 2. Run the Rejected Alternative

The rejected alternative uses a Greedy approach. It is included for comparison with the chosen Dynamic Programming algorithm.

```bash
python code/rejected_alternative.py
```

## 3. Generate Benchmark Inputs and Timing Results

Run the following command to generate benchmark inputs and measure the execution time of both algorithms.

```bash
python code/generate_inputs.py
```

### Choose Benchmark Sizes and Line Width

You can specify the input sizes and line width using command-line arguments.

```bash
python code/generate_inputs.py --sizes 100 250 500 1000 2000 --width 16
```

Here:

- `--sizes` specifies the number of words used in each benchmark.
- `--width` specifies the maximum number of characters allowed in each line.

## 4. Generated Output Files

The benchmark script generates deterministic word inputs in memory, runs both algorithms, and creates or overwrites the following files:

```text
results/
├── timing.csv
└── timing_plot.png
```

- **timing.csv:** Stores the execution-time results for both algorithms.
- **timing_plot.png:** Shows a comparison of the execution times of both algorithms.

## 5. Important Notes

- Python 3.9 or later is required.
- No compiler is required.
- No separate executable file is required.
- No virtual environment is required.
- No third-party package is needed to run the two algorithms.
- Matplotlib is required only for generating the timing plot.
- Run the commands from the `Batch_11/` directory to ensure the file paths work correctly.

## 6. Complete Execution Order

For a complete project execution, run these commands in order:

```bash
python code/main_solution.py
python code/rejected_alternative.py
python code/generate_inputs.py
```

After execution, check the `results/` folder for the benchmark CSV file and timing plot.
