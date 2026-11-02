# Mathematical Specification
## Interactive Industrial IoT Telemetry Compression & Network Optimization Dashboard

**Course:** 23I501 – Design and Analysis of Algorithms  
**Institution:** PSG College of Technology  
**Batch:** Batch 8 – IoT / Embedded Systems  
**Project:** Industrial IoT Telemetry Compression & Network Optimization Dashboard

---

# 1. Problem Definition

## 1.1 Background

Industrial Internet of Things (IIoT) environments consist of thousands of sensors continuously transmitting operational status information to centralized gateways.

These messages may represent normal operating conditions, temperature abnormalities, humidity variations, vibration alerts, door events, system faults, and reset operations.

In bandwidth-constrained industrial networks, transmitting every status message using the same fixed-length binary representation can result in inefficient bandwidth utilization.

The proposed system uses variable-length prefix-free coding to reduce the number of bits required to represent frequently occurring sensor messages.

Huffman Coding is used to construct an optimal prefix-free code based on the observed message frequencies.

The system also evaluates alternative algorithms, analyzes computational complexity, simulates network bandwidth utilization, and enforces receiver firmware constraints.

## 1.2 Problem Statement

The industrial communication environment has the following characteristics:

- 5,000 industrial IoT sensors.
- A narrowband communication link with a capacity of 9.6 kbps.
- Eight distinct sensor status messages.
- Existing fixed-length encoding of 3 bits per message.
- An aggregate message generation rate of 40 messages per second.
- A maximum permitted receiver codeword length of 4 bits.

The objective is to design and implement an efficient compression system that minimizes the average number of bits required per message while maintaining lossless decoding and satisfying embedded hardware constraints.

---

# 2. Input Data and System Assumptions

## 2.1 Sensor Status Distribution

The system uses the following frequency distribution representing the observed frequencies over the last hour.

| Symbol | Description | Frequency | Probability |
|---|---|---:|---:|
| OK | Normal operation | 52 | 0.52 |
| TEMP_HI | High temperature | 14 | 0.14 |
| TEMP_LO | Low temperature | 11 | 0.11 |
| HUM | Humidity abnormality | 9 | 0.09 |
| VIB | Vibration detected | 7 | 0.07 |
| DOOR | Door opened | 4 | 0.04 |
| FAULT | System fault | 2 | 0.02 |
| RESET | System reset | 1 | 0.01 |
| **Total** | | **100** | **1.00** |

The probability of each symbol is calculated using:

\[
P(x_i)=\frac{f_i}{\sum_{j=1}^{n}f_j}
\]

Where:

- \(f_i\) represents the frequency of symbol \(i\).
- \(n\) represents the number of distinct symbols.

The total frequency is:

\[
\sum f_i=100
\]

Therefore:

\[
\sum P(x_i)=1
\]

## 2.2 System Parameters

| Parameter | Value |
|---|---:|
| Number of sensors | 5,000 |
| Network capacity | 9,600 bits/sec |
| Original code length | 3 bits |
| Aggregate message rate | 40 messages/sec |
| Number of symbols | 8 |
| Maximum permitted code length | 4 bits |
| Observation frequency total | 100 |

**Assumptions:**

1. The 40 messages per second represent aggregate network traffic, not traffic generated independently by every sensor.
2. The historical frequency distribution is used to construct the compression codebook.
3. The simulated live message stream follows the configured probability distribution.
4. The initial theoretical bandwidth calculations exclude packet headers, framing, retransmissions, and codebook distribution overhead.
5. The original fixed-length encoding requires 3 bits because there are eight distinct symbols.

---

# 3. Question 1 – Optimal Huffman Coding

## 3.1 Objective

Construct an optimal prefix-free binary code using Huffman Coding that minimizes the weighted average code length.

## 3.2 Fixed-Length Encoding

For eight distinct symbols, the minimum fixed-length binary representation is:

