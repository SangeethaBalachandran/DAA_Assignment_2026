# Batch 3 – Database Systems: Ordering Joins in a Query Optimiser

## RUN Instructions

### 1. Requirements

- Python 3.x
- VS Code or any Python-supported IDE
- No external Python libraries are required.

### 2. Folder Structure

```text
Batch_3/
├── README.md
├── slides.pdf
├── code/
│   ├── main_solution.py
│   ├── rejected_alternative.py
│   ├── generate_inputs.py
│   └── RUN.md
└── results/
    ├── timing.csv
    └── timing_plot.png
```

### 3. Run the Dynamic Programming Solution

Open the terminal and navigate to the code directory:

```bash
cd Batches/Batch_3/code
```

Execute:

```bash
python main_solution.py
```

The program displays:
- Minimum join cost
- Optimal join order
- Dynamic Programming cost table

**Expected Output:**

```text
Minimum Join Cost: 24500
Optimal Join Order: ((R1 JOIN (R2 JOIN R3)) JOIN (R4 JOIN R5))
```

### 4. Run the Greedy Alternative

Execute:

```bash
python rejected_alternative.py
```

**Expected Greedy Cost:**

```text
30000
```

### 5. Generate Inputs and Benchmark Algorithms

Execute:

```bash
python generate_inputs.py
```

The script:
- Generates dimensions for 5, 10, 15, 20, and 25 relations.
- Executes the Dynamic Programming and Greedy algorithms.
- Measures execution times over 5 repetitions.
- Calculates median execution times.
- Saves benchmark results in `../results/timing.csv`.

### 6. View Results

The `results/` directory contains:

| File | Description |
|---|---|
| `timing.csv` | Measured execution times and algorithm costs |
| `timing_plot.png` | Performance comparison plot |

**Note:** The current `generate_inputs.py` script generates `timing.csv`. The timing plot must be generated separately unless plotting code is added to the script.

### 7. Execution Order

Run these commands from the `Batches/Batch_3/code/` directory:

```bash
python main_solution.py
python rejected_alternative.py
python generate_inputs.py
```

### 8. Notes

- Execution times may vary depending on the system.
- Run `generate_inputs.py` before analysing benchmark results.
- Ensure that `timing.csv` contains actual measured results before using it in the assignment analysis.
