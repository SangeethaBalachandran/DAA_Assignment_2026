# Batch 7 - Education: End-semester Exam Timetabling

**Course:** 23I501 Design and Analysis of Algorithms, PSG College of Technology

**Members:**
- Member 1: Soumya M - 24I357 - GitHub: `Soumya-M-2026`
- Member 2: Sumathi K - 24I366 - GitHub: `Sumathi-K04`
- Member 3: Rizvin A - 24I348 - GitHub: `rizvin1980-ai`
- Member 4: Thanya K - 24I369 - GitHub: `24i369`

**Presentation video:** (https://docs.google.com/presentation/d/1HiANg0gUzTlDgeMpOIkd813eonEaDn7Y/edit?usp=sharing&ouid=105269251308143861482&rtpof=true&sd=true)

**Chosen technique:** Backtracking with forward checking and most-constrained-first ordering.

**Rejected techniques:** Greedy, Dynamic Programming, Divide and Conquer, Branch and Bound.

## 0. Contribution table

| Member (name, roll no., GitHub) | Files committed | README sections | Slides | Video part |
|---|---|---|---|---|
| Member 1: Soumya M (24I357, Soumya-M-2026) | `code/main_solution.py`, `code/RUN.md`, `slides.pdf` | 1, 2, 3, 5 | 1-4, 6 | Problem model, data structures, why Backtracking, algorithm demo |
| Member 2: Sumathi K (24I366, Sumathi-K04) | `code/rejected_alternative.py`, `code/generate_inputs.py` | 4, 7, 10, 11 | 5, 9, 13, 14 | Rejecting the four techniques, Q4, proof, Q5 |
| Member 3: Rizvin A (24I348, rizvin1980-ai) | `code/benchmark.py`, `results/*` | 6, 8, 9 | 7, 8, 10, 11, 12 | Trace, complexity, timing plot, worst case |
| Member 4: Thanya K (24I369, 24i369) | `analysis_sheet.pdf` | 12 (+ table, video link) | 15 | Real-world reference, closing |

Each member commits their own contribution using their own GitHub account.

## 1. Problem modelling

Graph \(G=(V,E)\): \(V\) represents courses, and an edge \(\{u,v\}\) exists if and only if courses \(u\) and \(v\) share at least one student. A timetable is a map:

\[
slot:V\rightarrow\{1,\ldots,k\}
\]

- **Input:** \(G\), where \(n=420\), with 9 days × 2 slots = 18 slots in the real problem; the given instance has \(n=7\), \(k=3\).
- **Constraint:** For every edge \(\{u,v\}\), \(slot(u)\ne slot(v)\). This is a proper \(k\)-colouring.
- **Objective:** Decide feasibility for a given \(k\), or minimise \(k\), the chromatic number \(\chi(G)\).

### Given instance

Order of first appearance: DAA, OS, DBMS, ML, CN, SE, Maths.

Number of vertices: **7**

Number of edges: **10**

Conflict relationships:

1. DAA-OS
2. DAA-DBMS
3. DAA-ML
4. OS-CN
5. OS-DBMS
6. DBMS-SE
7. CN-ML
8. ML-Maths
9. SE-Maths
10. CN-SE

| Question | Type | Why |
|---|---|---|
| Can it fit in 3 slots? | **Decision** | Yes/no answer; 3-colourability is NP-complete. |
| What is the minimum number of slots? | **Optimisation** | Minimise \(k\); computing \(\chi(G)\) is NP-hard. |
| List all valid timetables. | **Enumeration** | Output all solutions; their number is the chromatic polynomial \(P(G,3)\). |

For this instance, \(\chi(G)=3\), and there are 36 proper labelled 3-colourings (6 distinct timetables up to renaming slots, by brute-force check).

## 2. Data structure analysis

**Chosen:** Adjacency sets (`adj[v]` = hash set) and bitmask domains (`dom[v]`, one integer, where bit \(s\) means slot \(s\) is still allowed).

| Operation | Adjacency set (chosen) | Adjacency matrix | Edge list |
|---|---|---|---|
| Space | \(O(n+m)\) | \(O(n^2)\) | \(O(m)\) |
| Are u,v in conflict? | \(O(1)\) average | \(O(1)\) | \(O(m)\) |
| Visit all neighbours of v (forward checking) | \(O(\deg v)\) | \(O(n)\) | \(O(m)\) |
| Build | \(O(m)\) | \(O(n^2)\) initialisation | \(O(m)\) |

For \(n=420\), the conflict graph is sparse (\(m\approx4,400\) in our random model versus 87,990 possible edges). Forward checking only visits neighbours, so adjacency sets are suitable.

Bitmask domains allow a slot to be removed in \(O(1)\), emptiness to be tested in \(O(1)\), and the number of candidates to be counted with one population-count operation. Boolean arrays would cost \(O(k)\) per update. Since \(k\leq18\), the domain fits in one machine word.

## 3. Technique identification: Backtracking

The property that makes Backtracking work is that **the state space is a tree of partial assignments with a prunable, locally checkable constraint**.

Assign courses one at a time. A partial timetable is extendable only if it is conflict-free. An invalid prefix can be rejected immediately without examining any completion, because a prefix that violates an edge can never be repaired by later assignments.

A violation is detected after checking one vertex's neighbours, and the entire subtree below that assignment can be discarded.

Forward checking strengthens this approach: if any unassigned course has no allowed slot left, the branch is rejected.

Because \(k\) is fixed by the examination cell (18 slots, i.e. 9 days), the real question is the decision problem: "Is there a feasible timetable?" Backtracking directly answers this by returning the first solution or proving that none exists.

## 4. Rejection of the other four techniques

### 4.1 Greedy - rejected by counterexample (Q4)

A fixed rule (descending conflicts, lowest free slot) commits to a slot and never revises it.

The 8-course tree in Q4 is 2-colourable, but the rule uses 3 slots.

Greedy is useful only as a fast upper bound or ordering heuristic inside our solver.

### 4.2 Dynamic Programming - exponential state space

The only subproblem structure is over subsets of courses:

\[
f(S)=1+\min_{I\text{ independent in }S}f(S\setminus I)
\]

It is correct but has \(2^n\) states and \(O(3^n)\) time.

Measured results:

- 0.23 ms at \(n=8\)
- 197 ms at \(n=14\)
- 1,837 ms at \(n=16\)

This is approximately a 9-fold increase for every additional 2 courses.

At \(n=420\), it would need \(2^{420}\) states. A conflict graph is arbitrary, so no polynomial-size set of subproblems exists in general, unlike bounded-treewidth graphs.

### 4.3 Divide and Conquer - subproblems are not independent

Split the courses into halves \(A\) and \(B\), colour each half separately, and merge.

The cross edges between \(A\) and \(B\) couple the halves. A valid colouring of \(A\) can make \(B\) uncolourable with the same \(k\). Fixing this means recolouring, so there is no merge step cheaper than solving the whole problem.

There is also no balanced split with few cross edges in a general conflict graph.

For the instance, split:

\[
\{DAA,OS,DBMS\}\mid\{ML,CN,SE,Maths\}
\]

The left half is a triangle (3 slots). The right half is a 4-cycle CN-ML-Maths-SE, which is 2-colourable on its own.

The 3 cross edges DAA-ML, OS-CN and DBMS-SE decide whether the independently chosen colourings fit. A clash forces recolouring, not a cheap merge.

### 4.4 Branch and Bound - weak or absent bound

With \(k\) fixed, there is no objective value to bound, so Branch and Bound degenerates to Backtracking.

For minimising \(k\), Branch and Bound needs a lower bound. The usual one is the clique number, which is NP-hard to determine itself and can be far below \(\chi\).

Mycielski graphs have clique number 2 but can have a higher chromatic number (for example, \(\chi=5\) on 23 vertices). The bound is therefore weak.

The experiments in Section 9 show that this bound cannot cut those search trees.

## 5. Algorithm

```text
COLOUR(adj, k, allowed, order):
  dom[v] <- allowed[v] (default {0..k-1}) as bitmask
  return SEARCH(dom, assigned=0, maxColourUsed=-1)

SEARCH(dom, done, maxc):
  if done == n: return TRUE
  v <- unassigned vertex with smallest popcount(dom[v])
       (tie: highest degree)
  for c in dom[v], ascending:
      if no pins and c > maxc+1: break
      nd <- copy(dom)
      nd[v] <- {c}
      for u in adj[v] unassigned:
          nd[u] <- nd[u] minus {c}
          if nd[u] empty: reject c; continue
      col[v] <- c
      if SEARCH(nd, done+1, max(maxc,c)): return TRUE
      col[v] <- unassigned
  return FALSE
```

The state consists of the partial colouring and the remaining domain of each unassigned course.

For finding the minimum number of slots, try \(k\) from the greedy or clique lower bound upwards until `COLOUR` succeeds.

### Day rule and pinning (Q5)

Two conflicting courses may not share a **day**. Hence, the colour of a course represents its day (\(D=9\) colours), and the slot inside the day is chosen afterwards, balancing the two slots.

"Maths in slot 1" is a unary constraint:

`allowed[Maths] = {day of slot 1} = {D1}`.

## 6. Trace on the instance (Q2, Q3)

Order: DAA, OS, DBMS, ML, CN, SE, Maths. Slots: 1-3. A slot is rejected if a neighbour already holds it.

| Step | Course | Try slot | Result | Reason |
|---|---|---|---|---|
| 1 | DAA | 1 | Accept | No assigned neighbour |
| 2 | OS | 1 | Reject | Conflicts with DAA (1) |
| 2 | OS | 2 | Accept | |
| 3 | DBMS | 1 | Reject | Conflicts with DAA (1) |
| 3 | DBMS | 2 | Reject | Conflicts with OS (2) |
| 3 | DBMS | 3 | Accept | |
| 4 | ML | 1 | Reject | Conflicts with DAA (1) |
| 4 | ML | 2 | Accept | Neighbours DAA=1, CN and Maths unassigned |
| 5 | CN | 1 | Accept | Neighbours OS=2, ML=2 |
| 6 | SE | 1 | Reject | Conflicts with CN (1) |
| 6 | SE | 2 | Accept | Neighbours DBMS=3, CN=1 |
| 7 | Maths | 1 | Accept | Neighbours ML=2, SE=2 |

**Result: 5 rejections, 0 backtracks.**

- Slot 1: {DAA, CN, Maths}
- Slot 2: {OS, ML, SE}
- Slot 3: {DBMS}

Every one of the 10 conflict pairs is split across slots.

### Q3 - Why 2 slots are impossible

DAA-OS, DAA-DBMS and OS-DBMS are all conflicts. Therefore, {DAA, OS, DBMS} is a triangle.

Three pairwise-conflicting examinations need three distinct slots (pigeonhole principle), hence:

\[
\chi(G)\geq3
\]

Together with the valid 3-slot colouring in Q2:

\[
\boxed{\chi(G)=3}
\]

In general, any clique of size \(q\) forces at least \(q\) slots.

### Q5 trace (3 days, Maths pinned to D1, most-constrained-first)

| Step | Domains before the pick | Pick |
|---|---|---|
| 1 | Maths {D1}; all others {D1,D2,D3} | Maths = D1 (domain size 1) |
| 2 | ML {D2,D3}, SE {D2,D3} (pruned by Maths); DAA, OS, DBMS, CN full | ML = D2 (tie with SE, higher degree/index) |
| 3 | DAA {D1,D3}, CN {D1,D3}, SE {D2,D3}, OS, DBMS full | DAA = D1 |
| 4 | OS {D2,D3}, DBMS {D2,D3}, CN {D1,D3}, SE {D2,D3} | OS = D2 |
| 5 | DBMS {D3}, CN {D1,D3}, SE {D2,D3} | DBMS = D3 |
| 6 | CN {D1,D3}, SE {D2} | SE = D2 |
| 7 | CN {D1,D3} | CN = D1 |

Slots:

- Day 1: Maths 1, DAA 1, CN 2
- Day 2: OS 3, SE 3, ML 4
- Day 3: DBMS 5

There are 7 nodes and 0 backtracks.

With only 3 slots (= 2 days), the instance is infeasible because the triangle needs 3 different days. The solver proves this in 4 nodes.

## 7. Q4 - Greedy counterexample

Courses u, v (3 conflicts each), w, z (2 each), and leaves l1, l2 (on u) and m1, m2 (on v).

Edges:

- u-w
- w-z
- z-v
- u-l1
- u-l2
- v-m1
- v-m2

This is a tree, so **2 slots suffice**:

- Slot 1 = {u, z, m1, m2}
- Slot 2 = {v, w, l1, l2}

Coordinator order: u, v, w, z, leaves (descending degree).

- u → 1
- v → 1 (not in conflict with u)
- w → 2 (u holds 1)
- z: v holds 1, w holds 2 → **3**
- Leaves take 2.

**Result: 3 slots versus optimum 2**, as demonstrated by `python3 rejected_alternative.py`.

Either tie-break among equal degrees gives the same outcome. The cause is that u and v are non-adjacent, so Greedy places them in the same slot, forcing the path w-z between them onto three slots.

## 8. Complexity

Let \(n\) be the number of courses, \(m\) the number of conflicts, and \(k\) the number of slots.

### Worst case

The search tree can have up to \(k^n\) leaves. Each node costs \(O(\deg v)\) for forward checking, plus \(O(n)\) for variable choice and domain copying.

Therefore:

\[
\boxed{O(k^n\cdot n)}
\]

With colour-symmetry breaking, the number of possibilities is roughly the number of set partitions, which is still exponential.

Recurrence:

\[
T(n)\leq kT(n-1)+O(n)
\]

No polynomial algorithm is expected because 3-colouring is NP-complete.

### Best case

If every course receives its first slot without backtracking, there are \(n\) nodes, each costing \(O(n+\deg v)\):

\[
O(n^2+m)
\]

### Practical behaviour on the real-data model

If \(k\geq\text{maximum conflicts}+1\), colouring never fails.

For our 420-course random model (average degree approximately 21, \(k=9\)), the search is backtracking-free: 420 nodes and approximately 30 ms.

### Space complexity

Recursion depth is \(n\), with a copied domain list per level:

\[
O(n^2)
\]

as implemented. An undo trail could reduce this to \(O(n)\) additional search space.

Graph storage is:

\[
O(n+m)
\]

### Minimum slots

There are at most \(k_{up}-k_{low}+1\) decision runs, each with the complexity described above.

## 9. Implementation and empirical analysis

Files:

- `code/main_solution.py` - chosen Backtracking implementation.
- `code/rejected_alternative.py` - subset Dynamic Programming and Greedy.
- `code/generate_inputs.py` - input graph generator.
- `code/benchmark.py` - benchmarking.
- `results/` - experimental result files.

### Timing results: minimum slots on random graphs (p = 0.3)

Both methods return the same answer.

| n | Backtracking (ms) | Subset DP (ms) |
|---:|---:|---:|
| 6 | 0.03 | 0.05 |
| 8 | 0.05 | 0.23 |
| 10 | 0.06 | 2.2 |
| 12 | 0.07 | 21.5 |
| 14 | 0.09 | 197 |
| 16 | 0.11 | 1,837 |

DP grows by approximately 9 times for every additional 2 courses, which matches the derived \(O(3^n)\) complexity.

Backtracking grows slowly on these easy instances.

### Timing-scale results

`results/timing_scale.csv` records the chosen method on feasible instances with 9 days, up to the real problem size.

| n | Backtracking time (ms) | Nodes |
|---:|---:|---:|
| 50 | 0.47 | 50 |
| 100 | 3.0 | 100 |
| 150 | 6.5 | 150 |
| 200 | 11.8 | 200 |
| 300 | 16.1 | 300 |
| 420 | 30.3 | 420 |

The number of nodes equals \(n\) in each case, with no backtracking. This is consistent with the observed behaviour of at most \(O(n^2)\) on these instances.

### Worst-case input

`results/worst_case.csv` contains Mycielski graphs (triangle-free, \(\chi=k\)) asked to use \(k-1\) slots. These are "no" instances that must be fully explored.

| Chromatic number | n | Slots asked | Nodes (most-constrained-first) | Nodes (input order) |
|---:|---:|---:|---:|---:|
| 4 | 11 | 3 | 26 | 57 |
| 5 | 23 | 4 | 895 | 49,388 |
| 6 | 47 | 5 | 448,614 (3.8 s) | >3,000,000 (stopped) |

Nodes grow approximately 34 times and then 500 times between consecutive rows. This is exponential, as the \(O(k^n)\) bound predicts.

The clique bound (=2) is ineffective here, showing why Branch and Bound with that bound does not help.

### Ordering effect

`results/ordering.csv` records the Maths-pinned, day-rule random graph experiment.

At \(n=40\), input order required:

- 21,769 nodes
- 10,552 nodes
- 7,910 nodes
- 69,981 nodes

One run exceeded 2,000,000 nodes and was stopped.

Most-constrained-first always used exactly 40 nodes.

### Timing plot

The timing plot is available at:

`results/timing_plot.png`

### Discussion

The experiments show that Backtracking performs efficiently on the tested feasible random graphs, especially when combined with forward checking and most-constrained-first ordering.

Subset Dynamic Programming becomes expensive as the number of courses increases. Its measured running time grows by approximately a factor of 9 for every additional 2 courses, matching its \(O(3^n)\) time complexity.

The Mycielski worst-case experiments show that Backtracking can still require exponential search on difficult infeasible instances. The ordering experiment demonstrates that most-constrained-first can substantially reduce the search compared with input order.

These results illustrate the difference between practical performance on favourable instances and worst-case exponential complexity.

## 10. Proof of correctness

**Claim:** `SEARCH` returns TRUE if and only if a proper colouring respecting `allowed` exists, and when it returns TRUE, `col` is such a colouring.

### Invariant (soundness)

At every call:

1. Assigned vertices have pairwise-different colours along edges.
2. For each unassigned vertex \(u\), `dom[u]` equals `allowed[u]` minus the colours of its assigned neighbours.

Initially, this is true because no vertices are assigned.

Assigning vertex \(v\) to colour \(c\) cannot clash with an assigned neighbour because the invariant says that `dom[v]` excludes their colours.

Removing \(c\) from each unassigned neighbour's domain preserves the invariant.

When `done == n`, every vertex is assigned and the colouring is proper.

### Completeness (pruning never discards a solution)

A rejection happens only when some unassigned vertex \(u\) has an empty domain. By the invariant, every colour for \(u\) either clashes with an assigned neighbour or is forbidden. Therefore, no extension of the current partial colouring exists.

The loop tries every colour in `dom[v]`. If a solution extends the current state, its colour for \(v\) is tried, and by induction on \(n-done\), the recursive call finds a solution.

The symmetry rule (used only with no pins) skips colours above `maxc+1`. Those colours are unused and interchangeable, so a solution using any such colour can be renamed to use `maxc+1` without changing validity. Thus, skipping those colours loses no solution.

### Termination

`done` increases by 1 at each recursion level. Therefore, recursion depth is at most \(n\), and each level tries at most \(k\) colours.

### Day-rule encoding

A timetable is valid if and only if conflicting courses are on different days.

Therefore, valid timetables correspond exactly to proper colourings with \(D\) colours (days), plus any slot choice inside each day.

Pinning Maths to slot 1 restricts its day to day 1. Any solution must satisfy this unary constraint, which is represented by the domain restriction.

## 11. Changed requirement (Q5)

### Encoding

- Maths in slot 1 → `allowed[Maths] = {D1}`.
- One exam per day → colour by day. Conflicting courses need different days.
- \(D=9\) colours are used for the real problem.
- The second slot per day does not relieve conflicts; it is only used for balancing rooms and invigilation.

A surprising consequence is that the 18 slots collapse to 9 colours.

### Instance effect

- 3 slots = days {1,2}: infeasible because the triangle needs 3 different days.
- With 3 days, the solution in Section 6 exists.

### Technique still holds

Unary restrictions and a coarser colouring remain a constraint-satisfaction problem solved by Backtracking.

Precolouring extension is still NP-complete, so no polynomial algorithm should be expected. The objections to Dynamic Programming, Greedy and Divide and Conquer remain unchanged. The pinned course only makes the search smaller.

### Best ordering

Most-constrained-first (smallest remaining domain), with ties broken by highest conflicts.

Maths (domain size 1) is placed first, immediately removing day 1 from its neighbours ML and SE. Then the course with the fewest options is placed (DSATUR-style).

Failures are found near the root, where they are cheap to cut (fail-first). In our tests, this reached a full timetable with zero dead ends (\(n\) nodes), while input order wasted up to millions of nodes.

Descending-degree ordering alone is not enough because it ignores the pin and the shrinking domains.

## 12. Real-world reference

**DSATUR**:

D. Brelaz, "New methods to color the vertices of a graph", *Communications of the ACM*, 1979.

This is the saturation-degree ordering used in exam-timetabling heuristics and exact colouring codes.

Carter, Laporte and Lee, "Examination timetabling: algorithmic strategies and applications", *Journal of the Operational Research Society*, 1996, compare such orderings on real university data.

The difference is that DSATUR as a heuristic never backtracks, whereas our approach adds forward checking and exact Backtracking to prove infeasibility.

Modern industrial timetabling, such as the ITC-2007 exam track solvers and CP-SAT in Google OR-Tools, adds learned clauses and soft constraints (room capacity and spreading), which our version does not model.

**Reference verification note:** The package asks the team to verify these citations in the library before presenting them.

## 13. Slides

The presentation slides are included as:

`slides.pdf`

## 14. Analysis sheet

The analysis sheet is included as:

`analysis_sheet.pdf`

## 15. Presentation and conclusion

**Presentation video:** (https://docs.google.com/presentation/d/1HiANg0gUzTlDgeMpOIkd813eonEaDn7Y/edit?usp=sharing&ouid=105269251308143861482&rtpof=true&sd=true)

The presentation should explain the problem, selected design technique, algorithm, implementation, experimental results, real-world application and conclusion.

All four members present their own parts with voice. The video should be shared with access enabled for anyone with the link to view.

### Conclusion

This assignment models end-semester examination timetabling as a graph-colouring problem and uses Backtracking with forward checking and most-constrained-first ordering.

The given 7-course instance requires 3 colours. The triangle formed by DAA, OS and DBMS proves that 2 colours are insufficient, while the trace demonstrates a valid 3-colour solution.

The experiments show that ordering and forward checking can make Backtracking effective on the tested feasible instances, while worst-case infeasible instances still demonstrate exponential growth.

The project connects Design and Analysis of Algorithms concepts with a practical examination-scheduling problem.

## References

1. Course materials for 23I501 — Design and Analysis of Algorithms.
2. Assignment instructions and report template provided by the course instructor.
3. Brelaz, D. (1979). "New methods to color the vertices of a graph." *Communications of the ACM*.
4. Carter, M. W., Laporte, G., and Lee, S. Y. (1996). "Examination timetabling: algorithmic strategies and applications." *Journal of the Operational Research Society*.
5. Python documentation: https://docs.python.org/3/
6. 