\[
L_{\text{fixed}}=\lceil\log_2(n)\rceil
\]

\[
L_{\text{fixed}}=\lceil\log_2(8)\rceil=3
\]

Therefore, the existing system requires 3 bits for every message.

## 3.3 Huffman Coding Algorithm

Huffman Coding is a greedy algorithm that repeatedly combines the two nodes with the smallest frequencies to construct an optimal binary prefix-code tree.

### Algorithm Steps

1. Create one leaf node for every symbol.
2. Insert all nodes into a minimum priority queue.
3. Extract the two nodes with the smallest frequencies.
4. Create a new internal node whose frequency equals their sum.
5. Insert the new internal node into the priority queue.
6. Repeat until only one node remains.
7. Traverse the resulting binary tree to generate codewords.

Assign:
- Left branch = 0.
- Right branch = 1.

The path from the root to each leaf determines its binary codeword.

## 3.4 Huffman Tree Construction

Initial frequencies in ascending order:

```text
1, 2, 4, 7, 9, 11, 14, 52
```

The merging operations are:

| Step | First Node | Second Node | Merged Frequency |
|---|---:|---:|---:|
| 1 | 1 | 2 | 3 |
| 2 | 3 | 4 | 7 |
| 3 | 7 | 7 | 14 |
| 4 | 9 | 11 | 20 |
| 5 | 14 | 14 | 28 |
| 6 | 20 | 28 | 48 |
| 7 | 48 | 52 | 100 |

The final node with frequency 100 becomes the root of the Huffman tree.

## 3.5 Generated Huffman Codebook

One valid Huffman code assignment is:

| Symbol | Frequency | Binary Code | Code Length |
|---|---:|---|---:|
| OK | 52 | 0 | 1 |
| TEMP_HI | 14 | 111 | 3 |
| TEMP_LO | 11 | 101 | 3 |
| HUM | 9 | 100 | 3 |
| VIB | 7 | 1101 | 4 |
| DOOR | 4 | 11001 | 5 |
| FAULT | 2 | 110000 | 6 |
| RESET | 1 | 110001 | 6 |

Note: Different left/right assignments can produce different binary strings while maintaining the same optimal code lengths and weighted average.

## 3.6 Average Code Length

The weighted average code length is:

\[
L_{\text{avg}}=\sum_{i=1}^{n}P(x_i)\times l_i
\]

Substituting the code lengths:

\[
L=0.52(1)+0.14(3)+0.11(3)
\]

\[
+0.09(3)+0.07(4)+0.04(5)
\]

\[
+0.02(6)+0.01(6)
\]

\[
L=0.52+0.42+0.33+0.27
\]

\[
+0.28+0.20+0.12+0.06
\]

\[
\boxed{L_{\text{avg}}=2.20\text{ bits/message}}
\]

## 3.7 Compression Ratio

\[
CR=\frac{L_{\text{compressed}}}{L_{\text{original}}}
\]

\[
CR=\frac{2.20}{3}
\]

\[
\boxed{CR=0.7333}
\]

## 3.8 Percentage Bandwidth Savings

\[
Savings=\left(1-\frac{L_{\text{compressed}}}
{L_{\text{original}}}\right)\times100
\]

\[
Savings=\left(1-\frac{2.20}{3}\right)\times100
\]

\[
\boxed{Savings=26.67\%}
\]

## 3.9 Huffman Optimality Proof

Huffman Coding produces an optimal prefix-free binary code using the greedy-choice property.

**Sibling Property:**

There exists an optimal prefix-code tree in which the two symbols with the smallest frequencies are sibling leaves at the maximum depth.

**Exchange Argument:**

If the two smallest-frequency symbols are not at maximum depth in an optimal tree, their positions can be exchanged with deeper leaves without increasing the weighted path length.

Since their frequencies are the smallest, placing them at greater depths does not increase the total weighted cost.

**Greedy Choice:**

Combining the two least-frequent symbols into a single pseudo-symbol reduces the problem to a smaller equivalent prefix-coding problem.

