# Telecom Fibre Rollout — Run Instructions

## Requirements
- Python 3.9 or later
- No third-party packages are required.

## Folder structure
```text
code/
├── main_solution.py
├── rejected_alternative.py
├── generate_inputs.py
└── RUN.md
```

## 1. Run the chosen algorithm
Open a terminal in the `code` folder and run:

```bash
python main_solution.py
```

On some systems, use `python3 main_solution.py` instead.

This runs Kruskal's algorithm on the project town network and prints the selected fibre links, minimum total cost, and execution time.

## 2. Run the rejected alternative
```bash
python rejected_alternative.py
```

This runs brute-force MST enumeration on a small demonstration graph. Brute force is included as a comparison technique, not as the main solution, because the number of edge combinations grows very quickly.

## 3. Generate timing inputs
```bash
python generate_inputs.py
```

This creates `generated_inputs.json` containing deterministic connected weighted graphs with 10, 25, 50, and 100 vertices.

## Notes
- Costs in the main project are in lakh rupees.
- The input generator uses a fixed seed, so it creates repeatable data.
- The generator creates test data; it does not automatically run the benchmark.
