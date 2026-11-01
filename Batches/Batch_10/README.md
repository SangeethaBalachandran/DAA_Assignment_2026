# Batch 10 - Field service: Assigning technicians to tickets

**Course:** 23I501 Design and Analysis of Algorithms, PSG College of Technology

**Members:**
- Member 1: Sriram A - 24I362 - GitHub: `srii-noir`
- Member 2: Purushothaman S - 24I344 - GitHub: `purushoths3004`
- Member 3: Praveen Kumaran - 24I340 - GitHub: `praveen1204062028`

**Presentation video:** (https://drive.google.com/file/d/1_x5O0_69i6G-3phNrqo_w2wwql-n_DLY/view?usp=sharing)
**NOTE:** DOWNLOAD THIS AND LISTEN IN POWERPOINT
**Chosen technique:** Branch and Bound with row-reduction lower bounding.

**Rejected techniques:** Greedy, Dynamic Programming, Divide and Conquer, Backtracking.

## 0. Contribution table

| Member (name, roll no., GitHub) | Files committed | README sections | Slides | Video part |
|---|---|---|---|---|
| Member 1: Sriram A (24I362, srii-noir) | `code/main_solution.py`, `slides.pdf` | 1, 2, 3, 5 | 1-3, 5 | Problem model, data structures, why Branch & Bound, algorithm demo |
| Member 2: Purushothaman S (24I344, purushoths3004) | `code/rejected_alternative.py`, `code/generate_inputs.py` | 4, 7, 8, 9 | 4, 6, 7 | Rejecting other techniques, Greedy counterexample, Timing analysis |
| Member 3: Praveen Kumaran (24I340, praveen1204062028) | `README.md`, `results/*` | 6, 10, 11, 12 | 8, 9, 10 | Trace, Proof of correctness, Complex constraints (Q5), Real-world |

Each member commits their own contribution using their own GitHub account.

## 1. Problem modelling

This is modeled as a Linear Assignment Problem (LAP) on a bipartite graph $G = (U, V, E)$. Let $U$ be the set of $N$ technicians and $V$ be the set of $N$ tickets. An edge $\{u,v\}$ has a weight $C_{u,v}$ representing travel minutes plus skill-mismatch penalty.

A valid dispatch is a bijective function (one-to-one mapping):
\[assign: U \rightarrow V\]

- **Input:** $N \times N$ cost matrix where rows = technicians (T1..T4) and columns = tickets (K1..K4). $N=4$.
- **Constraint:** Each technician is assigned exactly one ticket; each ticket receives exactly one technician.
- **Objective:** Find an assignment that minimizes total cost $\sum_{i=1}^{N} C_{i, assign(i)}$.

### Given instance

Number of technicians: **4**
Number of tickets: **4**

Cost Matrix (in minutes):
| | K1 | K2 | K3 | K4 |
|---|---|---|---|---|
| **T1** | 11 | 4 | 9 | 7 |
| **T2** | 8 | 6 | 5 | 10 |
| **T3** | 7 | 10 | 3 | 9 |
| **T4** | 9 | 8 | 11 | 6 |

| Question | Type | Why |
|---|---|---|
| What is the lowest cost mapping? | **Optimisation** | Minimise total weight; standard LAP is $O(N^3)$ via Hungarian. |
| Is a mapping possible with constraints? | **Decision** | Yes/no answer; side-constraints make this NP-hard. |
| List all valid mappings. | **Enumeration** | Output all $N!$ perfect matchings. |

## 2. Data structure analysis

**Chosen:** 2D Array (`cost_matrix[N][N]`) and a Boolean array (`assigned[N]`) tracking tickets.

| Operation | 2D Array (chosen) | Edge List | Adjacency List |
|---|---|---|---|
| Space | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ |
| Find cost of T(i) $\rightarrow$ K(j) | $O(1)$ | $O(N)$ | $O(N)$ |
| Check if ticket is free | $O(1)$ | $O(N)$ | $O(1)$ (with extra map) |
| Update Lower Bound | $O(N^2)$ | $O(N^3)$ | $O(N^2)$ |

For a dense, complete bipartite graph where any technician can theoretically take any ticket, a 2D matrix provides $O(1)$ edge-weight lookups. This is critical because calculating the theoretical lower bound at every node requires rapidly summing minimums across available rows.

## 3. Technique identification: Branch and Bound

The property that makes Branch and Bound work is that **the state space is a tree of partial assignments with a monotonically increasing cost that can be aggressively bounded.**

Assign tickets one technician at a time (level by level). At each node, calculate a theoretical Lower Bound (LB) of the total cost if we continue down this path.
If this LB exceeds the current known `min_cost` of a complete assignment, the entire subtree is discarded. A sub-optimal prefix can never be "repaired" into an optimal completion because costs are strictly non-negative.

Because side-constraints (like certifications) break the bipartite properties required by exact polynomial algorithms like the Hungarian method, Branch and Bound provides the flexibility to dynamically prune invalid paths while still guaranteeing a globally optimal result.

## 4. Rejection of the other four techniques

### 4.1 Greedy - rejected by counterexample (Q3)

A fixed rule (technicians pick the cheapest available ticket in turn) commits to an assignment and never revises it.
- **T1** picks K2 (Cost: 4). Free: K1, K3, K4.
- **T2** picks K3 (Cost: 5). Free: K1, K4.
- **T3** is forced to pick K1 (Cost: 7). Free: K4.
- **T4** is forced to pick K4 (Cost: 6).
- **Total Greedy Cost:** 22.

The tree contains an optimal path with cost 21. Greedy forces T3 into an inefficient assignment, entirely missing the global optimum.

### 4.2 Dynamic Programming - exponential space

Using Bitmask DP, the state is defined by the subset of tickets assigned:
\[DP[mask] = \min_{j \notin mask} (DP[mask \cup \{j\}] + cost[i][j])\]
It is correct and solves the problem in $O(N \cdot 2^N)$ time and space. However, for a real-world zone with 40-60 technicians, it requires storing $2^{60}$ states in memory, which is physically impossible. Branch and Bound uses a priority queue and prunes heavily, requiring drastically less space.

### 4.3 Divide and Conquer - subproblems are not independent

Split the technicians into halves $A$ and $B$. Assigning a ticket to a technician in $A$ permanently removes that ticket from the pool available to $B$. The subproblems overlap completely. There is no way to independently solve halves and merge them without causing ticket collisions.

### 4.4 Backtracking - Time Limit Exceeded (TLE)

Pure backtracking explores the entire $O(N!)$ state space. Without calculating a lower bound to prune paths, it wastes immense computational time exploring branches that are mathematically guaranteed to be sub-optimal.

## 5. Algorithm

```text
ASSIGN_BB(cost_matrix):
  pq = PriorityQueue()
  initial_bound = CALC_BOUND(cost_matrix, assigned=[False]*N, level=0)
  pq.push(Node(cost=0, path=[], bound=initial_bound, level=0, assigned))
  min_cost = INFINITY
  
  while pq is not empty:
      curr = pq.pop()
      if curr.bound >= min_cost: continue // Prune
      
      if curr.level == N: // Reached leaf
          min_cost = min(min_cost, curr.cost)
          continue
          
      i = curr.level
      for j in 0 to N-1:
          if not curr.assigned[j]:
              new_assigned = curr.assigned.copy()
              new_assigned[j] = True
              new_cost = curr.cost + cost_matrix[i][j]
              new_bound = new_cost + CALC_BOUND(cost_matrix, new_assigned, i+1)
              
              if new_bound < min_cost:
                  pq.push(Node(new_cost, path+j, new_bound, i+1, new_assigned))
