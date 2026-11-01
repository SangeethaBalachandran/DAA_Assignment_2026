import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Q5 Changed Requirement: Arbitrary Job Durations (1 to 4 hours).
 *
 * Demonstrates:
 *   1) Suboptimality of Greedy when durations vary:
 *      3-job counterexample where greedy heuristic yields 10, while exact optimum is 12.
 *   2) Exact Dynamic Programming formulation (Lawler-Moore pseudo-polynomial algorithm):
 *      Jobs sorted by deadline (EDD). State f[t] = max profit for total duration t.
 *      Time Complexity: O(nD), Space Complexity: O(D).
 *   3) Empirical cost measurement on n = 100,000 jobs, D = 10,000 hours,
 *      demonstrating that O(nD) exceeds the strict 2-second target for n = 10^6.
 *
 * Author: Vinothini (Roll No. 24I374)
 */
public class ChangedRequirement {

    /**
     * Exact pseudo-polynomial dynamic program for variable-duration jobs.
     *
     * @param duration Array of job execution lengths.
     * @param deadline Array of job deadlines.
     * @param profit   Array of job profits.
     * @param horizon  Total available hours in scheduling window (D).
     * @return Maximum achievable profit.
     */
    public static long solveExactDP(int[] duration, int[] deadline, int[] profit, int horizon) {
        int n = duration.length;
        Integer[] order = new Integer[n];
        for (int i = 0; i < n; i++) {
            order[i] = i;
        }

        // Sort by earliest deadline first (EDD rule)
        Arrays.sort(order, Comparator.comparingInt(i -> deadline[i]));

        long NEG_INF = Long.MIN_VALUE / 4;
        long[] f = new long[horizon + 1];
        Arrays.fill(f, NEG_INF);
        f[0] = 0;

        for (int idx : order) {
            int p = duration[idx];
            int w = profit[idx];
            int lastStart = Math.min(deadline[idx], horizon) - p;

            // Iterate downwards so each job is considered at most once
            for (int t = lastStart; t >= 0; t--) {
                if (f[t] > NEG_INF && f[t] + w > f[t + p]) {
                    f[t + p] = f[t] + w;
                }
            }
        }

        long bestProfit = 0;
        for (int t = 0; t <= horizon; t++) {
            if (f[t] > bestProfit) {
                bestProfit = f[t];
            }
        }
        return bestProfit;
    }

    /**
     * Heuristic extension of unit-time greedy: sorts by profit descending,
     * places each job in the latest contiguous free interval fitting before its deadline.
     */
    public static long solveGreedyBlockHeuristic(int[] duration, int[] deadline,
                                                 int[] profit, int horizon) {
        int n = duration.length;
        Integer[] order = new Integer[n];
        for (int i = 0; i < n; i++) {
            order[i] = i;
        }
        // Profit descending
        Arrays.sort(order, (a, b) -> Integer.compare(profit[b], profit[a]));

        boolean[] busy = new boolean[horizon + 2];
        long totalProfit = 0;

        for (int j : order) {
            int p = duration[j];
            int latestEnd = Math.min(deadline[j], horizon);

            // Find latest available contiguous block of length p
            for (int start = latestEnd - p + 1; start >= 1; start--) {
                boolean blockFree = true;
                for (int h = start; h < start + p; h++) {
                    if (busy[h]) {
                        blockFree = false;
                        break;
                    }
                }
                if (blockFree) {
                    for (int h = start; h < start + p; h++) {
                        busy[h] = true;
                    }
                    totalProfit += profit[j];
                    break;
                }
            }
        }
        return totalProfit;
    }

    public static void main(String[] args) {
        System.out.println("=== Q5 Analysis: Variable Job Durations (1 to 4 Hours) ===");

        // 3-job counterexample in a 3-hour window
        // Job A: (duration 3h, deadline 3, profit 10)
        // Job B: (duration 1h, deadline 1, profit 6)
        // Job C: (duration 2h, deadline 3, profit 6)
        int[] dur = {3, 1, 2};
        int[] dl  = {3, 1, 3};
        int[] pr  = {10, 6, 6};
        int horizon = 3;

        long greedyResult = solveGreedyBlockHeuristic(dur, dl, pr, horizon);
        long dpResult     = solveExactDP(dur, dl, pr, horizon);

        System.out.println("\n--- Counterexample on 3 Jobs (Horizon D = 3 hours) ---");
        System.out.println("Job A: 3h, d=3, p=10");
        System.out.println("Job B: 1h, d=1, p=6");
        System.out.println("Job C: 2h, d=3, p=6");
        System.out.printf("  Greedy Block Heuristic Profit: %d (Selects A, filling hours 1-3)%n", greedyResult);
        System.out.printf("  Exact DP Optimum Profit      : %d (Selects B in hour 1, C in hours 2-3)%n", dpResult);
        System.out.println("Conclusion: Greedy choice property is violated; matroid structure collapses.\n");

        // Empirical performance measurement of DP on large n
        int testN = 100_000;
        int testD = 10_000;
        System.out.printf("--- Dynamic Programming Scalability Test (n=%d, D=%d) ---%n", testN, testD);

        Random rnd = new Random(42);
        int[] testDur = new int[testN];
        int[] testDl  = new int[testN];
        int[] testPr  = new int[testN];
        for (int i = 0; i < testN; i++) {
            testDur[i] = 1 + rnd.nextInt(4);
            testDl[i]  = 1 + rnd.nextInt(testD);
            testPr[i]  = 1 + rnd.nextInt(1000);
        }

        // Warm-up run
        solveExactDP(testDur, testDl, testPr, testD);

        long t0 = System.nanoTime();
        long opt = solveExactDP(testDur, testDl, testPr, testD);
        double elapsedMs = (System.nanoTime() - t0) / 1e6;

        System.out.printf("  Measured DP runtime at n=100,000, D=10,000: %.1f ms (Profit=%d)%n", elapsedMs, opt);
        System.out.printf("  Extrapolated runtime at n=1,000,000      : ~%.2f seconds%n", (elapsedMs * 10.0) / 1000.0);
        System.out.println("Note: Because n*D = 10^10 updates, sequential DP exceeds the 2.0 s limit.");
    }
}
