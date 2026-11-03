# RUN.md — Batch 4 (best-value hotel strip)

Language: **Python 3.10+** (tested on 3.12.3). Standard library only for the algorithm;
`matplotlib` is needed only to redraw the plot. No compilation step.

All commands are run from `Batches/Batch_4/code/`.

```bash
cd Batches/Batch_4/code


python3 main_solution.py --instance



python3 main_solution.py --selftest


python3 rejected_alternative.py


python3 generate_inputs.py --mode anti --n 1000000 --seed 1 --out anti_1000000.csv
python3 main_solution.py --input anti_1000000.csv
python3 rejected_alternative.py --input anti_1000000.csv

pip install matplotlib        
python3 run_benchmark.py
```

Files

| file | role |
|---|---|
| `main_solution.py` | chosen algorithm: divide and conquer, 16 price-range shards, prefix-min merge; also the 3-D (rating) version and the O(n²) test oracle |
| `rejected_alternative.py` | rejected technique: global sort-and-sweep (greedy) |
| `generate_inputs.py` | produces the inputs used for timing (`uniform`, `anti`, `worst`, `instance`) |
| `run_benchmark.py` | timing harness (best of 3 for n ≤ 5·10⁵, single run above); writes `results/` |

Timing notes: the machine had one core, so the 16 "servers" run one after another.
`timing.csv` columns `time_chosen_ms` is the *sequential total* (partition + 16 local
solves + combine). The parallel figure in `timing_parallel_estimate.csv` is
`max(per-shard time) + combine time`; it ignores network cost and assumes the data is
already sharded, as it is in production.
