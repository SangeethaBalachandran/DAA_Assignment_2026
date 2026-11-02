# Batch_8 – Sensor Telemetry Compression using Huffman Coding

## DAA Assignment 2026

**Course:** 23I501 – Design and Analysis of Algorithms (DAA)  
**Institution:** PSG College of Technology  
**Academic Year:** 2026–27  
**Batch:** Batch_8

---

# Problem Statement

An industrial edge gateway forwards status codes from thousands of IoT sensors over a low-bandwidth communication channel. The objective is to compress the sensor telemetry efficiently using an optimal prefix-free encoding scheme while ensuring lossless data transmission.

The given sensor frequencies are:

| Sensor Code | Frequency |
|-------------|----------:|
| OK | 52 |
| TEMP_HI | 14 |
| TEMP_LO | 11 |
| HUM | 9 |
| VIB | 7 |
| DOOR | 4 |
| FAULT | 2 |
| RESET | 1 |

The goal is to reduce bandwidth usage while allowing the receiver to reconstruct the original data exactly.

---

# Selected Design Technique

## Greedy Algorithm – Huffman Coding

Huffman Coding is a Greedy Algorithm that repeatedly combines the two least frequent symbols to construct an optimal prefix-free binary tree.

This guarantees the minimum average number of bits required to encode the telemetry data.

---

# Why Other Design Techniques Were Rejected

## Divide and Conquer

The problem cannot be divided into independent subproblems because all symbol frequencies contribute to one optimal Huffman tree.

---

## Dynamic Programming

Dynamic Programming is unnecessary because Huffman Coding already provides an optimal solution through a greedy strategy without storing overlapping subproblems.

---

## Backtracking

Backtracking explores many possible trees, resulting in exponential complexity and making it unsuitable for real-time telemetry compression.

---

## Branch and Bound

Branch and Bound is mainly used for optimization search problems. Constructing a Huffman tree does not require searching multiple candidate solutions.

---

# Algorithm

1. Read all sensor symbols and their frequencies.
2. Insert every symbol into a Min Priority Queue.
3. Remove the two nodes with the smallest frequencies.
4. Merge them into a new internal node.
5. Insert the merged node back into the priority queue.
6. Repeat until only one node remains.
7. Traverse the Huffman Tree.
8. Assign binary codes to every symbol.
9. Encode the telemetry data using the generated Huffman codes.

---

# Data Structure Used

- Min Heap (Priority Queue)
- Binary Tree (Huffman Tree)

These data structures efficiently support selecting the two minimum-frequency nodes during every iteration.

---

# Complexity Analysis

| Operation | Time Complexity |
|-----------|-----------------|
| Build Priority Queue | O(n log n) |
| Huffman Tree Construction | O(n log n) |
| Generate Codes | O(n) |

### Overall Time Complexity

**O(n log n)**

### Space Complexity

**O(n)**

---

# Proof of Correctness

At every step, Huffman Coding selects the two least frequent symbols and merges them into a new node.

This greedy choice minimizes the weighted path length of the final tree.

Therefore, Huffman Coding always produces an optimal prefix-free code with the minimum average bits per message.

---

# Empirical Performance Analysis

The implementation was executed on multiple input sizes.

Execution times were recorded in:

```
results/timing.csv
```

The timing graph generated from the recorded values is available in:

```
results/timing_plot.png
```

The observed running time closely follows the expected **O(n log n)** complexity of Huffman Coding.

---

# Worst Case Input

The worst case occurs when the number of distinct sensor symbols increases significantly.

As more unique symbols are added, the Huffman tree becomes larger, increasing the number of priority queue operations.

---

# Files Included

```
Batch_8
│
├── README.md
├── slides.pdf
│
├── code
│   ├── backend
│   ├── frontend
│   ├── docs
│   └── RUN.md
│
└── results
    ├── timing.csv
    └── timing_plot.png
```

---

# Running the Project

Follow the instructions provided in:

```
code/RUN.md
```

---

# Presentation

The presentation video can be viewed using the following Google Drive link:

**Presentation Video**

https://drive.google.com/file/d/1H49ITVsPjIPwAGnax-xJIQpMN-MjRkGg/view?usp=drivesdk

---

# Team Contribution

| Member | Contribution |
|---------|--------------|
| Member 1 | Problem Analysis & Algorithm Selection |
| Member 2 | Huffman Algorithm Implementation |
| Member 3 | Backend Development |
| Member 4 | Frontend Development |
| Member 5 | Testing, Documentation & Presentation |

---

# References

1. Thomas H. Cormen, *Introduction to Algorithms (CLRS)*.
2. D. A. Huffman, *A Method for the Construction of Minimum-Redundancy Codes*.
3. GeeksforGeeks – Huffman Coding.
4. PSG College of Technology – DAA Course Material.

---

# Repository Structure

```
DAA_Assignment_2026/
└── Batches
    └── Batch_8
        ├── README.md
        ├── slides.pdf
        ├── code
        │   ├── backend
        │   ├── frontend
        │   ├── docs
        │   └── RUN.md
        └── results
            ├── timing.csv
            └── timing_plot.png
```

---

# Submission Checklist

- ✅ Problem Analysis Completed
- ✅ Greedy Technique Identified
- ✅ Other Four Techniques Rejected
- ✅ Huffman Algorithm Implemented
- ✅ Complexity Analysis Completed
- ✅ Proof of Correctness Included
- ✅ Timing Results Generated
- ✅ Timing Graph Included
- ✅ Slides Prepared
- ✅ Presentation Video Linked
- ✅ Source Code Uploaded
- ✅ Project Successfully Submitted
