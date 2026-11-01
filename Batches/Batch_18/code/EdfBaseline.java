import java.util.Arrays;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Baseline Scheduler: Earliest-Deadline-First (EDF) heuristic.
 *
 * Implements deadline-ordered dispatching for comparison against Greedy+DSU.
 * Evaluates two tie-breaking policies:
 *   1) Natural input order (arrival order)
 *   2) Highest profit first (best possible case for EDF)
 *
 * Author: Abirami P C (Roll No. 24I302, GitHub: abikomberi25)
 */
public class EdfBaseline {

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
     * Executes EDF scheduling on unit-duration jobs.
     *
     * @param deadline          Job deadlines (1-based hour).
     * @param profit            Job profits.
     * @param maxSlots          Available time horizon (slots).
     * @param tieBreakByProfit  If true, ties in deadline are broken by profit descending;
     *                          otherwise by input index.
     * @param verbose           Whether to log step trace.
     * @return Scheduling result.
     */
    public static Result schedule(int[] deadline, int[] profit, int maxSlots,
                                   boolean tieBreakByProfit, boolean verbose) {
        int n = deadline.length;
        Integer[] order = new Integer[n];
        for (int i = 0; i < n; i++) {
            order[i] = i;
        }

        Arrays.sort(order, (a, b) -> {
            if (deadline[a] != deadline[b]) {
                return Integer.compare(deadline[a], deadline[b]);
            }
            if (tieBreakByProfit && profit[a] != profit[b]) {
                return Integer.compare(profit[b], profit[a]); // higher profit first
            }
            return Integer.compare(a, b); // original index order
        });

        int[] slotToJob = new int[maxSlots + 1];
        Arrays.fill(slotToJob, -1);
        int currentSlot = 1;
        long totalProfit = 0;
        int count = 0;

        for (int j : order) {
            boolean onTime = (currentSlot <= maxSlots && currentSlot <= deadline[j]);
            if (onTime) {
                slotToJob[currentSlot] = j;
                totalProfit += profit[j];
                count++;
                if (verbose) {
                    System.out.printf("  Job J%d (d=%d, p=%3d): assigned to slot %d%n",
                            j + 1, deadline[j], profit[j], currentSlot);
                }
                currentSlot++;
            } else {
                if (verbose) {
                    System.out.printf("  Job J%d (d=%d, p=%3d): misses deadline at slot %d (REJECTED)%n",
                            j + 1, deadline[j], profit[j], currentSlot);
                }
            }
        }

        return new Result(totalProfit, count, slotToJob);
    }

    public static void main(String[] args) {
        int[] deadline = {2, 1, 2, 1, 3, 4, 3, 4};
        int[] profit = {100, 19, 27, 25, 15, 60, 40, 30};

        System.out.println("=== Q3 Evaluation: Earliest-Deadline-First (EDF) Baseline ===");

        System.out.println("\nPolicy A: Ties broken by input order (arrival order)");
        Result rA = schedule(deadline, profit, 4, false, true);
        System.out.printf("Result A -> Total Profit: %d, Jobs: %d%n", rA.totalProfit, rA.scheduledCount);

        System.out.println("\nPolicy B: Ties broken by highest profit (best case for EDF)");
        Result rB = schedule(deadline, profit, 4, true, true);
        System.out.printf("Result B -> Total Profit: %d, Jobs: %d%n", rB.totalProfit, rB.scheduledCount);

        System.out.println("\nComparison against MainSolution (Greedy + DSU):");
        System.out.println("  Optimal Profit: 230");
        System.out.printf("  EDF Policy A Deficit: 230 - %d = %d lost%n", rA.totalProfit, 230 - rA.totalProfit);
        System.out.printf("  EDF Policy B Deficit: 230 - %d = %d lost%n", rB.totalProfit, 230 - rB.totalProfit);
    }
}
