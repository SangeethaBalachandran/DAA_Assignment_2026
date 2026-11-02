# Academic Project Report Outline
## Industrial IoT Telemetry Compression & Network Optimization Platform

- **Institution:** Department of Computer Science & Engineering
- **Subject:** Design and Analysis of Algorithms (DAA) / Cyber-Physical Systems
- **Project Title:** Interactive Industrial IoT Telemetry Compression & Network Optimization Dashboard
- **Document Version:** 1.0.0

---

## Complete Table of Contents & Chapter Breakdown

### Title Page & Front Matter
- **Title:** Industrial IoT Telemetry Compression & Network Optimization Platform
- **Sub-Title:** Mathematical Formulation, Linear-Time Algorithmic Synthesis, and Length-Limited Firmware Deployment for Narrowband Edge Sensor Networks
- **Abstract:** Concise summary of the 5,000 sensor population, 9.6 kbps link constraint, fixed 3-bit to variable-length prefix-free codebook transition, Huffman optimality, Shannon-Fano suboptimality, Two-Queue linear-time construction, Package-Merge 4-bit hardware compliance, and full-stack implementation.
- **Acknowledgements & Declaration of Originality**
- **List of Figures, List of Tables, List of Algorithms**
- **List of Mathematical Symbols & Abbreviations**

---

### Chapter 1: Introduction & Problem Context
- 1.1 The Narrowband Industrial IoT Bottleneck (RS-485, Sub-GHz, PLC, Satellite).
- 1.2 Fixed-Length Encoding Inefficiencies:
  - Uniform 3-bit allocation for 8 states.
  - Symmetrical cost penalty for nominal vs critical alarms.
- 1.3 Embedded Receiver Hardware Constraints:
  - Microcontroller register limits (4-bit nibble manipulation).
  - Risk of register overflow in unconstrained Huffman codes.
- 1.4 Project Objectives & Engineering Scope:
  - Mathematical proof of optimality.
  - Construction of valid counterexample for Shannon-Fano.
  - Linear-time Two-Queue implementation.
  - Length-limited prefix coding via Package-Merge.
  - Full-stack interactive real-time platform.

---

### Chapter 2: Theoretical Foundations & Information Theory
- 2.1 Discrete Memoryless Source (DMS) Formulation.
- 2.2 Shannon Source Coding Theorem:
  - Definition of Information Entropy $H(X) = -\sum p_i \log_2(p_i)$.
  - Calculation for the calibrated 8-symbol telemetry distribution ($H(X) = 2.1843$ bits/msg).
- 2.3 Prefix-Free (Instantaneous) Codes:
  - Definition and Kraft-McMillan Inequality: $\sum 2^{-l_i} \le 1$.
  - Instantaneous decoding without delimiter overhead.
- 2.4 Coding Efficiency and Redundancy Metrics:
  - Average code length $L = \sum p_i \cdot l_i$.
  - Efficiency $\eta = H(X)/L$.
  - Redundancy $R = L - H(X)$.

---

### Chapter 3: Optimal Huffman Coding
- 3.1 Min-Heap Algorithmic Mechanics ($O(N \log N)$).
- 3.2 Step-by-Step Tree Merge Trace for the 8-Symbol Distribution:
  - Intermediate nodes: 3, 7, 14, 20, 28, 48, 100.
- 3.3 Derived Huffman Codebook:
  - Calculated code lengths: OK (1), TEMP_HI (3), TEMP_LO (3), HUM (3), VIB (4), DOOR (5), FAULT (6), RESET (6).
  - Average code length: $L = 2.2000$ bits/message.
  - Theoretical bandwidth reduction: $26.67\%$.
- 3.4 Mathematical Proof of Huffman Optimality:
  - Sibling property of optimal trees.
  - Exchange argument proof for the greedy-choice property.
  - Inductive proof of optimal substructure.
- 3.5 Hardware Incompatibility Analysis:
  - Why $l(\text{DOOR})=5$, $l(\text{FAULT})=6$, and $l(\text{RESET})=6$ preclude direct deployment in 4-bit firmware registers.

---

### Chapter 4: Shannon-Fano Coding & Suboptimality
- 4.1 Top-Down Recursive Bipartitioning Mechanics.
- 4.2 Behavior on the Telemetry Distribution:
  - Fortuitous root alignment (52 vs 48 split).
- 4.3 Proven Counterexample Analysis:
  - Classic 5-symbol case: $\Sigma = [35, 17, 17, 16, 15] \implies L_{\text{SF}} = 2.3100$ vs $L_{\text{Huff}} = 2.3000$ bits.
  - 8-symbol IoT case: $\Sigma = [37, 16, 16, 9, 7, 7, 5, 3] \implies L_{\text{SF}} = 2.6900$ vs $L_{\text{Huff}} = 2.6500$ bits.
- 4.4 Theoretical Root Cause of Shannon-Fano Suboptimality:
  - Irreversible greedy local decisions at the root level vs global bottom-up agglomeration.

