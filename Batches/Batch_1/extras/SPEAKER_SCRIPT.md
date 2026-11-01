# Speaker scripts, timings and viva Q&A (both members)

Planned total: **10:45** (limit 12:00). Member 1: 5:45 · Member 2: 5:00. Scripts are written for a natural pace of about 130–140 words per minute: practise once with a timer and trim if you run over.

## Slide allocation

| # | Slide title | Presenter | Duration | Main purpose |
|---|---|---|---|---|
| 1 | Fintech Audit: Reconciling a Disputed Bank Debit | Member 1 | 0:35 | Introduce scenario and split of work |
| 2 | Problem Modelling | Member 1 | 0:45 | Formal problem modelling and classification |
| 3 | Data Structures and Technique Choice | Member 1 | 0:50 | Data structure choice and technique identification |
| 4 | The Algorithm | Member 1 | 0:50 | State definition, search rule, pseudocode |
| 5 | Trace on the Given Instance | Member 1 | 1:00 | Complete trace and verified counts |
| 6 | Proof of Correctness | Member 1 | 0:50 | Correctness proof |
| 7 | Complexity and a Hard Input | Member 1 | 0:55 | Complexity and worst-case input |
| 8 | Rejected: Greedy and Dynamic Programming | Member 2 | 0:55 | Reject Greedy and Dynamic Programming with evidence |
| 9 | Rejected: Divide and Conquer, Branch and Bound | Member 2 | 0:55 | Reject Divide and Conquer and Branch and Bound honestly |
| 10 | Experiments: Pruned Search vs Brute Force | Member 2 | 1:00 | Empirical comparison and growth analysis |
| 11 | Changed Requirement: ±₹50 Tolerance | Member 2 | 0:50 | Changed requirement ±₹50 |
| 12 | Real-World Reference | Member 2 | 0:40 | Real-world reference and difference from our code |
| 13 | Conclusion | Member 2 | 0:40 | Conclusion |
| | **Total** | | **10:45** | |

# Slides for Member 1

## Slide 1 — Fintech Audit: Reconciling a Disputed Bank Debit  (0:35, script 80 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- Batch 1 · 23I501 Design and Analysis of Algorithms · PSG College of Technology
- A customer disputes a debit of ₹1,10,000; no single pending transaction matches
- Pending transactions (₹ thousand): 15, 22, 35, 40, 48, 53, 61
- Task: report EVERY combination whose total is exactly 110 (real batches: 30–40 transactions)
- Part 1 (Member 1): model, technique, algorithm, trace, proof, complexity
- Part 2 (Member 2): rejected techniques, experiments, ±₹50 change, reference

*[Member 1 name, roll no.]     [Member 2 name, roll no.]   — fill in before recording*


**Suggested visual:** Title slide only. Optional: a small bank-statement icon.

**Say aloud:**

> Good morning. We are Batch 1, working on the fintech audit. A customer disputes a debit of one lakh ten thousand rupees, but no single pending transaction matches it. So the auditor must find every combination of pending transactions that adds up to exactly that amount. In a real batch there are thirty to forty transactions. I will present the model, the algorithm, its trace and its proof. My teammate will cover the rejected alternatives, the experiments and the extensions.

**Likely questions:**

- **Q:** Why not just look for one matching transaction?
  **A:** No single transaction equals 110, so the amount must be a sum of several. We have to consider combinations of any size.
- **Q:** How big is the search space in a real batch?
  **A:** With 30 to 40 transactions there are 2^30 to 2^40 subsets, about 10^9 to 10^12. Checking all of them is not acceptable, which is why we prune.

**Transition:** “First, a precise model of the problem.”

---

## Slide 2 — Problem Modelling  (0:45, script 101 words)

**Slide text (paste into PowerPoint / see slides.pdf):**


| Input | n positive integer amounts (in rupees), target T = 1,10,000, tolerance τ (0 now, ₹50 later) |
|---|---|
| Output | ALL non-empty subsets of transactions with T − τ ≤ sum ≤ T + τ |
| Objective | Completeness: none missed, none invalid, none repeated |
| Constraints | Amounts > 0 · each transaction used at most once · equal amounts are different items · integer rupees, no floats |
| Class | Enumeration (listing). Decision version is NP-complete; #solutions can be exponential |
| Classical problem | SUBSET SUM, all-solutions listing form |

