# Batch 11 – Publishing: Paragraph Layout in an E-Reader

**Course:** 23I501 – Design and Analysis of Algorithms  
**Institution:** PSG College of Technology  
**Academic Year:** 2026–2027  
**Batch:** 11  
**Programming Language:** Python 3.9 or later  
**Selected Design Technique:** Dynamic Programming

---

# Team Details and Contributions

| Roll Number | Name | GitHub Username | Part Presented | Contribution |
|---|---|---|---|---|
| 24I351 | Sabarinathan L | sabarinathan50 | Execution Instructions | Prepared `RUN.md` with project requirements, execution commands, and instructions for running the algorithms and generating benchmark results. |
| 24I337 | Om Arya SP | arya1485553-cyber | Greedy Alternative | Prepared `rejected_alternative.md` explaining the rejected Greedy approach and its comparison with the selected algorithm. |
| 24I321 | Karthick B | karthick25-car | Team Lead – Results and Presentation | Coordinated the team, managed project results, prepared presentation slides, and handled the timing graph (`timing_plot.png`). |
| 24I367 | Tarun A | Tarun24i367 | Dynamic Programming | Implemented the selected Dynamic Programming solution in `main_solution.py`. |
| 24I375 | Vishal V | Vishal24i375 | Benchmarking and Input Generation | Developed `generate_inputs.py` to generate benchmark inputs, measure execution times, and produce timing results. |

---

# 1. Problem Modelling

## Problem Statement

An e-reader application must arrange a sequence of words into lines of a fixed maximum width `W`.

The application should format the paragraph so that the total penalty caused by unused spaces is minimized.

The penalty for each non-final line is the cube of its unused spaces. The last line of the paragraph has no penalty.

### Input

- A sequence of `n` words.
- Maximum line width `W`.

### Output

- An arrangement of words into valid lines.
- The minimum total penalty.

### Objective

Minimize the total penalty of all lines.

For a non-final line:

\[
Penalty = (Unused\ Spaces)^3
\]

For the final line:

\[
Penalty = 0
\]

### Constraints

1. Words must remain in their original order.
2. Words cannot be split between lines.
3. Every line must fit within the maximum width `W`.
4. At least one word must be placed on each line.
5. The last line has zero penalty.

### Problem Classification

This is a text formatting and optimization problem. It can be solved using Dynamic Programming because the optimal arrangement can be constructed from optimal arrangements of smaller groups of words.

---

# 2. Data Structure Analysis

The following data structures are used in the implementation.

| Data Structure | Purpose |
|---|---|
| List | Stores the input words |
| Prefix Sum Array | Helps calculate the total length of consecutive words efficiently |
| Dynamic Programming Array | Stores the minimum penalty for each prefix of words |
| Variables | Store line width, unused spaces and calculated penalty |

### Why These Data Structures Are Suitable

- Lists provide convenient access to words.
- Prefix sums avoid repeatedly calculating the length of word groups.
- The DP array stores previously calculated minimum penalties.
- These structures help reduce unnecessary calculations.

---

# 3. Design Technique Identification

## Selected Technique: Dynamic Programming

Dynamic Programming is selected because the paragraph layout problem has two important properties.

### 1. Optimal Substructure

The optimal arrangement of the first `j` words can be obtained by combining the optimal arrangement of an earlier group of words with a valid final line.

### 2. Overlapping Subproblems

The minimum penalty for earlier groups of words is needed repeatedly while evaluating different line arrangements.

Dynamic Programming stores these results and reuses them instead of calculating them again.

## Recurrence Relation

Let:

- `DP[j]` = Minimum penalty for arranging the first `j` words.
- `W` = Maximum line width.
- `Cost(i,j)` = Penalty for placing words `i` through `j` on one line.

Initially:

\[
DP[0] = 0
\]

For every valid line ending at word `j`:

\[
DP[j] = \min_{1 \leq i \leq j}
\left(DP[i-1] + Cost(i,j)\right)
\]

