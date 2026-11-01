# How to run (Python 3.9+; only `matplotlib` is needed, for the plot)

```bash
cd Batches/Batch_7/code
pip install matplotlib            # only for benchmark.py

python3 main_solution.py          # Q2 trace (rejections), min slots, Q5 (Maths pinned + day rule)
python3 rejected_alternative.py   # subset-DP answer + greedy counterexample (Q4)
python3 generate_inputs.py        # writes inputs/*.txt (edge lists) - optional
python3 benchmark.py              # regenerates ../results/*.csv and timing_plot.png (about 15 s)
```
Expected output of `main_solution.py`: 5 rejections, valid timetable
`{'DAA': 1, 'OS': 2, 'DBMS': 3, 'ML': 2, 'CN': 1, 'SE': 2, 'Maths': 1}`, min slots `3`.
`rejected_alternative.py` prints `greedy trap -> slots used: 3` while the DP optimum is `2`.
