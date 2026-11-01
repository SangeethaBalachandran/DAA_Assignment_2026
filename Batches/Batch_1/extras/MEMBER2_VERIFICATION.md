# Member 2 verification record (Batch 1)

This file records the checks listed in `MEMBER_2_TASKS.md`. Everything marked **executed** was run in the package-building sandbox (Python 3.12.3) and can be re-run with the command shown. Items marked **to do by Member 2** cannot be done by anyone else (own GitHub commits, own voice in the video, re-running timings on own computer).

## Status of the 14 tasks

| # | Task | Status in this package | How to re-check |
|---|---|---|---|
| 1 | Independent brute force | **Executed.** `code/verify_independent.py` contains a bitmask brute force (different method from `rejected_alternative.py`, which uses `itertools`). Both agree. | `python verify_independent.py` |
| 2 | Compare outputs (200 random cases, duplicates, tolerance 0/1/5) | **Executed**, all equal; plus a mutation test (changing `>` to `>=` in the overshoot rule) which the checker detects. | same command |
| 3 | Hand-verify the solution list | **Executed** (tables below). | by hand |
| 4 | Review §2 and §4 arithmetic and wording | **Executed** (findings below). | `python extra_experiments.py` |
| 5 | Hard-input verification and own extra input | **Executed**: own generator reproduces `C(n, n/2)` for n = 8, 12, 16, 20; extra input = equal amounts. | `python verify_independent.py` |
| 6 | Review benchmark design | **Executed** (findings below). | read `code/benchmark.py` |
| 7 | Re-run timings | **Executed once more in a scratch copy** (second run, same sandbox): states identical, times within a few percent for n ≥ 12. **To do by Member 2:** run `python benchmark.py` on your own computer and commit CSV + plot together. | `python benchmark.py` |
| 8 | Proof and complexity review | **Executed** (worked example below; `python test_all.py` passes). | `python test_all.py` |
| 9 | Changed-requirement verification | **Executed** (below). | commands below |
| 10 | Validate references | **Executed** (below). **To do by Member 2:** open the links yourself once. | open links |
| 11 | Slides 8–13 in your own words | Draft scripts exist in `extras/SPEAKER_SCRIPT.md`. **To do by Member 2:** rewrite in your own words and practise. | time yourself: about 5:00 |
| 12 | Record your part | **To do by Member 2.** | open link in a private window |
| 13 | Own commits | **To do by Member 2** (from your own GitHub account). | `git log --author` |
| 14 | Final review | **To do by both** with `extras/FINAL_CHECKLIST.md`. | checklist |

## Task 3: hand enumeration of subsets of {15, 22, 35, 40, 48, 53, 61} with sum 110

Step 1: size 1: no single amount equals 110 (largest is 61).

Step 2: size 2: the 21 pair sums (largest possible pair is 53 + 61 = 114).

| pair | sum | pair | sum | pair | sum |
|---|---|---|---|---|---|
| {15, 22} | 37 | {15, 35} | 50 | {15, 40} | 55 |
| {15, 48} | 63 | {15, 53} | 68 | {15, 61} | 76 |
| {22, 35} | 57 | {22, 40} | 62 | {22, 48} | 70 |
| {22, 53} | 75 | {22, 61} | 83 | {35, 40} | 75 |
| {35, 48} | 83 | {35, 53} | 88 | {35, 61} | 96 |
| {40, 48} | 88 | {40, 53} | 93 | {40, 61} | 101 |
| {48, 53} | 101 | {48, 61} | 109 | {53, 61} | 114 |

No pair sums to 110 (pairs reaching ≥ 110: only 53+61 = 114, 48+61 = 109 is one short). Pairs equal to 110: none.

Step 3: size 3: 35 triples; those that sum to exactly 110:

| triple | sum |
|---|---|
| {22, 35, 53} | 110 |
| {22, 40, 48} | 110 |