- Why “every combination” matters: yes/no tables and one-path greedy cannot produce a list — we need an exhaustive generator with SAFE cut-offs

**Suggested visual:** The table itself; highlight the word “ALL” in the Output row.

**Say aloud:**

> Formally, the input is n positive amounts, converted to integer rupees, a target T, and a tolerance, zero for now. The output is all non-empty subsets whose sum lies in the allowed window. There is nothing to maximise; the objective is completeness. Each transaction is a separate item, so equal amounts are different items, and nothing is used twice. This is the Subset Sum problem in its listing form. The yes or no version is NP-complete, and the number of answers can itself be exponential. Because we must list every combination, we need an exhaustive generator whose cut-offs are provably safe.

**Likely questions:**

- **Q:** Why integers and not floats?
  **A:** Money must be exact. Floating point can make 110.0 differ from the true sum, so a valid subset could be missed. We convert thousands to rupees as integers.
- **Q:** Is the number of answers always small?
  **A:** No. If all amounts are equal, C(n, n/2) subsets qualify, so every algorithm needs time at least proportional to the output.

**Transition:** “Next: which data structure and which design technique.”

---

## Slide 3 — Data Structures and Technique Choice  (0:50, script 110 words)

**Slide text (paste into PowerPoint / see slides.pdf):**


| Structure | Cost | Space | n=40, T≈10⁹ paise |
|---|---|---|---|
| Sorted array + suffix sums (CHOSEN) | O(1) per step | O(n) | independent of T |
| DP table / bitset reach[i][s] | O(n·T) build | O(n·T) | ≈4.1×10¹⁰ cells ≈ 41 GB (5.1 GB as bits) |
| Meet-in-the-middle sorted lists | O(n·2^(n/2)) | O(2^(n/2)) | 2²⁰ ≈ 10⁶ sums per half: feasible |
| Bitmask over all subsets | O(n) per mask | O(1) | 2⁴⁰ masks: infeasible |

- TECHNIQUE: Backtracking (depth-first, build subsets in increasing order)
- Enabling property: with positive amounts, a partial sum BOUNDS every completion
- Rule A overshoot: c + vⱼ > hi  ⇒  every later item overshoots (sorted)
- Rule B unreachable: c + suffix[j] < lo  ⇒  nothing from j onward can reach lo

**Suggested visual:** The comparison table; underline the chosen row in a colour.

**Say aloud:**

> For data structures we compare four. Our choice is a sorted array of amounts with a suffix-sum array. Each step is constant time, memory is order n, and it does not depend on how large the target is. A dynamic programming table at forty items and a target near ten to the nine paise needs about forty gigabytes as bytes. For the technique we choose backtracking. The enabling property is that amounts are positive, so the current sum bounds every completion. Overshoot: if adding the next item exceeds the limit, so does every later item, because the list is sorted. Unreachable: if even adding everything left stays short, we stop.

**Likely questions:**

- **Q:** Why not Branch and Bound?
  **A:** B&B needs an objective and an incumbent to compare bounds against. We have no objective, only feasibility bounds, which is exactly constraint pruning in backtracking. A best-first B&B would add a priority queue and frontier memory without reducing the number of states.
- **Q:** What if an amount were zero or negative?
  **A:** Both lemmas fail: a later item could lower the sum, so pruning would be unsafe. The program rejects non-positive amounts.

**Transition:** “Here is the algorithm that uses these two rules.”

---

## Slide 4 — The Algorithm  (0:50, script 112 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- State = one recursive call = one candidate subset (start, c): c = its sum, start = first position that may still be added
- Children: C ∪ {j}, for j = start … n−1 in increasing order  →  every subset is built in exactly one way
- Report C if it is non-empty and lo ≤ c ≤ hi    (lo = T − τ, hi = T + τ)

```
SEARCH(start, c):
    states += 1
    if chosen ≠ ∅ and lo ≤ c ≤ hi:  record solution
    for j = start .. n-1:
        if c + suffix[j] < lo:  break      # unreachable
        if c + v[j]    > hi:    break      # overshoot
        push j;  SEARCH(j+1, c + v[j]);  pop
```

