# Disagreement Between Two Recommenders (OTT / Streaming)

**DAA Assignment 2026 · Batch 12**

| | |
|---|---|
| **Course** | 23I501, Design and Analysis of Algorithms |
| **Technique** | Divide and conquer (merge sort, inversion counting) |
| **Language** | Python 3.9+ |
| **Presentation** | [Watch / download on Google Drive](https://drive.google.com/file/d/1Jnad1sR8zAS14RBSG73Xh1ixmVqkRZrG/view?usp=drive_link) (11:37)|

---

## Summary

The **disagreement score** counts the pairs of titles that two recommendation engines order differently. It is the inversion count of one ranking written in the other's positions.

- Merge-sort counting computes it in **O(n log n)** time and **O(n)** extra space. Brute force takes **O(n²)** time.
- The given instance `[3, 1, 6, 2, 8, 4, 7, 5]` scores **9**. Under the weighted top-10 rule it scores **45**.
- At n = 5,000 on random input, brute force took about **64×** as long as merge sort in the measured runs.
- Merge sort and the weighted method match brute force on a thousand random inputs (`code/test_solution.py`).

## Table of Contents

1. [Problem modelling](#1-problem-modelling)
2. [Data structures](#2-data-structures)
3. [Design technique](#3-design-technique)
4. [Why the other techniques do not fit](#4-why-the-other-techniques-do-not-fit)
5. [Algorithm](#5-algorithm)
6. [Proof of correctness](#6-proof-of-correctness)
7. [Trace on the given instance](#7-trace-on-the-given-instance)
8. [Complexity analysis](#8-complexity-analysis)
9. [Worst-case input](#9-worst-case-input)
10. [Implementation and empirical analysis](#10-implementation-and-empirical-analysis)
11. [Changed requirement: weighted top-10 disagreements](#11-changed-requirement-weighted-top-10-disagreements)
12. [Answers to remaining scenario questions](#12-answers-to-remaining-scenario-questions)
13. [Real-world reference](#13-real-world-reference)
14. [Team contribution](#team-contribution)
15. [Running the project](#running-the-project)

---

## 1. Problem modelling

Two engines rank the same `n` unique titles. Engine B is represented as an array of the corresponding positions in Engine A. An **inversion** is a pair `(i, j)` where `i < j` and `B[i] > B[j]`. The output is the number of inversions.

The objective type is **counting (enumeration)**: there is no optimum to find and no yes/no question to answer.

> **Assumption:** the input is a permutation of `1..n`. The code does not validate this.

- **Given instance:** `[3, 1, 6, 2, 8, 4, 7, 5]`
- **Expected disagreement score:** `9`

## 2. Data structures

| Approach | Time | Extra space | Fits when |
| --- | --- | --- | --- |
| Array with brute-force pair scan | O(n²) | O(1) | Tiny inputs only |
| Array with merge-sort counting | O(n log n) | O(n) | A full ranking arrives at once |
| Fenwick tree (binary indexed tree) | O(n log n) | O(n) | Rankings arrive incrementally |

The Fenwick tree needs coordinate compression, or values that are already small indexes, and supports incremental updates and prefix queries. Merge sort is the preferred nightly batch method because it processes the full ranking in O(n log n).

## 3. Design technique

**Divide and conquer.** The array is split into two independent halves, and each recursive call counts the inversions inside its half. During the merge, if the next right value is smaller than the current left value, it is smaller than every remaining value in the sorted left half, so `len(left) - i` cross-inversions are added.

## 4. Why the other techniques do not fit

| Technique | Reason |
| --- | --- |
| Greedy | A local choice does not count every inverted pair; the merge counting argument is needed. |
| Dynamic programming | The two halves are independent, so there are no overlapping subproblems for memoization to reuse. |
| Backtracking | Checking all pairs costs O(n²), and enumerating rankings would cost far more. Neither is needed. |
| Branch and bound | The task counts every inversion instead of searching for one optimal answer, so pruning cannot skip any pair. |

## 5. Algorithm

`code/main_solution.py` implements merge-sort inversion counting. The recurrence is:

```
T(n) = 2T(n/2) + O(n),   T(1) = O(1)
```

```text
COUNT(A):
  if length(A) <= 1: return (A, 0)
  split A into L and R
  (L, cL) = COUNT(L)
  (R, cR) = COUNT(R)
  merge L and R into M
    whenever R[j] < L[i], add the number of elements left in L
  return (M, cL + cR + cross)
```

## 6. Proof of correctness

**Base case.** An array of size 0 or 1 contains no inversions, and `COUNT` returns 0.

**Inductive step.** Assume the recursive calls count the inversions inside the left and right halves correctly. During the merge, when `right[j] < left[i]`, the left half is sorted, so all remaining left elements are greater than `right[j]`. Adding their number counts exactly the cross-inversions that this right value contributes. The merge takes from the left when `left[i] <= right[j]`, so equal values are never counted, which matches the strict `B[i] > B[j]` definition.

**Completeness.** Every inversion lies wholly in the left half, wholly in the right half, or across the split. These categories are disjoint and cover all inversions, so their sum is the total.

## 7. Trace on the given instance

**Input:** `[3, 1, 6, 2, 8, 4, 7, 5]`

| Step | Left | Right | Merged | Cross-inversions |
| ---: | --- | --- | --- | ---: |
| 1 | `[3]` | `[1]` | `[1, 3]` | 1 |
| 2 | `[6]` | `[2]` | `[2, 6]` | 1 |
| 3 | `[1, 3]` | `[2, 6]` | `[1, 2, 3, 6]` | 1 |
| 4 | `[8]` | `[4]` | `[4, 8]` | 1 |
| 5 | `[7]` | `[5]` | `[5, 7]` | 1 |
| 6 | `[4, 8]` | `[5, 7]` | `[4, 5, 7, 8]` | 2 |
| 7 | `[1, 2, 3, 6]` | `[4, 5, 7, 8]` | `[1, 2, 3, 4, 5, 6, 7, 8]` | 2 |

- Left subtotal (steps 1 to 3) = **3**
- Right subtotal (steps 4 to 6) = **4**
- Final merge adds **2**
- **Total = 3 + 4 + 2 = 9**

## 8. Complexity analysis

Merge-sort counting takes **O(n log n)** time and **O(n)** auxiliary space, from the recurrence `T(n) = 2T(n/2) + O(n)`. Best, average and worst-case time are all O(n log n), because the same divide-and-merge recursion runs whatever the input order.

Constant factors still differ in practice. At n = 5,000 the measured merge-sort time was 3.69 ms on sorted, 4.53 ms on reverse-sorted and 6.63 ms on random input (see [section 10](#10-implementation-and-empirical-analysis)).

Brute force takes **O(n²)** time and **O(1)** auxiliary space.

## 9. Worst-case input

A reverse-sorted permutation `[n, n-1, ..., 1]` has the maximum `n(n-1)/2` inversions. For `n = 8` the score is `28`. Merge sort still takes O(n log n) time on this input, and `code/test_solution.py` checks the `n(n-1)/2` count directly.

## 10. Implementation and empirical analysis

### Project structure

| Path | What it holds |
| --- | --- |
| `code/main_solution.py` | Merge-sort counting and the weighted top-10 method |
| `code/rejected_alternative.py` | Brute-force baselines, plain and weighted |
| `code/generate_inputs.py` | Random, sorted and reverse-sorted permutations |
| `code/benchmark.py` | Reproducible benchmark and plots |
| `code/test_solution.py` | Unit tests against brute force |
| `code/RUN.md` | Commands to run everything |
| `results/timing.csv` | Median timings on random input |
| `results/timing_orders.csv` | Median timings on random, sorted and reverse-sorted input |
| `results/timing_plot.png` | Runtime plot, linear and log-log |
| `results/timing_orders_plot.png` | Merge-sort runtime by input order |
| `results/environment.txt` | Python version and platform of the benchmark run |
| `Batch_12_DAA_Slides.pptx` | Editable slide deck (15 slides) |
| `slides.pdf` | PDF export of the same deck |

### Benchmark method

The benchmark times both algorithms on identical deterministic permutations at n = 100, 500, 1,000, 2,000 and 5,000, taking the **median of five trials**. Both algorithms must return the same inversion count before any timing is recorded.

### Results: random input

| n | Merge sort (ms) | Brute force (ms) | Inversions |
| ----: | ----: | ----: | ----: |
| 100 | 0.07 | 0.13 | 2,151 |
| 500 | 0.48 | 3.89 | 65,826 |
| 1,000 | 1.09 | 16.84 | 246,619 |
| 2,000 | 2.33 | 67.57 | 972,436 |
| 5,000 | 6.63 | 425.29 | 6,132,879 |

### Results: input order at the largest size

| Input order (n = 5,000) | Merge sort (ms) | Brute force (ms) | Inversions |
| --- | ----: | ----: | ----: |
| random | 6.63 | 425.29 | 6,132,879 |
| sorted | 3.69 | 266.85 | 0 |
| reverse | 4.53 | 429.15 | 12,497,500 |

Merge sort grows as O(n log n) on every order. Its constant factor is lowest on sorted input and highest on random input.

### Limitations of the measurements

- The numbers come from one machine and one Python version (see `results/environment.txt`), so compare the shape of the curves more than the exact milliseconds.
- The recursive implementation allocates new lists at every level instead of merging in place. This adds a constant-factor cost and leaves the asymptotic bounds unchanged.

## 11. Changed requirement: weighted top-10 disagreements

**Assumption:** a title belongs to the top 10 if it appears in Engine A's top 10 **or** Engine B's top 10. Each inversion involving at least one top-10 title has **weight 5**; every other inversion has **weight 1**. The guide's wording does not say which engine defines the top 10, so this reading should be confirmed with the instructor.

The optimized weighted method keeps a suffix count of top-10 titles in the left half during each merge. For a right element that forms cross-inversions, it adds the number of cross-inversions plus four extra units for each qualifying pair. Time stays O(n log n) and auxiliary space stays O(n).

`count_weighted_inversions_brute` in `code/rejected_alternative.py` validates it, and the tests use inputs with n greater than 10 so that both the weight-5 and weight-1 cases occur.

For the supplied 8-title example every title is in the top 10 under this assumption. There are 9 inversions, so the weighted score is **9 × 5 = 45**.

## 12. Answers to remaining scenario questions

- **Nightly brute-force pair comparisons at the maximum size:**
  `5×10^7 × (10^5 × (10^5 − 1) / 2) = 2.499975 × 10^17`
- **Merge-sort estimate per user:** about `10^5 × log2(10^5) ≈ 1.66 × 10^6` scale units, and about `8.3 × 10^13` scale units across all users. These are asymptotic operation estimates, not wall-clock timings.
- **Memoization:** merge sort has no overlapping subproblems, so memoization does not help.

## 13. Real-world reference

Donald E. Knuth, *The Art of Computer Programming, Volume 3: Sorting and Searching*, 2nd edition, Addison-Wesley, 1998.

This is a general reference on sorting and permutations. It does not describe any named OTT platform's recommender pipeline.

---

## Team Contribution

### File-wise work distribution

| Member | Assigned files | Total |
| --- | --- | ---: |
| Ramishwar B | `main_solution.py`, `test_solution.py` | 2 |
| David Melvin L | `rejected_alternative.py`, `generate_inputs.py` | 2 |
| Rakesh M | `benchmark.py`, `timing.csv`, `timing_orders.csv` | 3 |
| Dev Pasanna R | `timing_plot.png`, `timing_orders_plot.png`, `environment.txt` | 3 |
| Gokul D | `README.md`, `RUN.md`, `analysis_sheet.pdf`, `slides.pdf` | 4 |

### Member details

| Member | Roll Number | GitHub Username | Files | Work Completed |
| --- | --- | --- | --- | --- |
| Ramishwar B | 24I347 | `Ramishwar18` | `main_solution.py`<br>`test_solution.py` | • Implemented the main inversion-counting solution using the divide-and-conquer approach with merge sort.<br>• Developed test cases to verify the correctness of the algorithm across different input scenarios.<br>• Checked that the solution correctly counts disagreements between the two recommenders. |
| David Melvin L | 24I309 | `DavidMelvin007` | `rejected_alternative.py`<br>`generate_inputs.py` | • Implemented a rejected alternative approach for comparison with the main divide-and-conquer solution.<br>• Created an input-generation script to produce datasets for testing and performance evaluation.<br>• Supported the comparison of algorithmic approaches using generated inputs. |
| Rakesh M | 24I346 | `Rakesh-56` | `benchmark.py`<br>`timing.csv`<br>`timing_orders.csv` | • Developed the benchmarking script to measure the execution time of the implemented algorithms.<br>• Recorded benchmark results in `timing.csv` and `timing_orders.csv` for analysis.<br>• Organized timing data to support performance comparisons across different input sizes and orders. |
| Dev Pasanna R | 24I310 | `DemonPrince07` | `timing_plot.png`<br>`timing_orders_plot.png`<br>`environment.txt` | • Generated `timing_plot.png` to visualize the algorithm's execution-time performance.<br>• Generated `timing_orders_plot.png` to compare performance across different input orders.<br>• Prepared `environment.txt` to document the software and execution environment used for testing. |
| Gokul D | 24I316 | `Gokul8148` | `README.md`<br>`RUN.md`<br>`analysis_sheet.pdf`<br>`slides.pdf` | • Prepared `README.md` to explain the project, algorithm, implementation, and team contributions.<br>• Created `RUN.md` with instructions for running the project and its related scripts.<br>• Prepared `analysis_sheet.pdf` and `slides.pdf` to document the analysis and present the project. |

## Running the project

From the `Batch_12` folder:

```bash
python code/main_solution.py                 # prints 9 and 45 for the given instance
python -m unittest discover -s code -v       # runs the tests
python code/benchmark.py                     # regenerates results/ (needs matplotlib)
```

The algorithms and the tests need **no third-party packages**. The benchmark plots require `matplotlib`. See `code/RUN.md` for details.
