# Presentation Script — Batch 16: Best Trading Window

**Presenter:** Sankar S V (sole member) · **Target length:** about 10 minutes (hard limit 12:00) · **Deck:** `slides.pdf` (12 slides)

These are preparation notes for the recording, not a transcript of a recording. The spoken text (in quotes) is about 1,270 words: roughly 9.5 minutes at 135 words per minute, or about 10 minutes with slide changes and pauses. The times in brackets are targets. Rehearse once with a timer.

| Slide | Topic | Target |
|---|---|---|
| 1 | Title and problem | 0:35 |
| 2 | Model, instance, scale | 0:45 |
| 3 | Why Divide and Conquer | 0:45 |
| 4 | Summary and merge equations | 0:55 |
| 5 | Worked trace | 1:25 |
| 6 | Eight-server design | 1:05 |
| 7 | Comparison with Kadane | 0:50 |
| 8 | Range-query data structures | 0:50 |
| 9 | Rejecting the other four techniques | 0:55 |
| 10 | Two-window extension | 0:50 |
| 11 | Implementation and measurements | 0:45 |
| 12 | Conclusion and reference | 0:30 |
| | **Total** | **≈ 10:10** |

---

### Slide 1 — Title [0:35]

"Good morning. I'm Sankar, and this is Batch 16: the best trading window in distributed tick data. A brokerage stores a stock's net price changes on eight servers, each holding a contiguous date range: about 2.4 million minute ticks over 25 years. Analysts want the contiguous window with the largest total gain. I'll show how to find it without moving those 2.4 million numbers to one place."

*Transition:* "First, exactly what we compute."

### Slide 2 — Model [0:45]

"The input is a sequence of signed changes. We choose i ≤ j to maximise the sum from A i to A j. Three decisions matter. First, the window is non-empty: if every day is a loss, we report the least-bad day, not zero. Second, ties go to the earliest start, then the earliest end, so every implementation agrees. Third, I speak in one-based positions. The code is zero-based inside. For the twelve given values, the answer is 14 rupees, on days 3 through 8."

### Slide 3 — Why Divide and Conquer [0:45]

"Cut the array anywhere, and every window is in exactly one place: entirely left, entirely right, or crossing the cut. A crossing window is always a suffix of the left part glued to a prefix of the right part. So if each half reports a few numbers about itself, I can combine the halves in constant time, without looking inside. That's divide, conquer, combine. The same summary later drives the servers and the range-query structures. I'm not claiming it beats Kadane sequentially. The benefit is composability."

### Slide 4 — Summary and merge [0:55]

"The summary has four fields: the total; the best prefix, starting at the left edge; the best suffix, ending at the right edge; and the best window anywhere. A single value x gives x, x, x, x.

To merge L and R:
- totals add;
- the prefix either stays in L, or takes all of L plus R's prefix;
- the suffix is the mirror image;
- the best is the maximum of L's best, R's best, and L's suffix plus R's prefix, which is the crossing window.

That's constant work, so T of n equals 2 T of n over 2 plus a constant, which is linear. The stack is only log n deep because I pass indices, not slices. Four extra indices record *where* each window is."

### Slide 5 — Worked trace [1:25]

"Here's the instance merged bottom-up, exactly as the program printed it. Level one pairs the leaves. For example, days 7 and 8, four and seven, give 11 in every field. Level two: days 1 to 4 give total 4, prefix 6, suffix 6, best 8, which is the 8 on day 3. Days 5 to 8 give 8, 8, 11, 11.

Level three is the key merge. The best is the maximum of 8, 11, and the crossing value 6 plus 8, which is 14. The 6 is the suffix of days 3 and 4. The 8 is the prefix covering all of days 5 to 8. So the winner crosses the boundary: days 3 to 8.