- Items sorted ascending, ties by original index (duplicates stay separate items)
- Counts: states, overshoot cut-offs, unreachable cut-offs — measured separately; printing is outside the algorithm

**Suggested visual:** Pseudocode box. Optional: arrow from the two break lines to “Rule A / Rule B” of the previous slide.

**Say aloud:**

> Here is the algorithm. A state is one recursive call, which is one candidate subset, described by its sum c and the first position start that may still be added. The children add one more item at a position j, in increasing order, so every subset is built in exactly one way. Each state first checks whether its own sum is inside the window and records it. Then the loop tries each next item. If even taking everything from j onward cannot reach the lower limit, we break. If adding item j already exceeds the upper limit, we break. Otherwise we recurse. The program counts states and both kinds of cut-off separately.

**Likely questions:**

- **Q:** Why does the loop break instead of continue?
  **A:** Items are sorted and amounts are positive. If item j overshoots, every later item is at least as large and also overshoots. If the suffix from j is too small, the suffix from any later j is smaller still. So the rest of the loop is useless.
- **Q:** How are duplicate amounts handled?
  **A:** By position. Equal amounts occupy different positions, so they are different transactions. For [5,5,5,10] and target 10 we report three pairs and the single 10.

**Transition:** “Now let us run it on the given seven transactions.”

---

## Slide 5 — Trace on the Given Instance  (1:00, script 103 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- *(figure: `results/search_tree.png`)*
- ANSWER: {22, 35, 53} and {22, 40, 48}   (both sum to 110)
- States visited = candidate subsets tested: 35 of 2⁷ = 128   (1 / 6 / 15 / 13 by size 0–3)
- Cut-offs: 28 overshoot + 7 unreachable, skipping 56 child branches · 93 subsets never generated
- Example: {15,22,35} = 72, next 40 → 112 > 110: overshoot.  {35}: 35 + 61 = 96 < 110: unreachable

**Suggested visual:** Insert results/search_tree.png (green = solutions, cut:O overshoot, cut:U unreachable). Full 35-row table in report appendix extras/TRACE.md.

**Say aloud:**

> This is the real tree produced by our program. The root is the empty set. Green nodes are solutions. The algorithm finds exactly two combinations: twenty-two plus thirty-five plus fifty-three, and twenty-two plus forty plus forty-eight. It visits thirty-five states, out of one hundred twenty-eight subsets. Each state tests its own sum once. There are twenty-eight overshoot cut-offs and seven unreachable cut-offs. For example, fifteen, twenty-two, thirty-five sums to seventy-two, and adding forty gives one hundred twelve, so that branch and everything after it is skipped. Four or more items can never work, since the four smallest already sum to one hundred twelve.

**Likely questions:**

- **Q:** How do you know the trace is right?
  **A:** It is generated by the same function that solves the problem, and the brute-force program independently returns the same two subsets.
- **Q:** What is the difference between a state and a pruned branch?
  **A:** A state is a recursive call that actually happens: 35. A cut-off is a loop break: 35 events, 28 plus 7, each skipping 1 to 4 sibling branches, 56 in total, which are never created.

**Transition:** “Why can we trust this? Next, the correctness proof.”

---

## Slide 6 — Proof of Correctness  (0:50, script 107 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- Lemma A: if c + vⱼ > hi, every non-empty D ⊆ {j..n−1} gives sum ≥ c + vⱼ > hi   (sorted, positive)
- Lemma B: if c + suffix[j] < lo, every D ⊆ {j..n−1} gives sum ≤ c + suffix[j] < lo   (positive)
- Theorem (induction on n − start): SEARCH(start, c) reports exactly the valid sets C ∪ D, D ⊆ {start..n−1}, each once
- Base: start = n → only C itself, tested at entry.   Step: split by smallest added j; no cut ⇒ induction hypothesis; cut ⇒ Lemma A/B (also for all j′ ≥ j)
- Complete: apply the Theorem at the root (C = ∅).   Sound: report only after the window test; positions strictly increase ⇒ no item twice
- No duplicates: subset ↔ one increasing sequence; parent = remove largest position
- Same proof for any τ ≥ 0: only lo and hi change

