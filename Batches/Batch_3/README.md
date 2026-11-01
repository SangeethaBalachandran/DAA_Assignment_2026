# Batch 3 — Database Systems: Ordering Joins in a Query Optimiser

## Team

| Roll No. | Name | GitHub username | Part presented | Contribution (code, report sections) |
|---|---|---|---|---|
| 24i360 | Srikesav M | srikesav09 | Problem modelling and data structures | Problem modelling, Q1, data structure analysis, report integration |
| 24i307 | Asraf M | asrafit | Design technique identification | Technique selection, rejection of other four techniques, Q3, alternative implementation |
| 24i330 | Mazin J | 24i330 | Algorithm and correctness | Main algorithm, pseudocode, correctness proof, main implementation |
| 24i363 | Stalin K | stalinkaruna77-eng | Trace and complexity analysis | Q2, complete trace, complexity analysis, worst-case input |
| 24i368 | Tarun Kumar KPS | tk282006-spec | Extended scenario and empirical analysis | Section 10, Section 11, Q4, Q5, Section 13, benchmarking and timing results |

## Presentation

- Video link: [Presentation](https://drive.google.com/file/d/10VfggUGEGYpmiTFiN9gBAKijLazjAprR/view?usp=drivesdk)
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

## 3. Design Technique Identification

### 3.1 Selected Technique: Dynamic Programming

Dynamic Programming is selected to solve the database join ordering problem because it avoids repeatedly calculating the same subproblems and finds the minimum-cost join order.

**Properties that make Dynamic Programming suitable:**

**1. Optimal Substructure:**

- An optimal solution for a larger subchain contains optimal solutions for its smaller subchains.
- A chain Ri through Rj can be divided at a splitting position k into two smaller subchains.
- The minimum cost of the complete subchain is obtained by combining the optimal costs of these two smaller subchains and the final join cost.
- If either smaller subchain is not optimal, replacing it with its optimal solution would reduce the total cost.

**2. Overlapping Subproblems:**

- Different parenthesisations may require the same intermediate subchains.
- For example, the subchain R2 JOIN R3 may occur in multiple possible join orders.
- Calculating the same subchain repeatedly wastes computation.
- Dynamic Programming stores the result of each subproblem in a table and reuses it whenever required.

**Conclusion:**

Dynamic Programming is suitable because the problem has optimal substructure and overlapping subproblems. It reduces repeated calculations and finds the optimal join order in O(n³) time and O(n²) space.

## 4. Why the Other Four Techniques Do Not Fit

### 4.1 Greedy Method

- The Greedy method makes a locally optimal choice at every step without considering all future consequences.
- In this problem, selecting the cheapest adjacent pair first does not always produce the globally minimum join cost.
- For the given instance, the greedy approach produces a total cost of 30,000, whereas Dynamic Programming produces 24,500.
- Therefore, the greedy-choice property does not hold.

### 4.2 Divide and Conquer

- Divide and Conquer divides a problem into smaller independent subproblems, solves them recursively and combines their results.
- In join ordering, the same subchains can occur in multiple parenthesisations.
- A straightforward recursive implementation may calculate these subchains repeatedly.
- For example, the cost of joining R2 and R3 may be recalculated in different recursive branches.
- This leads to unnecessary repeated computations and exponential growth in the number of recursive possibilities.
- Dynamic Programming avoids this by storing and reusing calculated subproblem results.

### 4.3 Backtracking

- Backtracking explores possible join orders by constructing different parenthesisations.
- It may need to examine every possible valid parenthesisation to guarantee the optimal result.
- The number of possible join orders is given by Catalan numbers.
- For 5 tables, there are 14 possible join orders.
- For 15 tables, there are 2,674,440 possible join orders.
- Therefore, exhaustive backtracking becomes expensive as the number of tables increases.

### 4.4 Branch and Bound

- Branch and Bound explores possible solutions and prunes partial solutions using a lower bound.
- It can reduce the search space when strong lower bounds are available.
- However, for this chain problem, weak bounds may fail to eliminate many partial join orders.
- Its worst-case running time remains exponential.
- Dynamic Programming is more suitable because it systematically solves all required subchains in polynomial time.

**Conclusion:**

Dynamic Programming is preferred because it uses optimal substructure and overlapping subproblems to avoid repeated calculations. Greedy may produce a non-optimal result, Divide and Conquer repeats subproblems, Backtracking explores an exponentially growing search space, and Branch and Bound may still require exponential exploration.

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

We use Dynamic Programming to calculate the minimum join cost for every possible continuous subchain.

**Given input:**

`p = [40, 20, 30, 10, 30, 15]`

There are five relations:

| Relation | Dimensions |
|---|---|
| R1 | 40 × 20 |
| R2 | 20 × 30 |
| R3 | 30 × 10 |
| R4 | 10 × 30 |
| R5 | 30 × 15 |

### Step 1: Initialise the DP table

Let `m[i][j]` represent the minimum cost of joining relations Ri through Rj.

For a single relation, no join is required.

`m[i][i] = 0`

### Step 2: Calculate costs for subchains of length 2

Using the formula:

`Cost = p[i-1] × p[k] × p[j]`

| Subchain | Calculation | Minimum Cost |
|---|---|---:|
| R1 JOIN R2 | 40 × 20 × 30 | 24,000 |
| R2 JOIN R3 | 20 × 30 × 10 | 6,000 |
| R3 JOIN R4 | 30 × 10 × 30 | 9,000 |
| R4 JOIN R5 | 10 × 30 × 15 | 4,500 |

### Step 3: Calculate costs for subchains of length 3

**For R1 to R3:**

| Splitting Position | Calculation | Total Cost |
|---|---|---:|
| R1 \| (R2 JOIN R3) | 0 + 6,000 + (40 × 20 × 10) | 14,000 |
| (R1 JOIN R2) \| R3 | 24,000 + 0 + (40 × 30 × 10) | 36,000 |

Minimum cost = **14,000**

Optimal order: `R1 JOIN (R2 JOIN R3)`

**For R2 to R4:**

| Splitting Position | Calculation | Total Cost |
|---|---|---:|
| R2 \| (R3 JOIN R4) | 0 + 9,000 + (20 × 30 × 30) | 27,000 |
| (R2 JOIN R3) \| R4 | 6,000 + 0 + (20 × 10 × 30) | 12,000 |

Minimum cost = **12,000**

Optimal order: `(R2 JOIN R3) JOIN R4`

**For R3 to R5:**

| Splitting Position | Calculation | Total Cost |
|---|---|---:|
| R3 \| (R4 JOIN R5) | 0 + 4,500 + (30 × 10 × 15) | 9,000 |
| (R3 JOIN R4) \| R5 | 9,000 + 0 + (30 × 30 × 15) | 22,500 |

Minimum cost = **9,000**

Optimal order: `R3 JOIN (R4 JOIN R5)`

### Step 4: Calculate costs for subchains of length 4

**For R1 to R4:**

| Splitting Position | Calculation | Total Cost |
|---|---|---:|
| R1 \| (R2...R4) | 0 + 12,000 + (40 × 20 × 30) | 36,000 |
| (R1...R2) \| (R3...R4) | 24,000 + 9,000 + (40 × 30 × 30) | 69,000 |
| (R1...R3) \| R4 | 14,000 + 0 + (40 × 10 × 30) | 26,000 |

Minimum cost = **26,000**

Optimal order: `(R1 JOIN (R2 JOIN R3)) JOIN R4`

**For R2 to R5:**

| Splitting Position | Calculation | Total Cost |
|---|---|---:|
| R2 \| (R3...R5) | 0 + 9,000 + (20 × 30 × 15) | 18,000 |
| (R2...R3) \| (R4...R5) | 6,000 + 4,500 + (20 × 10 × 15) | 13,500 |
| (R2...R4) \| R5 | 12,000 + 0 + (20 × 30 × 15) | 21,000 |

Minimum cost = **13,500**

Optimal order: `(R2 JOIN R3) JOIN (R4 JOIN R5)`

### Step 5: Calculate the cost for the complete chain

For R1 to R5, all four possible splitting positions are evaluated.

| Splitting Position | Calculation | Total Cost |
|---|---|---:|
| R1 \| (R2...R5) | 0 + 13,500 + (40 × 20 × 15) | 25,500 |
| (R1...R2) \| (R3...R5) | 24,000 + 9,000 + (40 × 30 × 15) | 51,000 |
| (R1...R3) \| (R4...R5) | 14,000 + 4,500 + (40 × 10 × 15) | 24,500 |
| (R1...R4) \| R5 | 26,000 + 0 + (40 × 30 × 15) | 44,000 |

Minimum cost = **24,500**

Optimal splitting position: Between R3 and R4.

### Step 6: Final DP Cost Table

| DP State | R1 | R2 | R3 | R4 | R5 |
|---|---:|---:|---:|---:|---:|
| R1 | 0 | 24,000 | 14,000 | 26,000 | 24,500 |
| R2 | - | 0 | 6,000 | 12,000 | 13,500 |
| R3 | - | - | 0 | 9,000 | 9,000 |
| R4 | - | - | - | 0 | 4,500 |
| R5 | - | - | - | - | 0 |

### Step 7: Reconstruct the optimal join order

From the split table:

1. Join R2 and R3 first: Cost = 6,000.
2. Join R1 with the result of R2 JOIN R3: Cost = 8,000.
3. Join R4 and R5: Cost = 4,500.
4. Join the two resulting intermediate relations: Cost = 6,000.

**Final Optimal Join Order:**

`((R1 JOIN (R2 JOIN R3)) JOIN (R4 JOIN R5))`

**Total Minimum Join Cost:**

`6,000 + 8,000 + 4,500 + 6,000 = 24,500`

Therefore, the minimum join cost is **24,500**.

## 8. Complexity Analysis

### 8.1 Time Complexity

The Dynamic Programming algorithm calculates the minimum cost for every possible continuous subchain.

Let n represent the number of relations.

The algorithm uses three nested loops:

1. The outer loop considers subchain lengths from 2 to n.
2. The second loop selects the starting position of each subchain.
3. The innermost loop examines every possible splitting position.

The total number of split evaluations is:

`Σ (n - L + 1)(L - 1)`, for L = 2 to n.

This summation grows proportionally to n³.

Therefore, the time complexity is:

**O(n³)**

### 8.2 Space Complexity

The algorithm uses two n × n tables:

- Cost table `m[n][n]` stores minimum join costs.
- Split table `s[n][n]` stores optimal splitting positions.

Each table requires O(n²) space.

Therefore, the total space complexity is:

**O(n²)**

### 8.3 Best, Worst and Practical Cases

| Case | Time Complexity | Explanation |
|---|---|---|
| Best Case | O(n³) | Every possible splitting position is still evaluated, even if a good solution is found early. |
| Average Case | O(n³) | The number of subchains and splitting positions depends on n. |
| Worst Case | O(n³) | All possible splitting positions are evaluated for every subchain. |

**Practical Behaviour:**

- For a small number of relations, Dynamic Programming computes the optimal join order efficiently.
- As the number of relations increases, the number of DP states and split evaluations increases.
- The algorithm is much more efficient than enumerating all Catalan-number parenthesisations.
- For larger join graphs, the chain-based DP approach must be extended, and its complexity can increase significantly.

**Conclusion:**

Dynamic Programming solves the chain-based join ordering problem in O(n³) time and O(n²) space. Its polynomial complexity makes it more scalable than exhaustive enumeration for this scenario.

## 9. Worst-Case Input

### 9.1 Constructed Input

Consider a chain of `n` relations where all dimensions are equal:

`p = [10, 10, 10, ..., 10]`

For five relations:

`p = [10, 10, 10, 10, 10, 10]`

This input creates multiple equally optimal parenthesisations. However, the worst-case running time of the algorithm is determined by the number of relations and the number of possible split positions, not by the dimension values.

### 9.2 Worst-Case Behaviour of the Algorithm

The Dynamic Programming algorithm considers every possible continuous subchain and evaluates every valid splitting position.

For a chain containing `n` relations:

- Number of DP states: `n(n+1)/2 = O(n²)`.
- Each state may examine up to `n-1` splitting positions.
- Total split evaluations:

\[
\sum_{l=2}^{n}(n-l+1)(l-1)
=\frac{n(n-1)(n+1)}{6}
\]

Therefore, the algorithm performs **O(n³) time** and requires **O(n²) space**.

For five relations, the number of split evaluations is:

\[
\frac{5(5-1)(5+1)}{6}=20
\]

The algorithm evaluates all 20 possible split positions, even when multiple splits produce the same minimum cost.

### 9.3 DP Cost Table for the Constructed Input

For equal dimensions, every individual join costs:

`10 × 10 × 10 = 1,000`

**Subchains of length 2:**

| Join | Cost |
|---|---:|
| R1 JOIN R2 | 1,000 |
| R2 JOIN R3 | 1,000 |
| R3 JOIN R4 | 1,000 |
| R4 JOIN R5 | 1,000 |

**Subchains of length 3:**

Every parenthesisation requires two joins.

Minimum cost = 2 × 1,000 = **2,000**

**Subchains of length 4:**

Every parenthesisation requires three joins.

Minimum cost = 3 × 1,000 = **3,000**

**Complete chain of five relations:**

Every parenthesisation requires four joins.

Minimum cost = 4 × 1,000 = **4,000**

| DP State | R1 | R2 | R3 | R4 | R5 |
|---|---:|---:|---:|---:|---:|
| R1 | 0 | 1,000 | 2,000 | 3,000 | 4,000 |
| R2 | - | 0 | 1,000 | 2,000 | 3,000 |
| R3 | - | - | 0 | 1,000 | 2,000 |
| R4 | - | - | - | 0 | 1,000 |
| R5 | - | - | - | - | 0 |

### 9.4 Worst-Case Complexity

- **Time Complexity:** O(n³), because every possible split position is evaluated for every subchain.
- **Space Complexity:** O(n²), because the cost and split tables store results for all continuous subchains.
- **Worst-case behaviour:** The algorithm performs all possible split evaluations without skipping any based on the input dimensions.

**Conclusion:**

The constructed equal-dimension input demonstrates a tie-heavy case in which multiple parenthesisations have the same optimal cost. The algorithm still evaluates all possible split positions. Its worst-case time complexity remains O(n³), and its space complexity remains O(n²). The number of operations is determined by the number of relations, not by whether their dimensions are equal or different.

## 10. Empirical Analysis

### Experimental Setup

- Both Dynamic Programming and Greedy algorithms were tested.
- Input sizes were varied from 5 to 25 relations.
- Each algorithm was executed 5 times for every input size.
- Median execution time was used to reduce timing variations.

### Benchmark Results

The following table shows the median execution times and total join costs measured over 5 repetitions for each input size.

| Number of Relations | DP Time (seconds) | Greedy Time (seconds) | DP Cost | Greedy Cost |
|---:|---:|---:|---:|---:|
| 5 | 0.0000198 | 0.0000099 | 375,282 | 959,970 |
| 10 | 0.0000954 | 0.0000243 | 293,692 | 747,738 |
| 15 | 0.0002899 | 0.0000495 | 540,264 | 788,322 |
| 20 | 0.0009720 | 0.0001235 | 527,400 | 2,174,615 |
| 25 | 0.0018837 | 0.0001787 | 895,362 | 1,365,253 |

### Observations

- Both algorithms show increasing execution time as the number of relations increases.
- Greedy executes faster than Dynamic Programming for all tested input sizes.
- Dynamic Programming produces a lower join cost than Greedy for all five tested inputs.
- The performance difference demonstrates the trade-off between execution speed and optimality.

### Comparison with Theoretical Complexity

- Dynamic Programming has a theoretical time complexity of O(n³).
- Its measured execution time increases as the number of relations increases.
- The observed growth is broadly consistent with the cubic complexity, although small input sizes and system timing variations affect the measurements.
- The Greedy implementation is faster in these experiments, but it does not guarantee the optimal join cost.

### Performance Plot

The execution-time comparison is represented in `results/timing_plot.png`.

---

## 11. Changed Requirement

### Requirement: Handling Arbitrary Join Graphs

The original problem considers relations arranged in a linear chain. Consider a changed requirement where relations can form an arbitrary join graph.

- A linear-chain DP solution cannot directly handle every possible join relationship.
- Subset Dynamic Programming can represent groups of relations using bitmasks.
- Each subset stores the minimum cost of producing that group of relations.
- Valid partitions are evaluated to determine the minimum-cost join plan.
- Only connected subsets and partitions with valid join predicates should be considered when constructing join plans.

### Modified Approach

Let S represent a subset of relations.

- DP[S] stores the minimum cost of joining all relations in subset S.
- Divide S into two non-empty valid subsets A and B.
- Calculate DP[A] + DP[B] + JoinCost(A, B).
- Choose the partition with the minimum total cost.

### Complexity

- Time Complexity: O(3ⁿ)
- Space Complexity: O(2ⁿ)

The subset-based approach supports arbitrary join graphs but becomes computationally expensive as the number of relations increases.

---
## 12. Remaining Scenario Questions

### Q1. Count the possible join orders for 5 tables and 15 tables. Why is trying them all impractical?

The number of possible ways to fully parenthesise a chain of n relations is given by the Catalan number C(n-1).

**Catalan Number Formula:**

C(m) = (1 / (m + 1)) × (2m)! / (m! × m!)

**For 5 tables:**

- Number of relations = 5
- Possible join orders = C(5 - 1) = C(4)
- C(4) = 14

Therefore, there are **14 possible join orders** for 5 tables.

**For 15 tables:**

- Number of relations = 15
- Possible join orders = C(15 - 1) = C(14)
- C(14) = 2,674,440

Therefore, there are **2,674,440 possible join orders** for 15 tables.

**Comparison:**

| Number of Tables | Possible Join Orders |
|---|---:|
| 5 | 14 |
| 10 | 4,862 |
| 12 | 58,786 |
| 15 | 2,674,440 |

**Why is enumeration impractical?**

- The number of possible join orders grows rapidly according to Catalan numbers.
- Every possible parenthesisation must be generated and evaluated.
- The cost of every join order must be calculated and compared.
- As the number of tables increases, the computational effort becomes very high.
- For 15 tables alone, more than 2.6 million possible join orders must be considered.

**Conclusion:**

Enumerating all possible join orders becomes computationally expensive as the number of tables increases. Dynamic Programming avoids repeatedly solving the same subproblems and finds the optimal join order in O(n³) time and O(n²) space for a chain of n relations.

### Q2. Find the cheapest join order and its cost for the instance, showing every intermediate result your method computes.

**Given input:**

`p = [40, 20, 30, 10, 30, 15]`

The Dynamic Programming algorithm evaluates every continuous subchain and stores its minimum join cost.

**Intermediate Results:**

| Subchain | Minimum Cost | Optimal Parenthesisation |
|---|---:|---|
| R1 to R2 | 24,000 | R1 JOIN R2 |
| R2 to R3 | 6,000 | R2 JOIN R3 |
| R3 to R4 | 9,000 | R3 JOIN R4 |
| R4 to R5 | 4,500 | R4 JOIN R5 |
| R1 to R3 | 14,000 | R1 JOIN (R2 JOIN R3) |
| R2 to R4 | 12,000 | (R2 JOIN R3) JOIN R4 |
| R3 to R5 | 9,000 | R3 JOIN (R4 JOIN R5) |
| R1 to R4 | 26,000 | (R1 JOIN (R2 JOIN R3)) JOIN R4 |
| R2 to R5 | 13,500 | (R2 JOIN R3) JOIN (R4 JOIN R5) |
| R1 to R5 | 24,500 | ((R1 JOIN (R2 JOIN R3)) JOIN (R4 JOIN R5)) |

**Optimal Join Operations:**

| Step | Join Operation | Intermediate Dimensions | Join Cost |
|---|---|---|---:|
| 1 | R2 JOIN R3 | 20 × 10 | 6,000 |
| 2 | R1 JOIN (R2 JOIN R3) | 40 × 10 | 8,000 |
| 3 | R4 JOIN R5 | 10 × 15 | 4,500 |
| 4 | Combine the two intermediate results | 40 × 15 | 6,000 |

**Total Minimum Cost:**

= 6,000 + 8,000 + 4,500 + 6,000

= **24,500**

**Final Answer:**

- **Cheapest join order:** `((R1 JOIN (R2 JOIN R3)) JOIN (R4 JOIN R5))`
- **Minimum total join cost:** `24,500`

The Dynamic Programming algorithm finds this result by evaluating all possible splitting positions and retaining the minimum cost for each subchain.

### Q3. A colleague proposes: "Always join the cheapest adjacent pair first." Evaluate this approach on the given instance.

The proposed approach is a Greedy algorithm. It repeatedly selects the adjacent pair with the lowest immediate join cost.

**Given input:**

`p = [40, 20, 30, 10, 30, 15]`

**Step 1: Calculate initial adjacent join costs.**

| Adjacent Join | Cost |
|---|---:|
| R1 JOIN R2 | 40 × 20 × 30 = 24,000 |
| R2 JOIN R3 | 20 × 30 × 10 = 6,000 |
| R3 JOIN R4 | 30 × 10 × 30 = 9,000 |
| R4 JOIN R5 | 10 × 30 × 15 = 4,500 |

The cheapest adjacent pair is R4 JOIN R5.

Cost = 4,500.

**Step 2: Join the remaining cheapest adjacent pair.**

After joining R4 and R5, the remaining groups are:

R1, R2, R3, (R4 JOIN R5)

The adjacent join costs are:

| Adjacent Join | Cost |
|---|---:|
| R1 JOIN R2 | 24,000 |
| R2 JOIN R3 | 6,000 |
| R3 JOIN (R4 JOIN R5) | 30 × 10 × 15 = 4,500 |

The cheapest pair is R3 JOIN (R4 JOIN R5).

Cost = 4,500.

**Step 3: Join the remaining cheapest adjacent pair.**

The remaining groups are:

R1, R2, (R3 JOIN R4 JOIN R5)

| Adjacent Join | Cost |
|---|---:|
| R1 JOIN R2 | 24,000 |
| R2 JOIN (R3 JOIN R4 JOIN R5) | 20 × 30 × 15 = 9,000 |

The cheapest pair is R2 JOIN (R3 JOIN R4 JOIN R5).

Cost = 9,000.

**Step 4: Perform the final join.**

The remaining groups are:

R1, (R2 JOIN R3 JOIN R4 JOIN R5)

Final join cost:

40 × 20 × 15 = 12,000

**Total Greedy Cost:**

= 4,500 + 4,500 + 9,000 + 12,000

= **30,000**

**Comparison with Dynamic Programming:**

| Approach | Total Join Cost |
|---|---:|
| Greedy | 30,000 |
| Dynamic Programming | 24,500 |

Difference = 30,000 - 24,500 = 5,500.

The Greedy approach produces a cost that is approximately 22.45% higher than the optimal cost.

**Conclusion:**

The Greedy approach does not guarantee the globally optimal join order because choosing the cheapest immediate adjacent pair may lead to expensive future joins. Dynamic Programming is better because it evaluates all possible splitting positions and guarantees the minimum total join cost for the given chain.

### Q4. How can Dynamic Programming be extended to handle arbitrary join graphs instead of a linear chain?

**Answer:**

- Represent each subset of relations using a bitmask.
- Maintain a DP table where DP[S] stores the minimum cost of joining subset S.
- Enumerate valid partitions of S into two smaller subsets.
- Select the partition with the minimum combined join cost.

The subset DP approach has O(3ⁿ) time complexity and O(2ⁿ) space complexity under a constant-time split-cost model.

### Q5. Can Branch and Bound replace Genetic Query Optimisation for a large number of relations?

**Answer:**

- Branch and Bound explores possible join orders while maintaining the best complete solution.
- It prunes partial solutions whose lower bound cannot improve the current best solution.
- It can find an optimal solution if the search is completed with valid bounds.
- Its worst-case time complexity remains exponential, so it cannot always replace Genetic Query Optimisation for large queries.

Branch and Bound is useful when effective bounds allow substantial pruning, whereas Genetic Query Optimisation provides a heuristic search strategy for reducing planning time.

---

## 13. Real-World Application

### PostgreSQL Genetic Query Optimiser (GEQO)

PostgreSQL uses a Genetic Query Optimiser (GEQO) to plan queries involving a large number of relations.

- GEQO uses heuristic search to reduce query-planning time.
- It is designed for complex queries involving many relations.
- It may produce plans that are not globally optimal.
- The default `geqo_threshold` is 12 relations.

### Connection to Our Problem

- Join ordering is an important part of database query optimisation.
- Dynamic Programming finds optimal join orders for manageable problem sizes.
- Exhaustive search becomes expensive as the number of relations increases.
- PostgreSQL uses GEQO to manage planning time for larger queries.

**Reference:**

PostgreSQL Official Documentation – Genetic Query Optimizer

https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-GEQO-THRESHOLD

---

**Note:** Individual contributions are documented through the team contribution table, GitHub commit history and recorded presentation.
