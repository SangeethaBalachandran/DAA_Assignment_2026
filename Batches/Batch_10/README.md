# Batch 10 — Field service: Assigning technicians to tickets

## Team
| Roll No. | Name | GitHub username | Part presented | Contribution (code, report sections) |
| --- | --- | --- | --- | --- |
| 24I362 | Sriram A | srii-noir | Problem Modelling, Algorithm | Branch & Bound solution, Master Compilation |
| 24I344 | Purushothaman S | purushoths3004 | Alternative, Complexity | Greedy implementation, Input generation |
| 24I340 | Praveen Kumaran | PraveenKumaran12 | Trace, Empirics | Documentation, Timing analysis & Plotting |

## Presentation
- **Video link:** https://drive.google.com/file/d/1_x5O0_69i6G-3phNrqo_w2wwql-n_DLY/view?usp=sharing
- **Duration:** 07:51 (maximum 12:00)
- **Slides:** `slides.pdf`

## 1. Problem modelling
- **Input:** An $N \times N$ cost matrix where $M[i][j]$ represents the cost of assigning technician $i$ to ticket $j$.
- **Output:** An array of length $N$ mapping each technician to exactly one unique ticket to minimize total cost.
- **Objective:** Minimize the sum of the assignment costs.
- **Constraints:** 1 technician per ticket, 1 ticket per technician. All costs $\ge 0$.
- **Problem class:** Optimisation
- **Classical problem it maps to:** The Assignment Problem / Job Assignment Problem

## 2. Data structure analysis
| Data structure | Key operation(s) and cost | Space | Behaviour at the scale in the scenario |
| --- | --- | --- | --- |
| **Chosen:** Priority Queue (Min-Heap) | `insert`: $O(\log V)$, `extract_min`: $O(\log V)$ | $O(V)$ where $V$ is active nodes | Efficiently retrieves the most promising partial assignment (lowest bound). |
| **Alternative 1:** Simple Array/List | `insert`: $O(1)$, `search_min`: $O(V)$ | $O(V)$ | Too slow to find the minimum bound at every step as the state space grows. |
| **Alternative 2:** Stack (DFS) | `push`/`pop`: $O(1)$ | $O(N)$ | Uses less memory, but explores deep inefficient paths without evaluating global best first. |

**Why the chosen structure wins:** Least-Cost Branch and Bound (LCBB) requires repeatedly expanding the node with the lowest lower bound. A Min-Heap ensures we get this node in logarithmic time, vastly speeding up the search compared to a linear array scan.

## 3. Design technique identification
- **Technique chosen:** Branch and Bound
- **Property of the problem that makes it work (with proof):** The cost function is monotonically increasing. Proof: Since all edge costs (technician to ticket) are non-negative, adding a new assignment to a partial solution can only keep the cost the same or increase it. Therefore, a valid lower bound can be calculated, allowing us to safely prune paths that exceed our current best full solution.

## 4. Why the other four techniques do not fit
| Technique | Why it is unsuitable here (evidence) |
| --- | --- |
| **Divide and Conquer** | Subproblems overlap. Assigning Technician 1 to Ticket A restricts the available tickets for all other technicians, violating the independent subproblem requirement. |
| **Dynamic Programming** | The state space is $O(2^N)$ subsets of assigned tickets. For large $N$, this requires massive memory for memoization tables, whereas B&B prunes unpromising states early. |
| **Greedy** | Fails to guarantee an optimal solution. A greedy choice might pick a cost of 1 now, forcing a cost of 100 later. |
| **Backtracking** | Explores the full $O(N!)$ state space. Without cost-based lower-bound pruning, it wastes massive time exploring permutations that are obviously mathematically suboptimal. |

## 5. Algorithm
    Algorithm AssignTickets(CostMatrix, N):
        Initialize PriorityQueue PQ
        RootNode = create_node(level=0, cost=0, reduced_matrix)
        RootNode.bound = calculate_lower_bound(RootNode.matrix)
        PQ.push(RootNode)
        GlobalMin = INFINITY
        
        while PQ is not empty:
            Current = PQ.extract_min()
            if Current.bound >= GlobalMin: 
                continue // Pruning rule
                
            if Current.level == N:
                GlobalMin = min(GlobalMin, Current.cost)
                continue
                
            for each unassigned ticket J:
                Child = create_node(level=Current.level + 1, assign J)
                Child.bound = calculate_lower_bound(Child.matrix)
                if Child.bound < GlobalMin:
                    PQ.push(Child) // Selection rule