**Suggested visual:** Optional small diagram: node with fan of children; cut at j crossing out all siblings to its right.

**Say aloud:**

> The proof rests on two lemmas. Lemma A: if adding item j overshoots the upper limit, then any completion using items from j onward overshoots, because it contains some item at least as large, and amounts are positive. Lemma B: if the current sum plus everything from j onward is below the lower limit, every completion is below it. Then we prove by induction that a call reports exactly the valid completions of its current set, each once. A cut only discards completions the lemmas show are invalid. Applying it at the root gives completeness. The window test gives soundness, and the increasing order gives no duplicates.

**Likely questions:**

- **Q:** Where exactly is positivity used?
  **A:** In both lemmas: a sum never decreases when items are added, and the suffix sum is the largest possible addition.
- **Q:** Could pruning remove a valid subset that comes after a pruned one?
  **A:** No. The lemmas hold for every position j′ ≥ j, so when the test fails at j, all later siblings are invalid too.

**Transition:** “Next: how expensive is it, and what is its hardest input?”

---

## Slide 7 — Complexity and a Hard Input  (0:55, script 128 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- Time = Θ(states) + O(n log n) sort + O(output size);   states ≤ min(2ⁿ, Σ_{k≤K} C(n,k)),  K = most items that can fit
- Best Θ(n log n) · Worst Θ(2ⁿ) · Space O(n) + output.  Given instance: K = 3 ⇒ ≤ 64 states, measured 35
- Practical: target small vs batch total ⇒ small K ⇒ few states (n = 40 random batches: median 5.6×10⁵, max 8.2×10⁶ vs 2⁴⁰ ≈ 1.1×10¹²)
- Output can be exponential (equal amounts: C(n, n/2) answers) ⇒ no algorithm beats the output size
- Hard family (no solution): aᵢ = M + i, M = 10n², T = (⌊n/2⌋+1)M − 1

| n | states | C(n,n/2) | 2ⁿ | states/2ⁿ |
|---|---|---|---|---|
| 14 | 3,432 | 3,432 | 16,384 | 0.209 |
| 18 | 48,620 | 48,620 | 262,144 | 0.185 |
| 22 | 705,432 | 705,432 | 4,194,304 | 0.168 |

- Exactly C(n, ⌊n/2⌋) states (derived, verified for n = 4..22): pruning saves only ≈ √(πn/2). True worst case 2ⁿ: everything is a solution

**Suggested visual:** Table; optional bar showing states vs 2ⁿ.

**Say aloud:**

> For complexity, time is proportional to the number of states, plus sorting and the output. States are at most two to the n, and also at most the number of subsets with at most K items, where K is how many items can fit under the limit. For our instance that bound is sixty-four and we measured thirty-five. In the worst case the search is exponential. We built a hard family with no solution: amounts near a large M, and a target just below a multiple of M. The number of states is exactly n choose n over two, which we verified up to n equals twenty-two. So these pruning rules save only about a square-root factor here. The true worst case is when everything is a solution.

**Likely questions:**

- **Q:** Is this a genuine worst case?
  **A:** The family is a difficult search-only test with an exact state count. The true worst case, 2^n states, occurs when almost every subset is a solution, for example equal amounts with a huge tolerance.
- **Q:** Why is exponential time acceptable?
  **A:** Subset Sum is NP-complete and the output can itself be exponential. For audit data the target is small compared with the batch total, so K is small and the measured search stays small.

**Transition:** “My teammate will now explain why the other four techniques were rejected.”

---


# Slides for Member 2

## Slide 8 — Rejected: Greedy and Dynamic Programming  (0:55, script 123 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- GREEDY (largest that still fits): 61 → remaining 49 → 48 → remaining 1 → FAILS, reports nothing
- Yet {22,35,53} and {22,40,48} exist; neither contains 61 ⇒ greedy-choice property false at step 1 (49 is not a subset sum of the rest)
- A single path can output at most one subset; we need all
- DYNAMIC PROGRAMMING: reach[i][s] answers “is s reachable?”; listing needs all rows + a walk-back, O(n) per solution — DP CAN enumerate
- But cost depends on the VALUE of T (pseudo-polynomial): n = 40, T ≈ 10⁹ paise ⇒ 4.1×10¹⁰ cells = 41 GB (5.1 GB as bits)
- Given instance: table 888 cells vs 35 search states.  Honest note: 2⁴⁰ ≈ 1.1×10¹² > n·T, so DP has the better worst-case count — it loses on memory and on realistic batches (~5×10⁵ states)

