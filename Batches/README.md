# Batch_8 – Sensor Telemetry Compression using Huffman Coding

Repository for the Design and Analysis of Algorithms (DAA) Assignment submission of **Batch_8**.

**Course:** 23I501 – Design and Analysis of Algorithms (DAA)  
**Instructor:** Dr. B. Sangeetha  
**Institution:** PSG College of Technology  
**Semester:** Odd Semester (5th)  
**Academic Year:** 2026–27

---

# Project Overview

This project presents an efficient solution for compressing sensor telemetry data using **Huffman Coding**, a Greedy Algorithm.

The objective is to reduce the bandwidth and storage required for transmitting IoT sensor data while ensuring that the original information can be reconstructed exactly after decompression.

---

# Problem Statement

An industrial edge gateway forwards status codes from thousands of IoT sensors over a low-bandwidth communication channel.

The objective is to compress the telemetry efficiently using an optimal prefix-free encoding scheme while ensuring **lossless data transmission**.

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

The goal is to minimize bandwidth usage while allowing the receiver to reconstruct the original data exactly.

---

# Selected Design Technique

## Greedy Algorithm – Huffman Coding

Huffman Coding repeatedly combines the two least frequent symbols to construct an optimal prefix-free binary tree.

This minimizes the average number of bits required to encode the sensor telemetry data.

---

# Why Other Design Techniques Were Rejected

## Divide and Conquer

The problem cannot be divided into independent subproblems because every symbol contributes to constructing one optimal Huffman Tree.

## Dynamic Programming

Dynamic Programming is unnecessary since Huffman Coding already guarantees the optimal solution using a greedy strategy.

## Backtracking

Backtracking explores many unnecessary combinations, resulting in exponential complexity and poor performance.

## Branch and Bound

Branch and Bound is mainly suitable for optimization search problems and is not efficient for Huffman Tree construction.

---

# Algorithm

1. Read all sensor symbols and their frequencies.
2. Insert every symbol into a Min Priority Queue.
3. Remove the two nodes having the smallest frequencies.
4. Merge them into a new internal node.
5. Insert the merged node back into the priority queue.
6. Repeat until only one node remains.
7. Traverse the Huffman Tree.
8. Generate binary codes for every symbol.
9. Encode the sensor telemetry using the generated Huffman Codes.

---

# Data Structures Used

- Min Heap (Priority Queue)
- Binary Tree (Huffman Tree)

These data structures efficiently support selecting the two minimum-frequency nodes during every iteration.

---

# Complexity Analysis

| Operation | Time Complexity |
|-----------|-----------------|
| Build Priority Queue | O(n log n) |
| Huffman Tree Construction | O(n log n) |
| Generate Huffman Codes | O(n) |

### Overall Time Complexity

**O(n log n)**

### Space Complexity

**O(n)**

---

# Proof of Correctness

At every iteration, Huffman Coding selects the two least frequent symbols and merges them into a new internal node.

This greedy choice minimizes the weighted path length of the Huffman Tree.

Therefore, Huffman Coding always produces an optimal prefix-free encoding with the minimum average number of bits required.

---

# Empirical Performance Analysis

The implementation was tested using multiple input sizes.

Execution times were recorded in

```
results/timing.csv
```

The execution-time graph generated from the recorded values is available in

```
results/timing_plot.png
```

The observed performance closely follows the expected **O(n log n)** complexity.

---

# Worst Case Input

The worst case occurs when the number of distinct sensor symbols increases significantly.

As more unique symbols are introduced, the Huffman Tree grows larger, resulting in additional priority queue operations.

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

Follow the instructions provided in

```
code/RUN.md
```

---

# Project Report

The complete project report is available at:

📄 **Google Docs**

https://docs.google.com/document/d/1W3_5JTwUE8tu7Tx3pXHuf1E7A-rVlzlK/edit?usp=drive_link

---

# Presentation

The complete project presentation video is available at:

🎥 **Google Drive**

https://drive.google.com/file/d/1H49ITVsPjIPwAGnax-xJIQpMN-MjRkGg/view?usp=drivesdk

---

# Team Members

| Roll No | Name | GitHub Username |
|---------|-------------------|----------------|
| 24I371 | Tirumeni Vikash A | @tirumeni |
| 25I461 | Ashwath P M | @pmashwath22 |
| 24I370 | Thiribhuvan V | @Thiribhuvan |
| 24I305 | Arul Selvan A | @avsarul06 |

---

# Team Contributions

| Member | Contribution |
|---------|--------------|
| Tirumeni Vikash A | Problem Analysis, Algorithm Selection, Documentation |
| Ashwath P M | Huffman Algorithm Implementation |
| Thiribhuvan V | Backend Development, Performance Analysis |
| Arul Selvan A | Frontend Development, Testing, Documentation & Presentation |

---

# References

1. Thomas H. Cormen, *Introduction to Algorithms (CLRS)*.
2. D. A. Huffman, *A Method for the Construction of Minimum-Redundancy Codes*.
3. GeeksforGeeks – Huffman Coding.
4. PSG College of Technology – Design and Analysis of Algorithms Course Material.

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
- ✅ Project Report Linked
- ✅ Slides Uploaded
- ✅ Presentation Video Linked
- ✅ Source Code Uploaded
- ✅ All Team Members Contributed
- ✅ Project Successfully Submitted

---

**Course:** 23I501 – Design and Analysis of Algorithms (DAA)  
**Project:** Sensor Telemetry Compression using Huffman Coding  
**Batch:** Batch_8  
**Institution:** PSG College of Technology  
**Academic Year:** 2026–27