## 6. Proof of correctness
**Proof that pruning never discards an optimal solution:** 
The lower bound for any node is computed by reducing rows and columns (subtracting the minimum from each). This sum of minimums represents the absolute minimum cost to complete the remaining assignments. Because costs are $\ge 0$, any full assignment derived from this node will have a cost $C \ge \text{LowerBound}$. If $\text{LowerBound} \ge \text{GlobalMin}$ (the best complete assignment found so far), then $C \ge \text{GlobalMin}$. Therefore, no better solution can exist down this branch, and it is mathematically safe to prune it.

## 7. Trace on the given instance
**Matrix:**
[11, 4, 9, 7]
[ 8, 6, 5, 10]
[ 7, 10, 3, 9]
[ 9, 8, 11, 6]

**Step 1: Root Node Reduction (Level 0)**
- Row minimums: R1=4, R2=5, R3=3, R4=6. (Sum = 18).
- Subtract row mins: 
  [7, 0, 5, 3]
  [3, 1, 0, 5]
  [4, 7, 0, 6]
  [3, 2, 5, 0]
- Column minimums of new matrix: C1=3, C2=0, C3=0, C4=0. (Sum = 3).
- Subtract col mins (C1-3):
  [4, 0, 5, 3]
  [0, 1, 0, 5]
  [1, 7, 0, 6]
  [0, 2, 5, 0]
- **Root Lower Bound** = 18 + 3 = **21**.

**Step 2: Assignment & Result**
Looking at the reduced matrix, we can assign zeroes without conflict:
- Tech 1 -> Ticket 2 (Cost 4)
- Tech 2 -> Ticket 1 (Cost 8)
- Tech 3 -> Ticket 3 (Cost 3)
- Tech 4 -> Ticket 4 (Cost 6)
- **Total Cost:** 4 + 8 + 3 + 6 = **21**.
Since this valid assignment exactly matches the root lower bound, it is mathematically proven to be the absolute minimum. Final answer: `[Ticket 2, Ticket 1, Ticket 3, Ticket 4]` with a cost of 21.

## 8. Complexity analysis
- **Recurrence or counting argument:** The state space tree has $N!$ leaves. In the worst case, if no pruning occurs, we generate $N + N(N-1) + ... + N!$ nodes. 
- **Time:** 
  - Best/Typical: $O(N^3)$ (heavy pruning effectively drives the search down a single path).
  - Worst: $O(N^3 \cdot N!)$ (matrix reduction is $O(N^2)$ at each of the $N!$ nodes).
- **Space:** $O(N^2 \cdot N!)$ in the absolute worst case to store the reduced matrices in the priority queue.

## 9. Worst-case input
An input matrix where all entries are identical (e.g., all 1s). The lower bound will be identical for every single branch, meaning the Priority Queue cannot distinguish promising paths from unpromising ones. The algorithm degrades to pure Backtracking, exploring the entire $O(N!)$ tree before confirming the solution.

## 10. Implementation and empirical analysis
- **Language and how to run:** Python. See `code/RUN.md`.
- **Input sizes used:** $N = 4, 8, 10, 12, 14, 15$.
- **Plot:** See `results/timing_plot.png`.
- **Does the measured growth match Section 8?** Yes. For random inputs, the time grows smoothly rather than factorially, proving that LCBB pruning is highly effective in the typical case.
- **Comparison with the rejected alternative:** Purushothaman implemented the Greedy approach. The Greedy code runs in $O(N^2)$ time and is drastically faster than B&B on large datasets, but the solutions generated are frequently 15% - 30% more expensive than the optimal solution found by Branch & Bound.

## 11. Changed requirement
*Scenario Question: What if a technician can handle up to two tickets?*
The solution changes to a variant of the General Assignment Problem. The state definition must track the capacity of each technician. The Branch & Bound technique still holds, but the matrix must be expanded (cloning each technician row twice) or the constraints relaxed. The complexity remains $O(N!)$ worst-case but the constant factor increases due to a vastly larger state space. 

## 12. Answers to the remaining scenario questions
*(No additional scenario questions provided for Batch 10).*

## 13. Real-world reference
**The Hungarian Algorithm (scipy.optimize.linear_sum_assignment)**
In real-world Python applications, B&B is rarely used for the pure Assignment Problem because the Hungarian Algorithm solves it optimally in polynomial $O(N^3)$ time. The Scipy library uses this algorithm for tasks like multi-object tracking (assigning current bounding boxes to past track IDs). 
- Link: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html