**Suggested visual:** Small two-step diagram: 110 → 61 → 49 → 48 → 1 left (dead end).

**Say aloud:**

> I will cover the rejected techniques. Greedy takes the largest transaction that fits: sixty-one, leaving forty-nine. The largest that fits is forty-eight, leaving one thousand, and then it is stuck. It reports nothing, although two combinations exist, and neither contains sixty-one. So the greedy choice is wrong at the very first step, and a single path can never list all answers. Dynamic programming is different. It can enumerate, by walking back through the table. But its table grows with the numeric value of the target. With forty items and a target near ten to the nine paise, that is about forty gigabytes. In the pure worst case two to the forty is larger, but for realistic batches the search visits far fewer states.

**Likely questions:**

- **Q:** Does DP really fail?
  **A:** No, and we do not claim it does. It can list all solutions, but it needs memory proportional to n times T, which at paise scale is tens of gigabytes, and its cost depends on the unit used for money.
- **Q:** Could a smarter greedy work?
  **A:** Subset Sum has no known polynomial algorithm, so no simple greedy rule can be both fast and complete. Our counterexample shows the natural rule fails even on seven items.

**Transition:** “Two more techniques: Divide and Conquer, and Branch and Bound.”

---

## Slide 9 — Rejected: Divide and Conquer, Branch and Bound  (0:55, script 118 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- DIVIDE AND CONQUER = meet-in-the-middle (Horowitz–Sahni): two halves of 20 → 2²⁰ ≈ 10⁶ sums each, sort, match
- Worst case O(n·2^(n/2)): far better than 2⁴⁰ — it is a strong alternative (we cross-checked it against our solver)
- Not primary because: the COMBINE step (matching every left sum with right sums) is the cost and does not recurse; it always uses 2^(n/2) time AND memory; audit targets are small so pruning keeps the DFS tiny; DFS memory is O(n) and traceable
- BRANCH AND BOUND: needs an objective + incumbent; here the only bounds are feasibility bounds (the same two rules)
- Best-first order needs a priority queue and frontier memory; states are the same, so extra cost for no gain
- Choice: plain depth-first backtracking = simplest, O(n) memory — not because the others cannot solve it

**Suggested visual:** Two-column comparison: “Possible?” yes/yes, “Best fit here?” no/no.

**Say aloud:**

> Divide and conquer is a real option. Meet in the middle splits the forty items into two halves, lists about a million sums for each, sorts them and matches. Its worst case is far better than two to the forty, and we checked it against our solver. We did not choose it because the combine step, matching sums across halves, is the real cost and does not shrink by recursion, it always uses a million-sized lists, and the audit target is small so our pruned search stays tiny. Branch and bound can also solve this problem, but with no objective its bounds are the same feasibility rules, so a priority queue adds memory and bookkeeping without fewer states.

**Likely questions:**

- **Q:** So is Backtracking really the best choice?
  **A:** It is the best fit for this assignment: simplest, O(n) memory, traceable, and fast when the target is small. For an adversarial batch of 40 items, meet-in-the-middle has the better worst-case guarantee, and we say so.
- **Q:** What is the difference between your search and Branch and Bound?
  **A:** B&B compares an optimistic bound with the best value found so far. We have no value to optimise, so we only test whether a branch can still hit the window; that is backtracking with feasibility pruning.

**Transition:** “Now the experiments: the chosen algorithm against brute force.”

---

## Slide 10 — Experiments: Pruned Search vs Brute Force  (1:00, script 124 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- *(figure: `results/timing_plot.png`)*
- n = 8…22 (both), 24…40 (chosen only) · same inputs · seed 2026 · median of repeats · printing outside timing · solution sets compared first: identical in every case
- n = 22: brute force 1,710 ms vs search 7.1 ms on random batches (≈239×); on the hard family 1,700 ms vs 201 ms (≈8.5×)
- Brute force grows ≈ 4.2× per +2 in n (n·2ⁿ). Hard family grows ≈ 3.8× per +2 = C(n,n/2); dashed line = c × states lies on the data ⇒ time ∝ states
- Random family is irregular (n = 20 faster than n = 18): states depend on target vs total, not on n alone

