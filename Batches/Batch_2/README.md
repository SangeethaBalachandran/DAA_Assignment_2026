\# Telecom: Fibre Rollout Connecting Towns



\*\*Course:\*\* 23I501 – Design and Analysis of Algorithms  

\*\*Batch:\*\* 2

\## Presentation: https://drive.google.com/file/d/18pKHVlA59giDiKI9e0uG1wxuDooGN4wI/view?usp=sharing

\## Files



\- `telecom\_fibre.py` – Python implementation of the project algorithms and demonstrations.



\## Problem


Connect all seven towns using fibre-optic links at minimum total trenching cost. The graph is undirected and weighted. Costs are in lakh rupees.



\## Algorithms included



1\. \*\*Kruskal's MST\*\* – sorts links by cost and uses Disjoint Set Union (DSU) to avoid cycles.

2\. \*\*Prim's MST\*\* – grows the network from Coimbatore using a min-heap.

3\. \*\*Geographic split demonstration\*\* – shows why solving two regions independently and joining them may not give the global MST.

4\. \*\*Mandatory link\*\* – forces the CBE–ERD link into the spanning tree before running Kruskal.

5\. \*\*Salem degree constraint\*\* – finds the minimum tree where Salem has at most one incident fibre link.

6\. \*\*Benchmark\*\* – compares Kruskal with a brute-force MST method on five small complete graphs (4–8 vertices).



\## Run the program



Install Python 3 if it is not already installed. No external packages are required.



Open Command Prompt or the VS Code terminal in this folder and run:



```bash

python telecom\_fibre.py

```



On some Windows installations, use:



```bash

py telecom\_fibre.py

```



\## Expected key results



\- Normal MST: \*\*Rs. 27 lakh\*\*

\- Mandatory CBE–ERD link: \*\*Rs. 31 lakh\*\*

\- Salem degree at most one: \*\*Rs. 27 lakh\*\*

\- Geographic split example: \*\*Rs. 33 lakh\*\*, compared with the global MST of \*\*Rs. 27 lakh\*\*



Kruskal and Prim may print different edge orders, but their minimum total costs should match. If multiple equal-cost MSTs exist, their selected links may also differ.



\## Complexity



Let `V` be the number of towns and `E` the number of available links.



\- Kruskal: `O(E log E)` time; `O(V + E)` space for the edge list and DSU.

\- Prim with adjacency list and binary heap: `O(E log V)` time; `O(V + E)` space.

\- Brute force: examines combinations of `E` edges taken `V-1` at a time, so it is only suitable for very small graphs.



The timing output is generated on the computer running the program. Actual times depend on the machine and should be copied into the presentation only after running the code.



\## Editing the input given



To change the network, edit the `EDGES` list in `telecom\_fibre.py`. Each item has this format:



```python

("CBE", "TUP", 5)

```



This means there is a fibre link between Coimbatore (`CBE`) and Tiruppur (`TUP`) with a cost of Rs. 5 lakh.



