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

## 2. Data structure analysis

| Data structure | Key operation(s) and cost | Space | Behaviour at the scale in the scenario |
|---|---|---|---|
| Chosen: | | | |
| Alternative 1: | | | |
| Alternative 2: | | | |

**Why the chosen structure wins:**

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

Pseudocode, with the state definition / recurrence / selection rule / pruning or bounding rule as applicable.

```text

```

## 6. Proof of correctness

Exchange argument, induction, loop invariant, or proof that pruning never discards an optimal solution.

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