**Suggested visual:** Insert results/timing_plot.png (two panels). Optionally show the n = 22 rows of timing.csv.

**Say aloud:**

> For experiments, we ran both algorithms on identical inputs with a fixed seed, timed only the function call and took medians. The solution lists matched every time. On the left, typical random batches: at twenty-two transactions brute force takes about seventeen hundred milliseconds, the pruned search about seven, roughly two hundred forty times faster. On the right is the hard family, where pruning helps little: about eight and a half times. Brute force grows about four times for every two extra items, which fits n times two to the n. In the hard family the growth matches n choose n over two, and the dashed line, proportional to states, lies on the measurements. The random curve is irregular because states depend on the target.

**Likely questions:**

- **Q:** Why is the random curve not smooth?
  **A:** The state count depends on how large the target is relative to the total and which amounts were picked. With only five inputs per n that variation shows. Time follows states closely.
- **Q:** How do you know timing is not noise?
  **A:** We use medians of repeated runs, the results scale with the expected counts, and the plotted line proportional to measured states overlaps the data. Absolute values depend on the machine; we re-run it on ours.

**Transition:** “Next: the changed requirement, accepting sums within ±₹50.”

---

## Slide 11 — Changed Requirement: ±₹50 Tolerance  (0:50, script 116 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- Units: amounts in thousands → integer rupees. T = 110,000 · τ = 50 (= 0.05 thousand), exact via Fraction, no floats
- New condition: 109,950 ≤ sum ≤ 110,050
- Change: only lo = T − τ and hi = T + τ; same two rules; proof unchanged; solutions may now extend other solutions
- Given instance: all sums are multiples of ₹1,000 ⇒ still the same 2 solutions, still 35 states

| τ (₹) | 0 | 50 | 500 | 5,000 | 50,000 |
|---|---|---|---|---|---|
| solutions | 3 | 61 | 605 | 5,920 | 64,963 |
| states | 24,580 | 24,609 | 24,901 | 27,990 | 72,530 |

- Random n = 22 batch. Hypothetical amounts [15020, 22000, 35000, 39990, 48000, 53030, 61000]: τ = 0 → 0 solutions; τ = 50 → 2 (110,030 and 109,990)
- Complexity: still O(n log n + states + output), worst case Θ(2ⁿ); output grows ≈ in proportion to the window width

**Suggested visual:** The tolerance table; optional number line showing the window around 110,000.

**Say aloud:**

> For the changed requirement we convert everything to integer rupees: the target is one hundred ten thousand, the tolerance is fifty rupees, exactly, with no floating point. A subset is now accepted if its sum is between one hundred nine thousand nine hundred fifty and one hundred ten thousand fifty. Only the two limits change, so the same two pruning rules and the same proof apply. On our instance every sum is a multiple of one thousand, so the answer is unchanged: still two solutions and thirty-five states. On a random batch of twenty-two, the solutions grow roughly in proportion to the tolerance, while the states grow slowly. Worst case is still two to the n.

**Likely questions:**

- **Q:** Why does the answer not change for the given instance?
  **A:** All amounts are multiples of 1,000, so all subset sums are too, and the window 109,950 to 110,050 contains only 110,000.
- **Q:** Is the pruning still safe with tolerance?
  **A:** Yes. The lemmas use hi and lo only as constants, so replacing T by T+τ and T−τ keeps them true.

**Transition:** “Finally, how this relates to published work.”

---

## Slide 12 — Real-World Reference  (0:40, script 95 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- Horowitz & Sahni, “Computing Partitions with Applications to the Knapsack Problem”, J. ACM 21(2):277–292, 1974 — doi:10.1145/321812.321823
- Studies finding ALL combinations of numbers that sum to M; compares the usual algorithms and presents a square-root-factor improvement over dynamic programming (two-list / meet-in-the-middle idea)
- Ours: simple DFS with two bounds, O(n) memory, Θ(2ⁿ) worst case — theirs: 2^(n/2) techniques with more elaborate heuristics (we do not reproduce them)
- Technique origin: Golomb & Baumert, “Backtrack Programming”, J. ACM 12(4):516–524, 1965 — doi:10.1145/321296.321300
- Python itertools.combinations: generic enumerator, used only in our brute-force baseline

