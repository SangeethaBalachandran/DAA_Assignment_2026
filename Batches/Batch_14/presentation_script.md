# Presentation script — Batch 14: Valid ECU Feature Configurations
Target total ≈ 10:45 (limit 12:00). Slide numbers match `slides.pdf`. All figures are from the programs in `code/`.

| Member | Slides | Time |
|---|---|---|
| 1 | 1–3 | 2:00 |
| 2 | 4–6 | 2:00 |
| 3 | 7–9 | 2:15 |
| 4 | 10–12 | 2:15 |
| 5 | 13–15 | 2:15 |

---
## MEMBER 1 — Introduction and the automotive ECU problem (2:00)
**Slide 1 (0:20).** "Good day. We are Batch 14 from the IT department of PSG College of Technology. Our topic for 23I501 is *valid ECU feature configurations*. I'm `Aryaa Madhavan`; my teammates will introduce themselves when they start." (point to the member/part table.)

**Slide 2 (0:55).** "A car maker ships one ECU firmware that is configured per vehicle variant. Our scenario has seven optional binary features: four functions, ACC adaptive cruise, BC basic cruise, LKA lane keep assist and PA park assist; and three sensors, radar at ₹12,000, camera at ₹8,000 and ultrasonic at ₹5,000. Functions depend on sensors, and sensors are limited by a budget. A real product line has about 200 optional features, and the test team must list every valid configuration to plan coverage. So the question is: of the 2^7 = 128 raw on/off vectors, which are valid?"

**Slide 3 (0:45).** "The rules: ACC needs radar, LKA needs camera, PA needs ultrasonic, ACC excludes BC, at least one cruise function must be present, and the total sensor cost must not exceed ₹20,000. Formally the input is seven binary features plus these constraints; the output is the set of *all* valid vectors. There is no objective to optimise, so this is an **enumeration** problem, a constraint satisfaction problem. Both our programs found **19 valid configurations**. Brute force is fine for seven features but impossible for 200 (2^200 ≈ 1.6×10^60), which is why we need pruning and later pairwise testing. Now `Maileshwaran S` will model this formally."

## MEMBER 2 — CSP modelling, variables and constraints (2:00)
**Slide 4 (0:40).** "Thanks. I'm `Maileshwaran S`. We model it as a CSP: variables X are the seven features, each with domain {0,1}. The search space is 2^7 = 128 complete vectors, of which 19 are valid, about 15 %. The only unary constraint is the domain itself, because no feature is forced on or off. Sensor variables carry a cost when they are set to 1."

**Slide 5 (0:50).** "Constraints and classification. C1 to C3 are the 'requires' rules, implications between two variables, so **binary**. C4, ACC excludes BC, is binary. C5, at least one of ACC or BC, is also a two-variable clause; I classify it as binary, with the note that it generalises to a global at-least-one rule over a group. C6, the cost budget, 12000·RAD + 8000·CAM + 5000·US ≤ 20000, involves three variables in a linear inequality, so it is **global**. It is also monotone: costs are non-negative, so a partial sum above ₹20,000 can never recover. That makes early pruning safe. It forbids exactly radar, camera and ultrasonic together, ₹25,000."

**Slide 6 (0:30).** "This is the constraint graph. Green edges are dependencies from functions to sensors. The red edge is ACC–BC: exactly one cruise function. The shaded group on the right is the global cost constraint. Notice the three green constraints end in the sensors, which will matter for variable ordering. `Nishwanth B` will now present the algorithm."

## MEMBER 3 — Backtracking and rejection of other techniques (2:15)
**Slide 7 (0:50).** "I'm `Nishwanth B`. Our technique is **backtracking** with incremental constraint checking. We assign variables one at a time; each constraint is checked as soon as its last variable is assigned, and the running sensor cost is checked at every step. The key property is that a violated constraint over assigned variables stays violated in every extension, and the partial cost only grows, so the whole subtree can be skipped with no solution lost. The pseudocode is on the slide. For the ECU, features-first order makes 66 recursive calls and examines 94 assignments; sensors-first makes 67 calls and 96. The full tree would have 255 nodes."

