# Batch 11 – Publishing: Paragraph Layout in an E-reader

**Course:** Design and Analysis of Algorithms  
**Language:** Python  
**Chosen algorithm:** Dynamic Programming  
**Rejected alternative:** Next-fit Greedy  
**Team size:** 5

## Problem statement

An e-reader lays out a paragraph into lines of maximum width `W`. A non-final
line has penalty `(unused spaces)^3`; the final line is free. The goal is to
minimize the total penalty. The supplied instance has `W = 16` and the text:

> A clear model of the problem is half of the final answer

## 1. Greedy layout and optimal layout

The greedy baseline fills each line with as many consecutive words as possible.

| Line | Greedy words | Used | Unused | Penalty |
|---|---|---:|---:|---:|
| 1 | A clear model of | 16 | 0 | 0 |
| 2 | the problem is | 14 | 2 | 8 |
| 3 | half of the | 11 | 5 | 125 |
| 4 | final answer | 12 | 4 | 0 (final line) |

Greedy total: `0 + 8 + 125 + 0 = 133`.

The optimal DP layout is:

| Line | Words | Used | Unused | Penalty |
|---|---|---:|---:|---:|
| 1 | A clear model | 13 | 3 | 27 |
| 2 | of the problem | 14 | 2 | 8 |
| 3 | is half of the | 14 | 2 | 8 |
| 4 | final answer | 12 | 4 | 0 (final line) |

Optimal total: `27 + 8 + 8 + 0 = 43`.

Therefore, for this instance, DP improves the penalty from 133 to 43.

## 2. Proof of optimality

Let `DP[j]` be the minimum penalty for laying out the first `j` words.
Set `DP[0] = 0`. If the final line of a layout of the first `j` words begins
at word `i`, then its preceding prefix consists of words `1` through `i-1`.
The cost for this choice is `DP[i-1] + Cost(i,j)`.

Thus:

`DP[j] = min(DP[i-1] + Cost(i,j))`

over all `i` for which words `i` through `j` fit. If `j` is the final word,
the line cost is zero.

**Induction:** The empty prefix is optimal. Assume all shorter prefixes have
optimal DP values. Any valid layout ending at `j` has some final-line start
`i`; its preceding prefix must be optimal, or replacing it with a better
prefix would improve the whole layout. The recurrence checks every feasible
`i` and selects the least combined cost. Hence `DP[j]` is optimal. By
induction, `DP[n]` is optimal.

## 3. Linear versus cubic penalty

For a linear penalty, the cost of a non-final line is its unused width.
For any fixed number of lines, total unused width is determined by the
total width of the non-final lines. Greedy packing pushes as much text as
possible into the earliest lines and leaves the shortest possible suffix for
the free final line; it therefore minimizes the linear total.

For a cubic penalty, a large gap is much more expensive than several small
gaps: for example, 8 unused spaces cost `512`, while 4 unused spaces cost
`64`. Redistributing words can reduce the sum of cubes. Greedy makes each
line locally full but does not account for the effect on later lines, so it
is not guaranteed to minimize the cubic total. DP is required for a guarantee.

## 4. Time and space complexity; O(1) line cost

Let `n` be the number of words. For each endpoint `j`, scan backward over
candidate start positions `i` until the line exceeds width `W`. Since each
word uses at least one character and words require separating spaces, only
`O(W)` words can fit. There are `n` DP states and `O(W)` transitions per
state, giving `O(nW)` time.

Build prefix sums:

`Prefix[0] = 0`  
`Prefix[k] = Prefix[k-1] + length(word[k])`

Then:

`L(i,j) = Prefix[j] - Prefix[i-1] + (j-i)`

This is the character count of words `i..j`, including spaces, and takes
`O(1)` time. The algorithm stores only prefix, DP and parent arrays, so
auxiliary space is `O(n)`; no `n × n` matrix is stored.

## 5. Hyphenation and paragraph editing

At each marked hyphenation point, create an additional legal break option.
A line ending at such a point includes a printed hyphen and incurs an
additional fixed cost of 50. The DP considers both ordinary word boundaries
and permitted hyphenation breaks. Each candidate's total cost is the
whitespace penalty (zero for the final line), plus 50 if it ends in an
inserted hyphen, plus the best cost of the preceding text.

Paragraphs can be laid out independently. After an edit, recompute the
edited paragraph only. If its height changes, update subsequent page
positions/pagination as needed; the unchanged paragraphs' optimal layouts
do not need to be recomputed.

## Complexity summary

| Measure | Complexity |
|---|---|
| Time | `O(nW)` |
| Auxiliary space | `O(n)` |
| One line-cost query | `O(1)` |

## Five-member work split

| Member | Assigned section | Deliverable |
|---|---|---|
| Member 1 | Question 1 | Greedy and optimal layouts with calculations |
| Member 2 | Question 2 | Induction proof of optimality |
| Member 3 | Question 3 | Linear versus cubic penalty explanation |
| Member 4 | Question 4 | Complexity, prefix sums, implementation and benchmark |
| Member 5 | Question 5 | Hyphenation extension and paragraph editing |

All members should understand the problem statement, recurrence, and final
complexity before presentation.

## Reproducibility

See `code/RUN.md` for exact commands. Timing measurements are machine- and
Python-version-dependent; `results/timing.csv` and `results/timing_plot.png`
are generated by the benchmark script and are illustrative measurements,
not a universal 300 ms guarantee.