Applying this process repeatedly constructs an optimal Huffman tree.

Therefore, Huffman Coding minimizes:

\[
\boxed{\sum_{i=1}^{n}f_i l_i}
\]

among binary prefix-free codes for the given symbol frequencies.

---

# 4. Question 2 – Shannon-Fano Coding and Suboptimality

## 4.1 Objective

Implement Shannon-Fano Coding and demonstrate that its greedy partitioning strategy does not always produce an optimal prefix-free code.

## 4.2 Shannon-Fano Algorithm

Shannon-Fano Coding is a top-down recursive coding technique.

### Algorithm Steps

1. Sort symbols in descending order of frequency.
2. Divide the sorted symbols into two groups.
3. Select the partition that makes the group frequency totals as close as possible.
4. Assign 0 to one group and 1 to the other.
5. Recursively divide each group.
6. Continue until every group contains one symbol.

## 4.3 Algorithmic Limitation

Shannon-Fano uses a top-down partitioning approach.

Although it generates valid prefix-free codes, its locally balanced partitions do not guarantee a globally minimum weighted path length.

Huffman Coding instead uses a bottom-up greedy merging strategy that guarantees optimality.

## 4.4 Suboptimal Counterexample

The application must provide a separate counterexample frequency distribution for which:

\[
L_{\text{Shannon-Fano}}>L_{\text{Huffman}}
\]

The counterexample must be identified programmatically and independently validated.

The implementation must:

1. Generate candidate frequency distributions.
2. Run Shannon-Fano on each candidate.
3. Run standard Huffman on the same candidate.
4. Calculate both weighted average code lengths.
5. Select a candidate where Shannon-Fano has a strictly higher average code length.
6. Verify that both resulting codebooks are prefix-free.

The mathematical specification must record the selected counterexample, its input frequencies, both codebooks, and the numerical comparison after the implementation has validated it.

A counterexample must not be fabricated or assumed from the default assignment distribution.

## 4.5 Comparison Metrics

| Metric | Huffman | Shannon-Fano |
|---|---|---|
| Construction approach | Bottom-up | Top-down |
| Strategy | Greedy merging | Recursive partitioning |
| Prefix-free codes | Yes | Yes |
| Guaranteed optimality | Yes | No |
| Weighted path length | Minimum | Not necessarily minimum |

---

# 5. Question 3 – Linear-Time Huffman Construction

## 5.1 Objective

Demonstrate that Huffman tree construction can be performed in linear time when the original frequencies are already sorted.

## 5.2 Standard Min-Heap Approach

The standard Huffman algorithm uses a min-heap priority queue.

For every merge operation:

1. Extract the two minimum-frequency nodes.
2. Merge them.
3. Insert the new internal node.

There are \(n-1\) merge operations.

Each heap operation requires logarithmic time.

Therefore:

\[
\boxed{T(n)=O(n\log n)}
\]

## 5.3 Two-Queue Algorithm

The Two-Queue algorithm uses two sorted queues.

**Queue 1:** Contains the original leaf nodes sorted by frequency.

**Queue 2:** Contains newly generated internal nodes.

### Algorithm Steps

1. Sort all original frequencies in ascending order.
2. Insert the original nodes into Queue 1.
3. Keep Queue 2 initially empty.
4. Select the smallest available node from the fronts of both queues.
5. Repeat to select the second-smallest node.
6. Merge the selected nodes.
7. Insert the resulting node into Queue 2 while preserving sorted order.
8. Continue until one node remains.

Because newly generated nodes have frequencies no smaller than the nodes previously extracted, Queue 2 can be maintained in sorted order by appending the merged nodes.

## 5.4 Time Complexity Analysis

Each original node is removed once.

Each generated internal node is removed once.

There are \(n\) original nodes and \(n-1\) internal nodes.

The queue-front comparisons and removals take constant time.