---

### Chapter 5: Linear-Time Huffman via Two Queues
- 5.1 The van Leeuwen (1976) Algorithm Formulation.
- 5.2 Queue Data Structures:
  - Queue 1 (Leaf nodes sorted ascending).
  - Queue 2 (Generated internal nodes).
- 5.3 Formal Proof of Invariant Monotonicity:
  - Mathematical induction demonstrating Queue 2 is sorted for all steps.
- 5.4 Algorithmic Complexity Comparison:
  - $O(N)$ operations when pre-sorted.
  - Clarification on sorting prerequisites ($O(N \log N)$ vs integer bucket sorting).
- 5.5 Empirical Operation and Execution Benchmarks:
  - Comparative timing data across $N = 8$ to $1024$.

---

### Chapter 6: Length-Limited Huffman via Package-Merge
- 6.1 Constrained Optimization Formulation:
  - $\min \sum p_i l_i$ subject to $\sum 2^{-l_i} \le 1$ and $l_i \le L_{\max}$.
- 6.2 The Larmore-Hirschberg (1990) Package-Merge Reduction:
  - Coin collector knapsack problem.
  - Packaging pairs and merging across $L_{\max}$ levels.
- 6.3 Application to $L_{\max} = 4$ Bits:
  - Derived code lengths: OK (1), TEMP_HI (3), and 6 symbols at 4 bits.
  - Average code length: $L = 2.3000$ bits/message.
  - Kraft sum equality: $\sum 2^{-l_i} = 1.0000$.
- 6.4 Independent Global Optimality Validation:
  - Brute-force validation over $4^8 = 65,536$ search space.
- 6.5 Engineering Trade-off Analysis:
  - 0.1000 bit/message trade-off (4.5% efficiency cost) for 100% hardware compliance.

---

### Chapter 7: Network Bandwidth & Capacity Simulation
- 7.1 Mathematical Model of Narrowband Link:
  - $C = 9,600$ bps, $\lambda = 40$ msgs/s.
- 7.2 Quantitative Bitrate Calculations:
  - Original: 120.0 bps (1.250% utilization).
  - Compressed: 92.0 bps (0.958% utilization).
  - Bandwidth freed: 28.0 bps (23.33% savings).
  - Bandwidth freed per hour: 100,800 bits (12.60 kBytes).
- 7.3 Capacity Expansion Potential:
  - Headroom increase allowing $+14.54$ msgs/s or $+1,818$ sensors.
- 7.4 Protocol Framing & Physical Overhead Modeling:
  - 32-bit CRC16 frame encapsulation.

---

### Chapter 8: Over-the-Air Codebook Management
- 8.1 Codebook Versioning Protocol (`v1.0.0`, `v1.0.1`).
- 8.2 Broadcast Payload Structure:
  - 80 bits table payload + 32 bits framing = 112 bits/hour.
  - Amortized continuous bitrate: 0.0311 bps (< 0.00032% link load).
- 8.3 Receiver Synchronization Simulation:
  - ACK tracking across 5,000 nodes.
  - Retry latency under lossy Sub-GHz channels.
- 8.4 Version Mismatch Prevention:
  - Rejection of decoding with outdated codebook versions.

---

### Chapter 9: Software Architecture & Full-Stack Implementation
- 9.1 Backend Architecture (FastAPI, Python 3.14, Pydantic v2).
- 9.2 Frontend Architecture (React 18, TypeScript, Vite, Tailwind CSS v4).
- 9.3 Interactive Data Visualizations:
  - React Flow recursive binary tree layout with $0/1$ edge labeling.
  - Recharts real-time throughput area charts.
- 9.4 Real-Time Streaming via WebSockets (`/ws/telemetry`).
- 9.5 Automated Test Suite (Pytest: 16/16 Passed).

---

### Chapter 10: Experimental Results & Benchmarks
- 10.1 Mathematical Verification Matrix.
- 10.2 Encoder/Decoder Roundtrip Lossless Verification.
- 10.3 Empirical Runtime Comparison ($O(N)$ vs $O(N \log N)$).
- 10.4 1-Hour Network Projection Analysis (144,000 messages).

---

### Chapter 11: Conclusions & Future Work
- 11.1 Project Summary & Key Findings.
- 11.2 Adaptive Online Codebook Re-Estimation (Adaptive Huffman / Vitter).
- 11.3 Multi-Symbol Block Compression & Arithmetic Coding Comparison.
- 11.4 Hardware Firmware Deployment Guidelines (ARM Cortex-M0+ C implementation).

---

### References & Appendices
- **References:** Huffman (1952), Shannon (1948), Fano (1949), van Leeuwen (1976), Larmore & Hirschberg (1990).
- **Appendix A:** Complete `telemetry_codebook.h` C Header File.
- **Appendix B:** Full Python Source Code Listing for Algorithms.
- **Appendix C:** Pytest Test Suite Logs and Verification Outputs.

