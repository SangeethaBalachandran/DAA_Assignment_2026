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
| **Greedy** | Fails to guarantee an optimal solution. A greedy choice might pick a cost of 1 now, forcing a cost of 100 later. (e.g., Row 1: [1, 100], Row 2: [2, 3]. Greedy picks 1, forcing 3 = 4. Optimal is 100+2 = 102. Wait, Greedy picks 1, forcing 3. This fails when Greedy picks a locally cheap node that locks out the only cheap option for a subsequent row). |
| **Backtracking** | Explores the full $O(N!)$ state space. Without cost-based lower-bound pruning, it wastes massive time exploring permutations that are obviously mathematically suboptimal. |

## 5. Algorithm
```text
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