For completeness, triples with sum within 105 to 115: {15, 35, 61}=111, {15, 40, 53}=108, {22, 35, 48}=105, {22, 35, 53}=110, {22, 40, 48}=110, {22, 40, 53}=115.

Step 4: size ≥ 4: the four smallest amounts already sum to 15 + 22 + 35 + 40 = 112 > 110, so no subset with 4 or more items can work.

**Result:** exactly two subsets, {22, 35, 53} and {22, 40, 48}. This equals the output of both programs.

## Task 4: review of README §2 and §4 (arithmetic and wording)

Re-computed independently (`python extra_experiments.py`, last block):

| Claim in report | Re-computed | OK? |
|---|---|---|
| DP cells `(n+1)(T+1)`, n = 40, T = 10⁹ | 41,000,000,041 ≈ 4.1×10¹⁰ | yes |
| as bytes / as bits / one row as bitset | 41 GB / 5.125 GB / 125 MB | yes |
| `2⁴⁰` vs `n·T` | 1.0995×10¹² vs 4×10¹⁰ (ratio ≈ 27) | yes (so DP has the smaller worst-case *count*; the report says this openly) |
| DP table for the instance, T = 110 (thousand) | (7+1)(110+1) = 888 cells vs 35 search states | yes |
| greedy on the instance | 61 → remaining 49 → 48 → remaining 1 → stuck (`greedy_largest_fit` returns `[6, 4]`, remainder 1000) | yes |
| 49 is not a subset sum of {15,22,35,40,48,53} | singles: none; pairs: 37 … 101 but none equals 49; triples ≥ 72 | yes |
| meet-in-the-middle returns the same solutions | `analysis_tools.meet_in_middle` = brute force on 400 random cases (`test_all.py`) | yes |

Wording check: no sentence says a technique "cannot" solve the problem when it can. DP, Divide and Conquer (meet-in-the-middle) and Branch and Bound are each described as *possible*, with the reason they are less suitable here. Only Greedy is called incorrect, and that is backed by a counterexample.

Improvements made as a result of this review (applied in `README.md`):
1. §10 now states the reproducibility result of a second benchmark run, and that timings for n ≤ 10 are only indicative (small-n times differ by up to about 50 % between runs: 0.041 ms vs 0.064 ms for random n = 8).
2. §9 now contains a second difficult input (equal amounts) and says clearly that it is output-bound, not search-bound.
3. §10 now lists the independent verification script and its mutation test.

## Task 5: our own difficult input
Equal amounts, target = half the total (`python verify_independent.py`, check 4):

| n | solutions | states | 2ⁿ |
|---|---|---|---|
| 12 | 924 = C(12,6) | 1,716 | 4,096 |
| 16 | 12,870 = C(16,8) | 24,310 | 65,536 |
| 20 | 184,756 = C(20,10) | 352,716 | 1,048,576 |

Here the output itself is exponential, so no algorithm can do better than output size. This differs from the "no solution" family, where all the work is search.

## Task 6: benchmark design review
Checked in `code/benchmark.py`: (a) both algorithms receive the same list object per input; (b) timed region is only the function call (`median_ms` wraps `fn()`), printing and CSV writing are outside; (c) `gc.collect()` before each repetition; (d) median statistic; (e) correctness gate: solution sets compared before timing, run aborts with `MISMATCH`; (f) fixed seed `2026`.
Weaknesses found:
- The random family has only 5 inputs per n, so its curve is irregular (state count depends on target vs total). *Fix if time permits:* 20+ inputs per n and report the median and inter-quartile range.
- Times for n ≤ 10 are dominated by fixed overhead and noise. *Fix:* repeat each tiny run in an inner loop (e.g. 1000 calls) and divide.

