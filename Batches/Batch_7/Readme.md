# Batch 7 — Graph Colouring for Exam Timetabling

## Design and Analysis of Algorithms (DAA) Assignment

### 1. Team Details

MEMBER	NAME	ROLL  NO	GITHUB USERNAME	CONTRIBUTION
1	Soumya M	24i357	Soumya-M-2026	Problem modelling, graph-colouring solution, implementation, and execution documentation
2	Sumathi K	24i366	Sumathi-K04	Alternative algorithms, rejected approaches, and input-generation code
3	Rizvin A	24i348	rizvin1980-ai	Benchmarking, performance analysis, timing data, and plots
4	Thanya K	24i369	24i369	Real-world application study, analysis sheet, and presentation/video support



---

## 2. Problem Statement

Exam timetabling is the task of assigning examinations to time slots while ensuring that students do not have conflicting examinations scheduled at the same time.

This assignment models the exam-timetabling problem as a **graph-colouring problem**.

- Each vertex represents an examination.
- An edge connects two examinations if at least one student is enrolled in both.
- A colour represents an exam time slot.
- Adjacent vertices must receive different colours.

The objective is to assign colours to the graph while minimizing the number of colours used, subject to the conflict constraints.

---

## 3. Objectives

The objectives of this assignment are:

1. Represent an exam-timetabling problem using a graph.
2. Implement a graph-colouring algorithm to generate a valid timetable.
3. Study alternative algorithms and their limitations.
4. Analyze the time and space complexity of the algorithms.
5. Evaluate the implementation using experimental results.
6. Relate graph colouring to a real-world exam-timetabling application.

---

## 4. Problem Modelling

Let the conflict graph be:

\[
G=(V,E)
\]

where:

- \(V\) is the set of vertices representing examinations.
- \(E\) is the set of edges representing conflicts between examinations.

A colouring is a function:

\[
c:V\rightarrow \{1,2,\ldots,k\}
\]

such that:

\[
(u,v)\in E \implies c(u)\ne c(v)
\]

The goal is to find a valid colouring using as few colours as possible.

The minimum number of colours required for a graph is called its **chromatic number**, denoted by \(\chi(G)\).

---

## 5. Algorithm Used

### Backtracking Graph Colouring

The main solution uses a backtracking approach.

The algorithm assigns a colour to a vertex and checks whether that colour conflicts with any already-coloured adjacent vertex.

If a valid colour is found, the algorithm continues to the next vertex. If no available colour works, it backtracks and tries another assignment.

### General Steps

1. Select an uncoloured vertex.
2. Try assigning an available colour.
3. Check whether any adjacent vertex has the same colour.
4. If the assignment is valid, continue with the next vertex.
5. If no colour works, backtrack.
6. Stop when all vertices are coloured or no valid assignment is found for the given colour limit.

The implementation and execution instructions are available in the `code/` directory.

---

## 6. Repository Structure

```text
DAA_Assignment_2026/
└── Batches/
    └── Batch_7/
        ├── README.md
        ├── slides.pdf
        ├── analysis_sheet.pdf
        ├── code/
        │   ├── main_solution.py
        │   ├── RUN.md
        │   ├── rejected_alternative.py
        │   ├── generate_inputs.py
        │   └── benchmark.py
        └── results/
            ├── timing.csv
            ├── timing_scale.csv
            ├── worst_case.csv
            ├── ordering.csv
            └── timing_plot.png
```

*The structure above shows the intended organization. Files should be added as they are completed by the team.*

---

## 7. Implementation

The implementation is written in Python.

| File | Description |
|---|---|
| `main_solution.py` | Main graph-colouring solution |
| `RUN.md` | Instructions for running the main solution |
| `rejected_alternative.py` | Implementation of an alternative or rejected approach |
| `generate_inputs.py` | Generates test inputs for experimentation |
| `benchmark.py` | Runs experiments and collects performance measurements |

---

## 8. Experimental Analysis

The team evaluates the implementation using different graph inputs.

The experiments may examine:

- Number of vertices and edges
- Number of colours used
- Execution time
- Effect of graph size on performance
- Effect of vertex ordering
- Performance on difficult or dense graphs

Experimental results and plots are stored in the `results/` directory.

Results should be added only after the corresponding experiments have been executed.

---

## 9. Complexity Analysis

For a graph with \(V\) vertices and a maximum of \(K\) colours:

- **Worst-case time complexity:** \(O(K^{|V|})\), for a straightforward backtracking implementation.
- **Space complexity:** \(O(|V|)\) for the colour assignment and recursion stack, excluding graph storage.

The actual complexity depends on implementation details, pruning strategies, and the input graph.

---

## 10. Real-World Application

Graph colouring can be used in exam timetabling to avoid scheduling conflicting examinations in the same time slot.

The conflict graph represents examinations and student conflicts. A valid colouring assigns a time slot to each examination so that no two conflicting examinations share a slot.

This model can also be applied to:

- University examination scheduling
- Course timetabling
- Meeting scheduling
- Frequency assignment
- Resource allocation

In practical exam timetabling, additional constraints may also be needed, such as room capacity, student preferences, and restrictions on consecutive examinations.

---

## 11. Team Contributions

All four members contribute to the same Batch 7 assignment directory.

| Member | Main Responsibility |
| Member 1 | Problem modelling, main graph-colouring implementation, execution documentation, and slides |
| Member 2 | Alternative algorithms, rejected approaches, and input generation |
| Member 3 | Benchmarking, experimental data, plots, and performance analysis |
| Member 4 | Real-world application study, analysis sheet, and presentation/video support |

Each member's files are stored in the shared `code/`, `results/`, or main `Batch_7/` directory according to their purpose. No individual member folders are used.

---

## 12. Conclusion

This assignment demonstrates how graph colouring can model exam timetabling as a conflict-free scheduling problem.

The backtracking algorithm searches for a valid colour assignment while respecting the constraints represented by the graph. The implementation, alternative approaches, and experimental analysis help illustrate the strengths and limitations of graph-colouring techniques for scheduling problems.

The project also demonstrates the relevance of Design and Analysis of Algorithms concepts to practical applications.

---
## 13. Video Demonstration

The video demonstration explains the problem, graph representation, algorithm, implementation, and experimental results.

**Video Link:** 


## 14. References

- Course materials for Design and Analysis of Algorithms.
- Graph theory concepts related to vertex colouring and chromatic number.
- Python documentation: https://docs.python.org/3/
- Additional references used by the team should be listed here.