Only valid line arrangements that fit within width `W` are considered.

The cost is calculated as follows:

- If the line is the final line of the complete paragraph, its cost is zero.
- Otherwise, its cost is the cube of its unused spaces.

The algorithm selects the arrangement with the minimum total penalty.

---

# 4. Why the Other Four Design Techniques Do Not Fit

The assignment considers five design techniques. Dynamic Programming is selected, and the other four are evaluated below.

## A. Divide and Conquer

Divide and Conquer divides a problem into independent smaller problems and combines their results.

However, paragraph layout decisions are dependent on previous line breaks. The minimum cost of a later group depends on the best arrangement of the earlier words.

Therefore, directly dividing the paragraph into independent parts does not guarantee a globally optimal result.

## B. Greedy Algorithm

A Greedy algorithm makes the locally best choice at each step.

For this problem, a Greedy approach can place as many words as possible on the current line.

However, this does not always minimize the total cubic penalty.

**Example:**

Let the line width be:

\[
W = 16
\]

Input words:

`A clear model of the problem is half of the final answer`

One possible Greedy arrangement is:

| Line | Words | Unused Spaces | Penalty |
|---|---|---:|---:|
| 1 | A clear model of | 0 | 0 |
| 2 | the problem is | 2 | 8 |
| 3 | half of the | 5 | 125 |
| 4 | final answer | Final line | 0 |

Total penalty:

\[
0 + 8 + 125 = 133
\]

A better arrangement found using Dynamic Programming is:

| Line | Words | Unused Spaces | Penalty |
|---|---|---:|---:|
| 1 | A clear model | 3 | 27 |
| 2 | of the problem | 2 | 8 |
| 3 | is half of the | 2 | 8 |
| 4 | final answer | Final line | 0 |

Total penalty:

\[
27 + 8 + 8 = 43
\]

Since 43 is less than 133, this example shows that the Greedy arrangement is not always optimal.

Therefore, Greedy is rejected as the main technique.

## C. Backtracking

Backtracking explores different possible arrangements and checks whether they satisfy the constraints.

For this problem, it may explore a large number of possible line breaks.

As the number of words increases, the number of arrangements can grow significantly.

Dynamic Programming is more suitable because it stores and reuses solutions to overlapping subproblems.

## D. Branch and Bound

Branch and Bound explores possible solutions while using bounds to eliminate branches that cannot improve the current best solution.

However, it requires suitable bounds to prune the search effectively.

For this problem, Dynamic Programming provides a more direct method of calculating the minimum penalty without repeatedly exploring the same subproblems.

## Comparison

| Technique | Reason for Rejection |
|---|---|
| Divide and Conquer | Subproblems are not independent |
| Greedy | Local choices do not always give the minimum total penalty |
| Backtracking | Explores too many possible arrangements |
| Branch and Bound | Requires additional bounds and search management |
| Dynamic Programming | Selected because it reuses optimal subproblem results |

---

# 5. Algorithm Pseudocode

**Input:** List of words and maximum line width `W`.

**Output:** Minimum total paragraph layout penalty.

```text
WORD_WRAP(words, W):

    n = number of words

    Create DP array of size n + 1
    Initialize all DP values to infinity

    DP[0] = 0

    For j from 1 to n:

        For i from j down to 1:

            Calculate the total width of words
            from i to j, including spaces

            If total width is greater than W:
                Stop checking earlier starting positions

            Calculate unused spaces

            If j is the final word:
                line_cost = 0
            Else:
                line_cost = unused_spaces * unused_spaces
                            * unused_spaces

            DP[j] = minimum of:
                    DP[j],
                    DP[i - 1] + line_cost

    Return DP[n]
```

The actual Python implementation is available in:

`code/main_solution.py`

---

# 6. Proof of Correctness

The correctness of the algorithm can be explained using induction.

## Base Case

When there are zero words, no line is required.

Therefore:

