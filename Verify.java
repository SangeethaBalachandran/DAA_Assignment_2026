import java.util.Random;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Correctness Verification Harness.
 *
 * Validates algorithmic correctness by testing three independent solvers on
 * 1,000 randomly generated problem instances (n <= 12):
 *   1) MainSolution (Greedy + DSU)
 *   2) RejectedAlternative (Feasibility-pruned search)
 *   3) Exhaustive Brute-Force subset enumerator (O(2^n))
 *
 * Also checks structural schedule validity:
 *   - Distinct slot assignments within [1, D]
 *   - Deadline compliance: slot(j) <= deadline[j]
 *   - Accurate profit summation
 *
 * Author: Bharaghave Shi C G (Roll No. 24I308)
 */
public class Verify {

    /**
     * Exact brute-force solver: iterates over all 2^n subsets and finds the
     * maximum profit subset satisfying Hall's feasibility condition.
     */
    public static long solveBruteForce(int[] deadline, int[] profit, int maxSlots) {
        int n = deadline.length;
        int maxD = 0;
        for (int d : deadline) {
            if (d > maxD) maxD = d;
        }
        int D = Math.min(maxSlots, maxD);

        long maxProfit = 0;
        int totalSubsets = 1 << n;

        for (int mask = 0; mask < totalSubsets; mask++) {
            // Count jobs with deadline <= t for t in 1..D
            int[] cnt = new int[D + 1];
            long currentProfit = 0;
            boolean feasible = true;

            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) {
                    currentProfit += profit[i];
                    int d = Math.min(deadline[i], D);
                    cnt[d]++;
                }
            }

            // Cumulative count check (Hall's condition)
            int runningSum = 0;
            for (int t = 1; t <= D; t++) {
                runningSum += cnt[t];
                if (runningSum > t) {
                    feasible = false;
                    break;
                }
            }

            if (feasible && currentProfit > maxProfit) {
                maxProfit = currentProfit;
            }
        }

        return maxProfit;
    }

    /**
     * Validates that the schedule returned by MainSolution is structurally sound.
     */
    public static boolean isValidSchedule(int[] deadline, int[] profit,
                                           MainSolution.Result r, int maxSlots) {
        if (r.slotToJob == null || r.slotToJob.length < 1) {
            return false;
        }

        boolean[] used = new boolean[deadline.length];
        long sumProfit = 0;
        int count = 0;

        for (int s = 1; s < r.slotToJob.length; s++) {
            int j = r.slotToJob[s];
            if (j >= 0) {
                // Bounds check
                if (j >= deadline.length || used[j]) {
                    return false; // Duplicate job assignment
                }
                used[j] = true;

                // Slot and Deadline check
                if (s > maxSlots || s > deadline[j]) {
                    return false; // Job scheduled past window or past deadline
                }

                sumProfit += profit[j];
                count++;
            }
        }

        return (sumProfit == r.totalProfit && count == r.scheduledCount);
    }

    public static void main(String[] args) {
        int testCount = 1000;
        Random rnd = new Random(2026);
        System.out.printf("Running %d correctness verification tests...%n", testCount);

        long startTime = System.currentTimeMillis();

        for (int test = 1; test <= testCount; test++) {
            int n = 1 + rnd.nextInt(12); // n in [1, 12]
            int D = 1 + rnd.nextInt(12); // D in [1, 12]

            int[] deadline = new int[n];
            int[] profit = new int[n];
            for (int i = 0; i < n; i++) {
                deadline[i] = 1 + rnd.nextInt(D);
                profit[i] = 1 + rnd.nextInt(500);
            }

            // Execute all three solvers
            MainSolution.Result rMain = MainSolution.solve(deadline, profit, D);
            RejectedAlternative.Result rAlt = RejectedAlternative.solve(deadline, profit, D);
            long bfOptimum = solveBruteForce(deadline, profit, D);

            // 1) Verify structural validity of MainSolution schedule
            if (!isValidSchedule(deadline, profit, rMain, D)) {
                throw new AssertionError(String.format(
                        "Test %d FAILED: MainSolution produced an invalid schedule! n=%d, D=%d",
                        test, n, D));
            }

            // 2) Verify profit equality across chosen, rejected, and brute-force
            if (rMain.totalProfit != bfOptimum) {
                throw new AssertionError(String.format(
                        "Test %d FAILED: MainSolution profit (%d) != BruteForce (%d)! n=%d, D=%d",
                        test, rMain.totalProfit, bfOptimum, n, D));
            }
            if (rAlt.totalProfit != bfOptimum) {
                throw new AssertionError(String.format(
                        "Test %d FAILED: RejectedAlternative profit (%d) != BruteForce (%d)! n=%d, D=%d",
                        test, rAlt.totalProfit, bfOptimum, n, D));
            }

            if (test % 200 == 0) {
                System.out.printf("  Verified %4d / %d tests successfully.%n", test, testCount);
            }
        }

        long elapsed = System.currentTimeMillis() - startTime;
        System.out.printf("ALL %d VERIFICATION TESTS PASSED in %d ms.%n", testCount, elapsed);
        System.out.println("Solvers verified: MainSolution == RejectedAlternative == BruteForce.");
    }
}