Therefore, when the input frequencies are already sorted:

\[
\boxed{T(n)=O(n)}
\]

If the sorting operation is included:

\[
T(n)=O(n\log n)+O(n)
\]

\[
\boxed{T(n)=O(n\log n)}
\]

## 5.5 Algorithm Comparison

| Property | Min-Heap Huffman | Two-Queue Huffman |
|---|---|---|
| Data structure | Priority queue | Two sorted queues |
| Input sorting | Not required beforehand | Required |
| Construction after sorting | \(O(n\log n)\) | \(O(n)\) |
| Overall with sorting | \(O(n\log n)\) | \(O(n\log n)\) |
| Optimal weighted path length | Yes | Yes |

Both algorithms must produce the same optimal weighted path length.

Their exact binary codewords may differ due to tie-breaking.

---

# 6. Question 4 – Network Bandwidth Optimization

## 6.1 Objective

Calculate the amount of network bandwidth saved by replacing fixed-length encoding with Huffman Coding.

## 6.2 Network Configuration

| Parameter | Value |
|---|---:|
| Network capacity | 9,600 bits/sec |
| Aggregate messages | 40 messages/sec |
| Original code length | 3 bits |
| Huffman average code length | 2.20 bits |

## 6.3 Original Transmission Rate

The original data rate is:

\[
R_{\text{original}}=
MessageRate\times FixedBits
\]

\[
R_{\text{original}}=40\times3
\]

\[
\boxed{R_{\text{original}}=120\text{ bps}}
\]

## 6.4 Compressed Transmission Rate

\[
R_{\text{compressed}}=
MessageRate\times AverageBits
\]

\[
R_{\text{compressed}}=40\times2.20
\]

\[
\boxed{R_{\text{compressed}}=88\text{ bps}}
\]

## 6.5 Bandwidth Saved Per Second

\[
R_{\text{saved}}=
R_{\text{original}}-R_{\text{compressed}}
\]

\[
R_{\text{saved}}=120-88
\]

\[
\boxed{R_{\text{saved}}=32\text{ bps}}
\]

## 6.6 Bandwidth Saved Per Hour

One hour contains:

\[
3600\text{ seconds}
\]

Therefore:

\[
B_{\text{saved}}=32\times3600
\]

\[
\boxed{B_{\text{saved}}=115,200\text{ bits/hour}}
\]

In bytes:

\[
\frac{115,200}{8}=14,400\text{ bytes}
\]

## 6.7 Network Utilization

Original network utilization:

\[
U_{\text{original}}=
\frac{120}{9600}\times100
\]

\[
\boxed{U_{\text{original}}=1.25\%}
\]

Compressed network utilization:

\[
U_{\text{compressed}}=
\frac{88}{9600}\times100
\]

\[
\boxed{U_{\text{compressed}}=0.917\%}
\]

## 6.8 Bandwidth Comparison

| Metric | Fixed-Length | Huffman |
|---|---:|---:|
| Bits/message | 3 | 2.20 |
| Messages/sec | 40 | 40 |
| Data rate | 120 bps | 88 bps |
| Network capacity | 9,600 bps | 9,600 bps |
| Network utilization | 1.25% | 0.917% |
| Bandwidth saved/hour | 0 | 115,200 bits |

**Note:** These calculations represent theoretical payload compression. The actual simulation may additionally account for packet headers, codebook broadcasting, framing, and communication overhead.

The 5,000 sensors represent the network population. The specified 40 messages per second is the aggregate traffic rate.

---

# 7. Question 5 – Length-Limited Huffman Coding Using Package-Merge

## 7.1 Objective

The receiver firmware has a restriction that no binary codeword can exceed four bits.

Ordinary Huffman Coding minimizes average code length without imposing a maximum depth.

For the given frequency distribution, the ordinary Huffman tree produces codewords as long as six bits.

Therefore, the ordinary Huffman codebook is not directly compatible with the receiver firmware.

