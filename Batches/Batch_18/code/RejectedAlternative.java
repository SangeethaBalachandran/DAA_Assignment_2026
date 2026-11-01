/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Rejected Alternative: Recursive Include/Exclude Search with Feasibility Pruning.
 *
 * For each job, we explore two decisions:
 *   1) Include: admitted only if Hall's feasibility condition is preserved.
 *   2) Exclude: skip the job and proceed to next.
 *
 * Feasibility test: for all horizons t in [d_i, D], count of admitted jobs <= t.
 * Pruning is strictly feasibility-based (no upper-bound profit pruning),
 * making this an exact search with worst-case O(2^n * D) complexity.
 *
 * Author: Bharaghave Shi C G (Roll No. 24I308)
 */
public class RejectedAlternative {

    private final int[] deadline;
    private final int[] profit;
    private final int D;
    private final int[] cnt; // cnt[t] = count of selected jobs with deadline <= t
    private long bestProfit;
    private long nodesVisited;

    private RejectedAlternative(int[] deadline, int[] profit, int maxSlots) {
        this.deadline = deadline;
        this.profit = profit;
        int maxD = 0;
        for (int d : deadline) {
            if (d > maxD) maxD = d;
        }
        this.D = Math.min(maxSlots, maxD);
        this.cnt = new int[this.D + 2];
        this.bestProfit = 0;
        this.nodesVisited = 0;
    }

    public static final class Result {
        public final long totalProfit;
        public final long nodesVisited;

        public Result(long totalProfit, long nodesVisited) {
            this.totalProfit = totalProfit;
            this.nodesVisited = nodesVisited;
        }
    }

    /**
     * Solves the scheduling problem via exhaustive pruned search.
     */
    public static Result solve(int[] deadline, int[] profit, int maxSlots) {
        RejectedAlternative searcher = new RejectedAlternative(deadline, profit, maxSlots);
        searcher.search(0, 0L);
        return new Result(searcher.bestProfit, searcher.nodesVisited);
    }

    private void search(int i, long currentProfit) {
        nodesVisited++;
        if (i == deadline.length) {
            if (currentProfit > bestProfit) {
                bestProfit = currentProfit;
            }
            return;
        }

        int d = Math.min(deadline[i], D);

        // Branch 1: Include job i if feasibility condition holds for all t in [d, D]
        boolean feasible = true;
        for (int t = d; t <= D; t++) {
            cnt[t]++;
            if (cnt[t] > t) {
                feasible = false;
            }
        }

        if (feasible) {
            search(i + 1, currentProfit + profit[i]);
        }

        // Backtrack counter state
        for (int t = d; t <= D; t++) {
            cnt[t]--;
        }

        // Branch 2: Exclude job i
        search(i + 1, currentProfit);
    }

    public static void main(String[] args) {
        int[] deadline = {2, 1, 2, 1, 3, 4, 3, 4};
        int[] profit = {100, 19, 27, 25, 15, 60, 40, 30};

        System.out.println("=== Pruned Search on 8-Job Instance ===");
        Result res = solve(deadline, profit, 4);
        System.out.printf("Optimal Profit : %d%n", res.totalProfit);
        System.out.printf("Nodes Visited  : %d%n", res.nodesVisited);
    }
}