At the root we add days 9 to 12. Its best is only 7, and the crossing candidate is 14 minus 2, which is 12. So 14 survives. Final answer: 14 rupees on days 3 to 8. Check: 8 minus 2 plus 6 minus 9 plus 4 plus 7 is 14. The program, brute force and Kadane all agree."

### Slide 6 — Eight servers [1:05]

"Each server makes one pass over about 300,000 ticks and sends just its summary: eight integers, sixty-four in total instead of 2.4 million. The coordinator merges in three rounds: four merges, then two, then one, so seven constant-time merges. It must keep date order, because the merge is associative but not commutative.

Local work is n over p, and total work is still order n. The merge tree has depth log p, so the ideal parallel time is order n over p plus log p. That assumes balanced blocks, one core each, data already on the servers, and negligible network cost. On my laptop the simulation proves correctness, not speedup, and I claim no cluster timings."

### Slide 7 — Versus Kadane [0:50]

"Question three. Kadane's scan keeps the best window ending at each position. Both methods take linear time. Kadane needs constant space, mine needs log n stack, which is 23 frames at 2.4 million. So for one full scan on one machine, Kadane wins: it's leaner, with smaller constants. Divide and Conquer wins when data is already partitioned, because Kadane's state for block five needs block four, and when many range queries or updates reuse the summary. There's no free eightfold speedup: shipping data or network latency can cost more than the extra servers save."

### Slide 8 — Data structures [0:50]

"Question four: many queries for the best window between day L and day R. A direct scan needs no setup, but each query costs its length. A segment tree stores our summary in every node. It builds in linear time, answers in log n, about 22 levels, and updates a corrected tick in log n with linear memory. That's my recommendation. A disjoint sparse table answers with one merge, but needs n log n build time and memory and has no cheap updates, so it suits only frozen history. The classic overlapping sparse table fails here, because our merge isn't idempotent: overlap would count ticks twice. All three structures are implemented and tested."

### Slide 9 — Other techniques [0:55]

"Why not the others? Greedy: the rule 'never bridge a negative' returns 5 on 5, minus 1, minus 1, minus 1, 5, but the whole array gives 7. That refutes the rule, not every greedy idea. Dynamic programming: Kadane is a correct linear DP, and I use it as my reference. It isn't my primary design because its state depends on everything to the left, so a server or tree node can't hold it on its own. Backtracking explores all n times n plus 1 over 2 windows: 2.88 trillion at full scale. Branch and bound needs a tight, sound bound. With signed data, 'current sum plus all remaining positives' is too optimistic, so it prunes little and stays quadratic in the worst case."

### Slide 10 — Two windows [0:50]

"Question five allows up to two non-overlapping windows. One summary describes only one window, so it isn't enough on its own. I use a prefix–suffix DP. P of i is the best window in the first i days, from a forward Kadane pass. Q of i is the best window from day i on, from a backward pass. The answer is the larger of P of n, which is one window, and P of i plus Q of i plus 1 over every split. Every disjoint pair is counted at the split after its first window. This is linear time and space. Here it picks days 3 to 5 and 7 to 8, for 23 rupees, skipping the minus 9. For k windows, a DP runs in order k n."

### Slide 11 — Evidence [0:45]

"Everything is in standard-library Python, with 24 unit tests, all passing. They include two thousand random arrays against brute force, associativity, both range structures, and the two-window solution against exhaustive pairs. The benchmark uses the same seeded input for both algorithms and checks that the answers match before timing. Doubling n roughly doubles Divide and Conquer and quadruples exhaustive search: linear versus quadratic. At 2.4 million values, my pure-Python version took about 19 seconds. The report discusses that constant factor honestly."

### Slide 12 — Conclusion [0:30]

"To conclude: the answer is 14 rupees on days 3 to 8, or 23 with two windows. An associative constant-time summary merge gives linear work, seven merges across eight servers, and a segment tree for range queries. It's the same shape as MapReduce by Dean and Ghemawat, except our reduce is order-sensitive. Thank you. I'm happy to take questions."