A length-limited coding algorithm is required.

## 7.2 Hardware Constraint

\[
\boxed{l_i\leq4}
\]

Where \(l_i\) is the length of the codeword assigned to symbol \(i\).

## 7.3 Package-Merge Algorithm

Package-Merge is an algorithm for constructing an optimal length-limited prefix code.

It finds the minimum weighted path length subject to a maximum codeword length.

### Algorithm Overview

1. Create leaf items using the symbol weights.
2. Sort the items by increasing weight.
3. Construct successive package levels.
4. Pair adjacent items to form packages.
5. Merge packages with the original leaf items.
6. Repeat the process up to the configured maximum code length.
7. Select the required lowest-weight items.
8. Unpack the selected packages to determine symbol code lengths.
9. Generate a canonical prefix code from the resulting lengths.

The implementation must correctly handle package weights, package identities, and symbol multiplicities.

Simply truncating ordinary Huffman codes is not a valid implementation of Package-Merge.

## 7.4 Length-Limited Codebook

For the supplied distribution, one optimal length-limited code assignment is:

| Symbol | Frequency | Binary Code | Code Length |
|---|---:|---|---:|
| OK | 52 | 0 | 1 |
| TEMP_HI | 14 | 100 | 3 |
| TEMP_LO | 11 | 1010 | 4 |
| HUM | 9 | 1011 | 4 |
| VIB | 7 | 1100 | 4 |
| DOOR | 4 | 1101 | 4 |
| FAULT | 2 | 1110 | 4 |
| RESET | 1 | 1111 | 4 |

## 7.5 Average Length of Constrained Code

\[
L_{\text{limited}}=\sum p_i l_i
\]

\[
L_{\text{limited}}=
0.52(1)+0.14(3)
\]

\[
+0.11(4)+0.09(4)+0.07(4)
\]

\[
+0.04(4)+0.02(4)+0.01(4)
\]

\[
\boxed{L_{\text{limited}}=2.30\text{ bits/message}}
\]

## 7.6 Compression Savings

\[
Savings=
\frac{3-2.30}{3}\times100
\]

\[
\boxed{Savings=23.33\%}
\]

## 7.7 Comparison of Ordinary and Length-Limited Huffman

| Metric | Ordinary Huffman | Length-Limited |
|---|---:|---:|
| Average code length | 2.20 bits | 2.30 bits |
| Maximum code length | 6 bits | 4 bits |
| Firmware compatible | No | Yes |
| Compression savings | 26.67% | 23.33% |
| Bandwidth saved/hour | 115,200 bits | 100,800 bits |

The constrained solution sacrifices some compression efficiency to satisfy receiver hardware limitations.

## 7.8 Kraft Inequality Validation

For a binary prefix-free code, Kraft's inequality must hold:

\[
\sum_{i=1}^{n}2^{-l_i}\leq1
\]

For the length-limited code:

\[
2^{-1}+2^{-3}+6(2^{-4})
\]

\[
=0.5+0.125+0.375
\]

\[
\boxed{1.0\leq1}
\]

Therefore, the code lengths satisfy Kraft's inequality with equality.

The generated canonical code is also prefix-free.

## 7.9 Package-Merge Optimality

Package-Merge optimizes the weighted path length subject to the maximum permitted code length.

Its objective is:

\[
\min\sum_{i=1}^{n}f_i l_i
\]

Subject to:

\[
1\leq l_i\leq L_{\max}
\]

and the binary prefix-code feasibility constraint.

The implementation must be validated against exhaustive feasible length assignments for small symbol sets.

This provides independent verification that the generated length-limited solution is optimal.

---

# 8. Entropy and Theoretical Compression Limit

Shannon entropy measures the theoretical information content of the symbol distribution.

It is calculated as:

\[
H(X)=-\sum_{i=1}^{n}p_i\log_2(p_i)
\]

Entropy provides a lower bound on the average code length of a binary lossless prefix code.