**Slide 8 (1:00).** "Why not the others? **Divide and conquer**: the halves share constraints. Splitting features from sensors gives 8 left assignments and 7 right ones, and the merge has to test 56 pairs to find 19, and in general 2^n pairs, so T(n) = 2T(n/2) + Θ(2^n). **Greedy** makes irrevocable choices and returns one configuration; we need 19. If it turns ACC on first it can never reach the 14 BC configurations. **Dynamic programming** can only count: its state needs the pending dependencies, which form a subset, so up to 2^k states, and listing the configurations means walking the table again, which is backtracking. **Branch and bound** needs an objective: the cheapest valid configuration is {BC} at ₹0, and bounding with it would prune the other 18 valid ones. Only feasibility bounds are valid, and that is exactly our pruning."

**Slide 9 (0:25).** "Correctness in three parts. Soundness: a leaf is reached only after every constraint was checked with its full scope assigned. Completeness: by induction, every prefix of a valid configuration passes the checks, because a check can fail only when the configuration is already invalid. Uniqueness: every configuration corresponds to exactly one path. The exhaustive program gives the identical 19 configurations. Over to `Param Vijayeshvar`."

## MEMBER 4 — Valid configurations, trace, variable ordering, data structures (2:15)
**Slide 10 (0:40).** "I'm `Param Vijayeshvar`. Here are all 19 valid configurations, columns ACC, BC, LKA, PA, RAD, CAM, US. Fourteen contain BC and five contain ACC. A hand check: for BC, the seven allowed sensor sets give 1, 2, 2, 4, 1, 2, 2 choices of LKA and PA, a total of 14; for ACC, radar is forced, and the three sets give 1 + 2 + 2 = 5. Backtracking examined 94 assignments, 29 pruned, instead of 254 for the full tree and 128 leaves."

**Slide 11 (0:45).** "This is the trace, features-first. ACC=0 is fine but then BC=0 is pruned immediately because neither cruise function is on; BC=1 continues. ACC=1 with BC=1 is pruned by the exclusion. Deeper, you see the other prunes: ACC without RAD at depth 5, all three sensors costing ₹25,000 at depth 7, PA without US, LKA without CAM. The complete 148-line trace is in the README."

**Slide 12 (0:50).** "Variable ordering. Features-first does slightly less total work, 66 calls against 67, because the ACC/BC rule closes at depth 2 and removes two large subtrees. Sensors-first rejects earlier on average, mean prune depth 5.6 against 6.2, because requirements and the budget close earlier. The difference is small for seven variables; the principle is to close constraints as early as possible. On the right: bit vectors give O(1) per constraint and handle the budget; an implication graph costs O(n+E) per full check and cannot express the cost; a BDD checks in O(n); we measured 23 nodes in features-first order and 24 in sensors-first order. Next, `Sanjith B K`."

## MEMBER 5 — Complexity, benchmarking, worst case, pairwise testing (2:15)
**Slide 13 (0:45).** "I'm `Sanjith B K`. Time is the number of visited nodes times the incremental check cost, plus n per solution. Best case is O(1) when the first variable contradicts, or output-sensitive O(n·|S|) with no dead ends; the worst case is Θ(2^n); space is O(n). Our constructed worst case has no constraint, or only one between the first and last variable of the order, so nothing is pruned early. Measured at n = 15: 65,534 assignments out of 65,534 possible, 65,535 calls, and with the late constraint 57,343 calls and 8,192 pruned only at the last level."

<!--SCRIPT14-START-->
**Slide 14 (0:50).** "Benchmark, median of five runs. The first size is the real ECU; 9 to 21 features are seeded synthetic instances. Exhaustive time grows about four times per two extra features: 37 ms at 15 features to 2.4 seconds at 21. Backtracking took 9 ms at 15 and 56 ms at 21. Its time follows the assignments examined, about a microsecond each: 48,206 against 2,097,152 at n = 21, a 42-times speed-up. Limits: noise below a millisecond at small n, the instances are synthetic, and exhaustive search at 30 features was not run."
<!--SCRIPT14-END-->

**Slide 15 (0:40).** "Changed requirement: with 200 features listing everything is impossible, so we generate a pairwise test set: every feasible pair of feature settings appears at least once. We compute feasible pairs by propagating two settings through the implication graph, then greedily build tests that cover the most uncovered pairs. For the real ECU, 6 tests cover all 78 feasible pairs, down from 19 valid configurations. For 200 *synthetic, illustrative* features, 58 tests cover all 77,964 feasible pairs out of 79,600. This is a greedy result, not proven optimal. Thank you; we welcome your questions."
