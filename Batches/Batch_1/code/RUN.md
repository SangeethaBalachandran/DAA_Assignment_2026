# How to run (Batch 1)

Requirements: **Python 3.9+** (tested on Python 3.12.3, Linux).  
Only `benchmark.py` and `make_trace.py` need `matplotlib` (`pip install matplotlib`). Everything else uses the standard library.

Run all commands from inside `Batches/Batch_1/code/`.

| Purpose | Command |
|---|---|
| Solve the assignment instance (A = 15,22,35,40,48,53,61 thousand; target 110 thousand) | `python main_solution.py` |
| Same, printing every state and pruning decision | `python main_solution.py --trace` |
| Changed requirement: accept sums within ±₹50 | `python main_solution.py --tolerance 50` |
| Your own input (amounts in thousands of rupees) | `python main_solution.py --amounts 10 20 30 --target 40 --scale 1000` |
| Your own input in plain rupees | `python main_solution.py --amounts 15020 22000 --target 37020 --scale 1 --tolerance 50` |
| Brute-force alternative on the same instance | `python rejected_alternative.py` |
| Generate a benchmark input (JSON) | `python generate_inputs.py --family hard --n 16` (families: `random`, `hard`) |
| Self-tests (cross-check against brute force, DP, meet-in-the-middle; exact state counts) | `python test_all.py` (prints `ALL TESTS PASS`) |
| Independent checks (own bitmask brute force, hard-family counts, mutation test) | `python verify_independent.py` (prints `ALL INDEPENDENT CHECKS PASSED`) |
| Numbers quoted in the report (tolerance study, worst cases, DP size) | `python extra_experiments.py` |
| Regenerate `extras/TRACE.md` and `results/search_tree.png` | `python make_trace.py` |
| Re-run the timing experiments (~30 s) → `results/timing.csv`, `results/timing_large_n.csv`, `results/timing_plot.png` | `python benchmark.py` |

## Units
* `--amounts`, `--target` are in *input units*; `--scale` is rupees per input unit (default 1000, i.e. thousands).
* `--tolerance` is always in **rupees**. Internally everything is an **integer number of rupees** (no floats). Decimals such as `0.05` are converted exactly with `fractions.Fraction`; an input that is not a whole number of rupees is rejected.

## Notes
* Timings depend on your computer. After re-running `benchmark.py`, commit the new CSV **and** the new plot together so that they match.
* The benchmark stops with `MISMATCH` if the two algorithms ever return different solution sets.
