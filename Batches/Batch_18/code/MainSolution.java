import java.util.Arrays;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Chosen Algorithm: Maximum-profit unit-job scheduling with deadlines.
 *
 * Technique : Greedy by descending profit.
 * Data Structure : Disjoint Set Union (DSU) over slots 0..D with path compression.
 *                  find(x) returns the latest free slot <= x (0 means none available).
 *
 * Time Complexity : O(n log n) sorting + O((n + D) * alpha(D)) DSU operations = O(n log n).
 * Space Complexity: O(n + D) for job keys, parent array, and schedule mapping.
 *
 * Author: Abirami P C (Roll No. 24I302, GitHub: abikomberi25)
 */
public class MainSolution {

    /**
     * Scheduling result holding total profit, count of scheduled jobs,
     * and the slot assignment array (slot 1..D -> 0-based job index).
     */
    public static final class Result {
        public final long totalProfit;
        public final int scheduledCount;
        public final int[] slotToJob;

        public Result(long totalProfit, int scheduledCount, int[] slotToJob) {
            this.totalProfit = totalProfit;
            this.scheduledCount = scheduledCount;
            this.slotToJob = slotToJob;
        }
    }

    /**
     * Iterative find with full two-pass path compression.
     * Prevents call-stack overflow on deep tree chains.
     *
     * @param parent DSU parent array where parent[s] == s indicates slot s is free.
     * @param x      Target slot query.
     * @return The representative root representing the latest free slot <= x.
     */
    public static int find(int[] parent, int x) {
        int root = x;
        while (parent[root] != root) {
            root = parent[root];
        }
        int curr = x;
        while (parent[curr] != root) {
            int next = parent[curr];
            parent[curr] = root;
            curr = next;
        }
        return root;
    }

    /**
     * Schedules unit-time jobs to maximize total profit without verbose logging.
     */
    public static Result solve(int[] deadline, int[] profit, int maxSlots) {
        return solve(deadline, profit, maxSlots, false);
    }

    /**
     * Solves the scheduling problem with optional verbose trace.
     *
     * @param deadline Array of job deadlines (1-based hour, >= 1).
     * @param profit   Array of job profits (>= 0).
     * @param maxSlots Capacity of the scheduling window in slots/hours.
     * @param verbose  Whether to print step-by-step trace and parent array state.
     * @return Scheduling result.
     */
    public static Result solve(int[] deadline, int[] profit, int maxSlots, boolean verbose) {
        int n = deadline.length;
        int maxD = 0;
        for (int d : deadline) {
            if (d > maxD) maxD = d;
        }
        int D = Math.min(maxSlots, maxD);

        // 1) Sort jobs descending by profit; break ties by smaller job index.
        // Pack (profit, index) into 64-bit primitive long to avoid object allocation.
        long[] keys = new long[n];
        for (int i = 0; i < n; i++) {
            keys[i] = ((long) (Integer.MAX_VALUE - profit[i]) << 32) | (long) i;
        }
        Arrays.sort(keys);

        // 2) Initialize DSU over slots 0..D. Slot 0 is the sentinel for "no slot free".
        int[] parent = new int[D + 1];
        for (int s = 0; s <= D; s++) {
            parent[s] = s;
        }

        int[] slotToJob = new int[maxSlots + 1];
        Arrays.fill(slotToJob, -1);
        long totalProfit = 0;
        int scheduledCount = 0;

        if (verbose) {
            System.out.println("Initial DSU parent array: " + Arrays.toString(parent));
        }

        for (int k = 0; k < n; k++) {
            int j = (int) keys[k]; // Extract original job index
            int d = Math.min(deadline[j], D);
            int slot = find(parent, d);

            if (slot > 0) {
                slotToJob[slot] = j;
                totalProfit += profit[j];
                scheduledCount++;
                // Point slot to the latest free slot before it
                parent[slot] = find(parent, slot - 1);
            }

            if (verbose) {
                String action = slot > 0 ? ("slot " + slot) : "REJECT";
                System.out.printf("Step %d | Job J%d (d=%d, p=%3d): find(%d) -> %-7s | parent = %s%n",
                        k + 1, j + 1, deadline[j], profit[j], d, action, Arrays.toString(parent));
            }
        }

        return new Result(totalProfit, scheduledCount, slotToJob);
    }

    public static void main(String[] args) {
        // Given instance from Batch 18 scenario: J1..J8
        int[] deadline = {2, 1, 2, 1, 3, 4, 3, 4};
        int[] profit = {100, 19, 27, 25, 15, 60, 40, 30};

        System.out.println("=== Q1 Trace: Greedy + DSU on 8-Job Instance ===");
        Result r = solve(deadline, profit, 4, true);

        System.out.println("\n=== Final Schedule ===");
        for (int s = 1; s < r.slotToJob.length; s++) {
            int j = r.slotToJob[s];
            String desc = (j < 0) ? "empty" : ("J" + (j + 1) + " (profit " + profit[j] + ")");
            System.out.printf("  Slot %d (Hour %d-%d): %s%n", s, s - 1, s, desc);
        }
        System.out.printf("Total Profit: %d (thousand INR), Jobs Scheduled: %d / 4%n",
                r.totalProfit, r.scheduledCount);
    }
}