**Suggested visual:** Reference list with the DOI links (all checked).

**Say aloud:**

> Our main reference is Horowitz and Sahni, 1974, Journal of the ACM. It studies exactly our task, finding all combinations of numbers that sum to a given value, compares the usual algorithms, and gives a square-root improvement over dynamic programming. That is the meet-in-the-middle idea we discussed. Our implementation is much simpler: a depth-first search with two bounds and linear memory, but exponential in the worst case. The backtracking technique itself goes back to Golomb and Baumert in 1965. Python's itertools combinations is just a generic enumerator, which we use only for the brute-force baseline.

**Likely questions:**

- **Q:** Does this paper use backtracking?
  **A:** Its main contribution is the two-list method. We cite it because it addresses the same all-combinations problem, and we say exactly how ours differs.
- **Q:** Is itertools a Subset Sum solver?
  **A:** No. It enumerates all combinations in a fixed order with no target and no pruning.

**Transition:** “To conclude.”

---

## Slide 13 — Conclusion  (0:40, script 95 words)

**Slide text (paste into PowerPoint / see slides.pdf):**

- Problem: Subset Sum, listing form → Backtracking with two proven-safe cut-offs
- Answer: {22,35,53} and {22,40,48}; 35 of 128 subsets examined
- Rejected with evidence: Greedy (wrong), DP (value-dependent memory), D&C (strong but heavier combine), B&B (no objective)
- Measured: ≈239× faster than brute force on typical batches at n = 22; only ≈8.5× on the hard family — exponential worst case remains
- ±₹50: same technique, two constants change; exact integer arithmetic
- Limitations: worst case Θ(2ⁿ); for adversarial n = 40, meet-in-the-middle is a better guarantee

**Suggested visual:** Summary slide. End on the two solutions.

**Say aloud:**

> To conclude. The task is Subset Sum in listing form, solved by backtracking with two proven-safe cut-offs. On the given data it finds exactly two combinations while examining thirty-five of one hundred twenty-eight subsets. We rejected greedy because it is wrong, and explained honestly why dynamic programming, divide and conquer and branch and bound can work but fit less well. Measurements show a large speed-up on typical batches and a modest one on our hard family, so the worst case stays exponential. The plus or minus fifty rupee change needs only two constants. Thank you.

**Likely questions:**

- **Q:** What would you use for an adversarial 40-transaction batch?
  **A:** Meet-in-the-middle, with about 2^20 work per half, because its worst-case guarantee is much better than 2^40.
- **Q:** What did each member contribute?
  **A:** See the contribution table in the report; it matches our individual commits.

**Transition:** “End of presentation.”

---

# Short cross-question preparation (anyone may be asked any of these)

1. *Why is the greedy approach wrong?* It takes 61 first, but 110 − 61 = 49 is not a subset sum of the rest; it ends with remainder 1 and finds nothing, although two solutions exist.
2. *Can DP list all solutions?* Yes (walk back through the full table), but the table is O(n·T): about 4.1×10¹⁰ cells for n = 40, T ≈ 10⁹ paise.
3. *Is meet-in-the-middle better?* For adversarial n = 40, yes (≈2²⁰ per half). We chose the DFS for O(n) memory, simplicity and the small-target audit setting.
4. *Why do the cut-offs never lose a solution?* Lemmas A and B hold for every later position, since the list is sorted and amounts are positive.
5. *What is the state count on the given instance and what does it mean?* 35 recursive calls = 35 candidate subsets tested out of 128.
6. *Is your hard input a true worst case?* It is a hard no-solution family with exactly C(n, n/2) states; the true worst case is 2ⁿ when everything is a solution.
7. *Why did the ±₹50 change nothing for the given data?* All sums are multiples of ₹1,000.
8. *Where did the numbers come from?* From the programs in `code/`, saved in `results/*.csv`; rerun with `python benchmark.py`.
