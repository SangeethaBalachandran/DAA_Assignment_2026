# Batch 3 — Database Systems: Ordering Joins in a Query Optimiser

## Team

| Roll No. | Name | GitHub username | Part presented | Contribution (code, report sections) |
|---|---|---|---|---|
| 24i360 | Srikesav M | srikesav09 | Problem modelling and data structures | Problem modelling, Q1, data structure analysis, report integration |
| 24i307 | Asraf M | asrafit | Design technique identification | Technique selection, rejection of other four techniques, Q3, alternative implementation |
| 24i330 | Mazin J | 24i330 | Algorithm and correctness | Main algorithm, pseudocode, correctness proof, main implementation |
| 24i363 | Stalin K | stalinkaruna77-eng | Trace and complexity analysis | Q2, complete trace, complexity analysis, worst-case input |
| 24i368 | Tarun Kumar KPS | Username pending | Extended scenario and empirical analysis | Q4, Q5, changed requirement, benchmarking and timing results |

## Presentation

- Video link: Pending
- Duration: Pending (maximum 12:00)
- Slides: [slides.pdf](slides.pdf)

---

## 1. Problem Modelling

- **Input:**
  - A sequence of five relations: R1, R2, R3, R4 and R5.
  - Dimension array: `p = [40, 20, 30, 10, 30, 15]`.
  - Each relation Ri has dimensions `(p[i-1], p[i])`.

- **Output:**
  - The optimal parenthesisation (join order) of the five relations.
  - The minimum total join cost.

- **Objective:**
  - Minimise the total computational cost of joining all five relations.
  - The cost of joining two intermediate subchains `Ri...Rk` and `R(k+1)...Rj` is:
    `p[i-1] * p[k] * p[j]`.

- **Constraints:**
  - All five relations must be joined.
  - The original order of relations must be preserved.
  - Only adjacent subchains can be combined.
  - Join operations are associative, so different parenthesisations produce the same logical result.
  - The total cost is the sum of the costs of all intermediate joins.

- **Problem class (decision / optimisation / enumeration):**
  - **Optimisation problem**, because the objective is to find the join order that produces the minimum total cost among all possible valid parenthesisations.

- **Classical problem it maps to:**
  - **Matrix Chain Multiplication (MCM)**.
  - Similar to MCM, the problem involves finding the optimal parenthesisation of a sequence while minimising the total multiplication/join cost.
  - It can be solved using Dynamic Programming by storing the minimum cost of every possible continuous subchain.

## 2. Data Structure Analysis

| Data structure | Key operation(s) and cost | Space | Behaviour at the scale in the scenario |
|---|---|---|---|
| Chosen: Two-Dimensional Array | Access and update DP entries: O(1). Used to store and retrieve minimum costs and optimal split positions. | O(n²) | Efficiently stores all continuous subchain costs. Suitable for the given 5-table problem and moderate-sized join chains. |
| Alternative 1: Hash Map | Search, insertion and update: Average O(1), using subchain indices as keys. | O(n²) for all possible subchains | Supports memoisation, but introduces hashing overhead and is less convenient for displaying a complete DP table. |
| Alternative 2: Adjacency List | Traverse neighbouring relations: O(degree of vertex). | O(V + E) | Suitable for representing join relationships in arbitrary join graphs, but unnecessary for the given fixed chain of five relations. |

**Why the chosen structure wins:**

A two-dimensional array is the most suitable data structure because our problem requires storing the minimum join cost for every possible continuous subchain. It provides constant-time access and updates, supports bottom-up Dynamic Programming, and allows easy reconstruction of the optimal join order using a separate split table. It is simpler and more appropriate for the given chain-based problem than a hash map or adjacency list.

## 3. Design technique identification

- Technique chosen:
- Property of the problem that makes it work (with proof):

## 4. Why the other four techniques do not fit

Give concrete evidence for each: a counterexample, a subproblem count, a state-space size, or a missing bound. One-line answers such as "not efficient" earn no marks.

| Technique | Why it is unsuitable here (evidence) |
|---|---|
| | |
| | |
| | |
| | |

## 5. Algorithm

### 5.1 Selected Algorithm: Dynamic Programming

We use Dynamic Programming based on the Matrix Chain Multiplication approach to find the minimum-cost join order.

**State Definition:**

Let `m[i][j]` represent the minimum cost of joining relations Ri through Rj.

Let `s[i][j]` represent the optimal splitting position for the subchain Ri through Rj.

**Base Case:**

A single relation requires no join operation.

m[i][i] = 0

**Recurrence Relation:**

For every possible splitting position k between i and j:

m[i][j] = min { m[i][k] + m[k+1][j] + p[i-1] × p[k] × p[j] }

where i <= k < j.

**Algorithm Steps:**