## Task 7: reproducibility (second run in a scratch copy)
Same sandbox, same code, `python benchmark.py` run again; compared with the committed `timing.csv`:
- `states_chosen` identical in all 16 rows.
- Speed-up at n = 22: random 239.4× (committed) vs 241.6× (re-run); hard 8.5× vs 8.4×.
- Hard family times differ by less than 3 % for n ≥ 12; random n = 8 differs by about 50 % (noise at 0.04 ms).
- README §10 table values equal `timing.csv` exactly (8 rows checked by script).
The committed CSV and plot come from one run; they were not changed by the second run.

## Task 8: proof walk-through
Worked example `[5,5,5,10]`, target 10, τ = 0 (real trace, `python main_solution.py --amounts 5 5 5 10 --target 10 --scale 1 --trace`):
- Items sorted: positions 0,1,2 = 5, position 3 = 10; `suffix = [25, 20, 15, 10]`.
- Root S1 → children 5 (S2). From S2 (sum 5): child 5 gives S3 = {5,5} sum 10 → **solution** (Lemma A: adding 5 more gives 15 > 10, so the loop breaks, skipping 2 branches). Then child (pos 2) S4 = {5(pos 0), 5(pos 2)} → **solution**; then 10 gives 15 > 10, break.
- S5 = {pos 1}: child pos 2 gives S6 → **solution**. S7 = {pos 2}: 5 + 10 = 15 > 10 → overshoot. S8 = {10} → **solution**.
- Result: three pairs of 5s (three different transaction pairs) plus the single 10: 4 solutions, 8 states of 16 subsets, 6 overshoot cuts. This shows duplicates are separate items and that Lemma A cut off only invalid completions (every cut-off completion has sum ≥ 15).
- Hockey-stick check (README §9): hard family n = 6 → states = 20 = C(6,3). ✔ (`generate_inputs.hard_instance(6)`).
- Why `break` and not `continue`: if item j overshoots then all later items (≥ v_j) overshoot, and if `c + suffix[j] < lo` then `c + suffix[j'] < lo` for all j' > j since the suffix shrinks.

## Task 9: changed requirement
```
python main_solution.py --tolerance 50
python main_solution.py --amounts 15020 22000 35000 39990 48000 53030 61000 --target 110000 --scale 1 --tolerance 50
python main_solution.py --amounts 15020 22000 35000 39990 48000 53030 61000 --target 110000 --scale 1 --tolerance 0
```
Results: (1) 2 solutions, 35 states (unchanged because every sum is a multiple of ₹1,000). (2) 2 solutions: 22000+35000+53030 = 110,030 and 22000+39990+48000 = 109,990; 35 states. (3) 0 solutions, 34 states. Hand check: 110,030 − 110,000 = +30 ≤ 50 ✔; 109,990 − 110,000 = −10 ≥ −50 ✔. Unit conversion: 0.05 thousand × 1000 = 50 rupees (`to_rupees("0.05", 1000) == 50` in `test_all.py`).

## Task 10: reference validation
| Reference | What was checked | Result |
|---|---|---|
| Horowitz & Sahni, *J. ACM* 21(2):277–292, April 1974, DOI 10.1145/321812.321823 | Journal, volume, pages and year confirmed in two bibliographies (MIT J. ACM index of author pages; Crossref record cited by Martello & Toth); the Cornell technical-report abstract (hdl.handle.net/1813/5989) says it investigates algorithms for finding all combinations of numbers that sum to M and a technique that improves the dynamic-programming methods by a square-root factor | valid. Relating that to meet-in-the-middle is standard knowledge but is **not** stated in the abstract; the report says so. |
| Golomb & Baumert, "Backtrack Programming", *J. ACM* 12(4):516–524, October 1965, DOI 10.1145/321296.321300 | Crossref listing and NIST *Dictionary of Algorithms and Data Structures* entry "backtracking" (https://www.nist.gov/dads/HTML/backtrack.html) both cite it | valid |
| Python docs, `itertools.combinations` | Page fetched: tuples in lexicographic order, elements unique by position, length `n!/r!/(n−r)!`; no target or pruning | valid; matches how the report uses it |

**Member 2: open each link once yourself** before submission (the checks above were done by search and fetch, not by you).
