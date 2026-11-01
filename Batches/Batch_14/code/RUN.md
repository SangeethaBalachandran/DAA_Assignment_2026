# How to run (Windows, Python 3.9+; standard library only)

Open Command Prompt or PowerShell in the `Batch_14\code` folder.

```bat
python main_solution.py            :: 7-feature ECU: 19 valid configs, stats for both variable orders
python main_solution.py --trace    :: + full execution trace (features-first order)
python main_solution.py --worst    :: constructed worst-case instances (measured counts)
python main_solution.py --bdd      :: ROBDD node counts for both orders
python rejected_alternative.py     :: exhaustive 2^7 enumeration + equality check with backtracking
python pairwise_testing.py         :: pairwise suite: real 7-feature ECU + synthetic 200 features
python generate_inputs.py          :: shows the seeded benchmark instances (n = 7..15)
pip install matplotlib             :: only needed for the benchmark plot
python benchmark.py                :: writes ..\results\timing.csv and ..\results\timing_plot.png (~1 min)
```
`generate_inputs.py` and `benchmark.py` are extra files required by the official repository README
(inputs for timing). Timings depend on the machine; counts (calls, assignments, valid configs) do not.