\[
DP[0] = 0
\]

This is correct because the penalty is zero.

## Inductive Hypothesis

Assume that `DP[k]` contains the minimum possible penalty for arranging the first `k` words, for every `k` smaller than `j`.

## Inductive Step

Consider an optimal arrangement of the first `j` words.

Its final line must contain some consecutive group of words from position `i` to `j`.

The words before position `i` must be arranged optimally. Otherwise, replacing their arrangement with a lower-penalty arrangement would improve the complete solution, contradicting optimality.

By the inductive hypothesis, the minimum penalty for the preceding words is:

\[
DP[i-1]
\]

The algorithm considers every valid possible starting position `i` for the final line and adds the correct line cost.

It selects the minimum among all these possibilities.

Therefore, `DP[j]` stores the minimum possible penalty for the first `j` words.

By induction, `DP[n]` gives the minimum total penalty for the complete paragraph.

Hence, the algorithm is correct.

---

# 7. Trace on the Given Instance

Consider the following example.

**Input words:**

`A clear model of the problem is half of the final answer`

**Maximum line width:**

\[
W = 16
\]

The Dynamic Programming algorithm evaluates valid line arrangements and selects the arrangement with the minimum total penalty.

## Selected Arrangement

| Line | Words | Characters Used | Unused Spaces | Penalty |
|---|---|---:|---:|---:|
| 1 | A clear model | 13 | 3 | 27 |
| 2 | of the problem | 14 | 2 | 8 |
| 3 | is half of the | 14 | 2 | 8 |
| 4 | final answer | 12 | Final line | 0 |

## Total Penalty

\[
27 + 8 + 8 + 0 = 43
\]

**Minimum total penalty = 43**

The final line is free, so it contributes zero penalty.

---

# 8. Complexity Analysis

Let:

- `n` = Number of words.
- `W` = Maximum line width.

The algorithm uses a Dynamic Programming array and a prefix sum array.

For each word position, it checks possible previous line starting positions until the line width becomes invalid.

With positive integer word lengths, the number of words that can fit in a line is bounded by the line width.

## Time Complexity

\[
O(nW)
\]

This is the bound when the maximum number of candidate words per line is bounded by `W`.

## Space Complexity

\[
O(n)
\]

The DP array and prefix sum array each require linear space.

The exact number of iterations depends on the word lengths and the number of valid line arrangements.

---

# 9. Worst-Case Input

A worst-case input contains many short words that can fit together in different combinations within the line width.

For example:

- Number of words: 2000
- Maximum line width: 16
- Words: Repeated short words such as `a`, `to`, `is`, and `in`

This type of input allows the algorithm to examine many possible line endings.

It is useful for measuring the performance of the implementation as the number of words increases.

The benchmark script generates deterministic inputs for different sizes.

---

# 10. Implementation and Empirical Analysis

## Implementation

The project is implemented using Python.

The following files are included:

| File | Purpose |
|---|---|
| `main_solution.py` | Implements the selected Dynamic Programming algorithm |
| `rejected_alternative.py` | Implements the Greedy alternative |
| `generate_inputs.py` | Generates benchmark inputs and measures execution time |
| `RUN.md` | Contains execution instructions |

## Experimental Setup

The benchmark script tests five different input sizes:

- 100 words
- 250 words
- 500 words
- 1000 words
- 2000 words

The line width is set to 16 for the benchmark command.

## Benchmark Command

```bash
python code/generate_inputs.py --sizes 100 250 500 1000 2000 --width 16
```

## Actual Timing Results

The following values are the measured execution times from the benchmark results.

| Input Size (n) | Dynamic Programming Time (ms) | Greedy Time (ms) |
|---:|---:|---:|
| 100 | 0.081012 | 0.012979 |
| 250 | 0.199931 | 0.029925 |
| 500 | 0.441025 | 0.062084 |
| 1000 | 0.923113 | 0.123146 |
| 2000 | 1.951815 | 0.249296 |