1. Initialise a two-dimensional cost table `m` with zeros.
2. Initialise a split table `s` to store optimal splitting positions.
3. Consider subchains of increasing length, starting from length 2.
4. For each subchain Ri through Rj, initialise its minimum cost to infinity.
5. Try every possible splitting position k between i and j.
6. Calculate the total cost using the recurrence relation.
7. Update the minimum cost and splitting position whenever a lower cost is found.
8. After filling the table, reconstruct the optimal join order using the split table.
9. Return the minimum cost and optimal parenthesisation.

### 5.2 Pseudocode

```text
MATRIX_CHAIN_JOIN(p, n):

    Create cost table m[n][n]
    Create split table s[n][n]

    For i = 1 to n:
        m[i][i] = 0

    For length = 2 to n:

        For i = 1 to n - length + 1:

            j = i + length - 1
            m[i][j] = INFINITY

            For k = i to j - 1:

                current_cost =
                    m[i][k] +
                    m[k+1][j] +
                    p[i-1] * p[k] * p[j]

                If current_cost < m[i][j]:

                    m[i][j] = current_cost
                    s[i][j] = k

    Return m[1][n], s


CONSTRUCT_ORDER(s, i, j):

    If i == j:
        Return Ri

    k = s[i][j]

    left = CONSTRUCT_ORDER(s, i, k)
    right = CONSTRUCT_ORDER(s, k+1, j)

    Return (left JOIN right)
```
### 5.3 Optimal Join Order

For the given input:

`p = [40, 20, 30, 10, 30, 15]`

The Dynamic Programming algorithm produces:

- **Minimum join cost:** 24,500
- **Optimal join order:** `((R1 JOIN (R2 JOIN R3)) JOIN (R4 JOIN R5))`

**Individual Join Costs:**

| Join Operation | Cost |
|---|---:|
| R2 JOIN R3 | 6,000 |
| R1 JOIN (R2 JOIN R3) | 8,000 |
| R4 JOIN R5 | 4,500 |
| Final join | 6,000 |
| **Total** | **24,500** |

Therefore, the minimum total join cost is **24,500**.

## 6. Proof of Correctness

We prove that the Dynamic Programming algorithm always finds the minimum-cost join order.

### 6.1 Base Case

For a subchain containing only one relation Ri, no join operation is required.

Therefore:

m[i][i] = 0

This is the correct minimum cost for a single relation.

### 6.2 Optimal Substructure

Consider a subchain of relations Ri through Rj.

In any valid parenthesisation, the final join must divide the subchain at some position k, where i <= k < j.

This creates two smaller subchains:

- Left subchain: Ri through Rk.
- Right subchain: R(k+1) through Rj.

The total cost is:

m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j]

Suppose the left or right subchain does not have its minimum possible cost.

Replacing that subchain with its optimal parenthesisation would reduce the total cost without changing the final join dimensions.

This would contradict the assumption that the original parenthesisation was optimal.

Therefore, both subchains must also have optimal parenthesisations.

This establishes the **optimal substructure property**.

### 6.3 Inductive Proof

**Base Case:**

The algorithm correctly computes the minimum cost for a single relation because m[i][i] = 0.

**Inductive Hypothesis:**

Assume that the algorithm correctly computes the minimum join cost for all subchains of length smaller than L.

**Inductive Step:**

Consider a subchain of length L, from Ri through Rj.

The algorithm examines every possible splitting position k between i and j.

For each split, it combines:

- The optimal cost of the left subchain.
- The optimal cost of the right subchain.
- The cost of performing the final join.

By the inductive hypothesis, the costs of both smaller subchains are optimal.

Since every possible final split is examined, the algorithm selects the minimum total cost among all valid parenthesisations.

Therefore, it correctly computes the optimal cost for the subchain of length L.

By mathematical induction, the algorithm computes the minimum join cost for every subchain, including the complete chain.

### 6.4 Conclusion

The algorithm considers every possible final split and uses the optimal solutions of smaller subchains. Therefore, it always produces the minimum-cost join order.

Hence, the Dynamic Programming algorithm is correct.

## 7. Trace on the given instance

Show every intermediate table, tree level, merge step or bound. State the final answer.

## 8. Complexity analysis

- Recurrence or counting argument:
- Time (best / worst / typical):
- Space:

## 9. Worst-case input

The input you constructed, and how your algorithm behaves on it.

## 10. Implementation and empirical analysis

- Language and how to run: See [code/RUN.md](code/RUN.md)
- Input sizes used (at least five):
- Plot: ![timing plot](results/timing_plot.png)
- Does the measured growth match Section 8? Explain any deviation.
- Comparison with the rejected alternative:

## 11. Changed requirement

Answer the last question of your scenario: how the solution changes, whether the technique still holds, and the new complexity.

## 12. Answers to the remaining scenario questions

Answer each numbered question from your scenario not already covered above.

## 13. Real-world reference

One real system, library or published paper that uses this approach, and how it differs from your version. Include a link.

---

**Note:** Individual contributions are documented through the team contribution table, GitHub commit history and recorded presentation.