For a valid binary prefix code:

\[
H(X)\leq L_{\text{avg}}
\]

For the default distribution, entropy should be calculated programmatically from the eight probabilities.

The application should display:

- Shannon entropy.
- Huffman average code length.
- Length-limited average code length.
- Difference between entropy and actual average code length.

This helps explain the efficiency of the generated codes.

---

# 9. Mathematical Validation and Testing

All algorithms must be validated before their results are displayed as final results.

## 9.1 Probability Validation

\[
\sum_{i=1}^{n}p_i=1
\]

The input distribution must contain valid nonnegative frequencies and at least two positive-frequency symbols for binary tree construction.

## 9.2 Prefix-Free Validation

No generated codeword should be the prefix of another codeword.

## 9.3 Kraft Inequality

\[
\sum_{i=1}^{n}2^{-l_i}\leq1
\]

## 9.4 Huffman Optimality Validation

For small test distributions, compare the Huffman weighted path length with an exhaustive search over feasible prefix-code length assignments.

## 9.5 Two-Queue Validation

The Two-Queue implementation must produce the same optimal weighted path length as standard min-heap Huffman.

## 9.6 Shannon-Fano Validation

Verify that the generated codebook is prefix-free and that the selected counterexample has:

\[
L_{\text{Shannon-Fano}}>L_{\text{Huffman}}
\]

## 9.7 Package-Merge Validation

Verify:

- Maximum code length does not exceed four bits.
- Kraft inequality is satisfied.
- The code is prefix-free.
- The weighted path length is optimal under the constraint.

## 9.8 Encoding and Decoding Validation

For every valid input message sequence:

\[
Decode(Encode(X))=X
\]

## 9.9 Network Calculation Validation

Check the following expected values for unconstrained Huffman:

| Metric | Expected Value |
|---|---:|
| Original bitrate | 120 bps |
| Compressed bitrate | 88 bps |
| Bandwidth freed | 32 bps |
| Bandwidth freed/hour | 115,200 bits |
| Original utilization | 1.25% |
| Compressed utilization | 0.917% |

For length-limited coding:

| Metric | Expected Value |
|---|---:|
| Average bits/message | 2.30 |
| Compressed bitrate | 92 bps |
| Bandwidth freed | 28 bps |
| Bandwidth freed/hour | 100,800 bits |

---

# 10. Expected Mathematical Results

The following table summarizes the expected baseline results for the supplied assignment distribution.

| Requirement | Algorithm | Expected Result |
|---|---|---|
| Q1 | Huffman Coding | 2.20 bits/message |
| Q2 | Shannon-Fano | Valid prefix-free code; counterexample must be independently verified |
| Q3 | Two-Queue Huffman | O(N) construction after sorting |
| Q4 | Network Optimization | 115,200 bits/hour saved |
| Q5 | Package-Merge | Maximum code length of 4 bits |

---

# 11. Conclusion

The mathematical model demonstrates how variable-length prefix-free coding can reduce telemetry transmission requirements in bandwidth-constrained Industrial IoT environments.

Huffman Coding provides the optimal unconstrained prefix code for the observed symbol distribution, reducing the average message length from 3 bits to 2.20 bits.

The Shannon-Fano implementation demonstrates the limitations of top-down partitioning, while the Two-Queue implementation demonstrates how sorted input frequencies enable linear-time Huffman tree construction.

The network analysis quantifies the theoretical bandwidth savings, and the Package-Merge algorithm provides an optimal length-limited code that satisfies the receiver firmware's four-bit restriction.

Together, these techniques connect algorithm design, data structures, mathematical optimization, network performance, and embedded hardware constraints in one integrated engineering application.

---

**End of Mathematical Specification**

Project: Industrial IoT Telemetry Compression & Network Optimization Dashboard  
Course: 23I501 – Design and Analysis of Algorithms  
Institution: PSG College of Technology  
Batch: 8 – IoT / Embedded Systems