## Timing Results Interpretation

- Dynamic Programming takes more execution time because it checks multiple valid line arrangements.
- Greedy takes less execution time because it makes a local decision for each line.
- As the input size increases, the execution time of both algorithms increases.
- Dynamic Programming is selected because it provides the minimum penalty, while the Greedy alternative does not guarantee an optimal arrangement.

## Graph

The benchmark script generates the timing graph at:

`results/timing_plot.png`

The graph compares the execution times of Dynamic Programming and Greedy for the five input sizes.

## Generated Output Files

```text
results/
├── timing.csv
└── timing_plot.png
```

- `timing.csv` stores the input sizes and execution times.
- `timing_plot.png` provides a visual comparison of the algorithms.

## Observation

The experimental results show that the Greedy approach is faster in the tested inputs. However, faster execution does not guarantee the minimum penalty.

Dynamic Programming requires additional calculations but evaluates possible valid line arrangements to obtain the optimal result.

Execution times may vary depending on the computer and system workload.

---

# 11. Changed Requirement – Hyphenation

## New Requirement

Suppose the e-reader application allows long words to be split across lines using hyphenation.

The current implementation does not support this feature because it assumes that words cannot be split.

## Required Changes

1. Identify valid positions where a word can be split.
2. Include the hyphen character in the line-width calculation.
3. Consider the possible word fragments when generating line arrangements.
4. Update the Dynamic Programming states to represent the additional splitting choices.
5. Calculate the penalty for each valid arrangement.
6. Select the arrangement with the minimum total penalty.

## Effect on the Algorithm

The number of possible choices increases because a word can now be placed completely on a line or split into valid parts.

Dynamic Programming can still be used, but its state and transition rules must be extended to handle word fragments.

---

# 12. Remaining Scenario Questions

## Question 1: What happens if the line width changes?

The algorithm can use a different value of `W`. It must recalculate valid line arrangements and their penalties for the new width.

## Question 2: What happens if a word is longer than the maximum line width?

The current implementation cannot place that word because splitting is not supported. The input must be validated, or the algorithm must be extended to support hyphenation.

## Question 3: Why is the last line free?

The problem statement specifies that the final line has no penalty. Therefore, its cost is set to zero.

## Question 4: Why is the cubic penalty used?

The cubic penalty gives a much higher cost to lines with large unused spaces. This encourages more balanced line arrangements.

## Question 5: Why is Dynamic Programming better than Greedy?

Dynamic Programming evaluates valid alternatives and selects the minimum total penalty. Greedy makes local decisions that may not produce the globally optimal arrangement.

---

# 13. Real-World Reference

Paragraph layout and line-breaking techniques are used in many digital publishing applications.

Examples include:

- E-reader applications.
- Digital books.
- Word processors.
- Document viewers.
- Newspaper and magazine publishing systems.
- Responsive text formatting applications.

These applications arrange text according to available screen width and formatting rules.

The paragraph layout problem demonstrates how optimization algorithms can improve text presentation and readability.

---

# Presentation Details

- **Presentation Slides:** `slides.pdf`
- **Presentation Video:** [Watch Batch 11 Presentation](https://drive.google.com/file/d/1U1lMdO1MDSZbVZ2eUVc4u86fEu4gMC7p/view?usp=sharing)
- **Presentation Duration:** 8 minutes 58 seconds
- **Team Members:** Sabarinathan L, Om Arya SP, Karthick B, Tarun A, Vishal V

The presentation duration is within the maximum allowed time of 12 minutes.

**Video Access:** Ensure the Google Drive sharing permission is set to "Anyone with the link" so the evaluator can access the presentation.

---

**Project:** DAA Assignment – Batch 11  
**Scenario:** Publishing – Paragraph Layout in an E-Reader  
**Course:** 23I501 – Design and Analysis of Algorithms  
**Programming Language:** Python  
**Selected Technique:** Dynamic Programming
