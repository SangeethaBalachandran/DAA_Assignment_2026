import java.util.Random;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Workload and Input Generation Suite.
 *
 * Provides synthetic inputs under three evaluation profiles:
 *   1) "random"        : Deadlines uniform in 1..D, profits uniform in 1..1000.
 *                        Simulates standard stochastic cloud batch submissions.
 *   2) "same_deadline" : All deadlines set to D.
 *                        Maximum contention for the final slot; every subset is
 *                        feasible when D = n, triggering worst-case search trees.
 *   3) "chain"         : The first D jobs have deadlines D, D-1, ..., 1 with strictly
 *                        descending profits; subsequent jobs have deadline D.
 *                        Forces an initial DSU path of length D before path compression.
 *
 * Reproducibility: Seed initialized to 42 + n.
 *
 * Author: Sowmya P Nagarajan (Roll No. 24I358)
 */
public class GenerateInputs {

    public static final int LARGE_D = 10_000;

    /**
     * Determines the slot capacity D according to workload and size n.
     *
     * @param workload Name of the workload.
     * @param n        Number of jobs.
     * @return Slot bound D.
     */
    public static int slotsFor(String workload, int n) {
        if (n >= 1_000) {
            return LARGE_D;
        }
        // Small sizes for exact search comparison
        if ("random".equalsIgnoreCase(workload)) {
            return Math.max(1, n / 2);
        }
        return n; // "same_deadline" and "chain" small benchmarks use D = n
    }

    /**
     * Generates parallel arrays of deadlines and profits.
     *
     * @param workload Workload identifier ("random", "same_deadline", "chain").
     * @param n        Number of jobs to generate.
     * @param D        Slot capacity horizon.
     * @param seed     Pseudorandom number generator seed.
     * @return 2D array: res[0] = deadline[], res[1] = profit[].
     */
    public static int[][] generate(String workload, int n, int D, long seed) {
        Random rnd = new Random(seed);
        int[] deadline = new int[n];
        int[] profit = new int[n];

        switch (workload.toLowerCase()) {
            case "random":
                for (int i = 0; i < n; i++) {
                    deadline[i] = 1 + rnd.nextInt(D);
                    profit[i] = 1 + rnd.nextInt(1000);
                }
                break;

            case "same_deadline":
                for (int i = 0; i < n; i++) {
                    deadline[i] = D;
                    profit[i] = 1 + rnd.nextInt(1000);
                }
                break;

            case "chain":
                for (int i = 0; i < n; i++) {
                    deadline[i] = (i < D) ? (D - i) : D;
                    profit[i] = n - i; // Strictly descending profit guarantees order
                }
                break;

            default:
                throw new IllegalArgumentException("Unknown workload type: " + workload);
        }

        return new int[][]{deadline, profit};
    }

    public static void main(String[] args) {
        System.out.println("=== Workload Generation Verification ===");
        for (String wl : new String[]{"random", "same_deadline", "chain"}) {
            int n = 10;
            int D = slotsFor(wl, n);
            int[][] sample = generate(wl, n, D, 42 + n);
            System.out.printf("Workload '%-13s' (n=%d, D=%d):%n", wl, n, D);
            System.out.print("  Deadlines: ");
            for (int d : sample[0]) System.out.print(d + " ");
            System.out.println();
            System.out.print("  Profits  : ");
            for (int p : sample[1]) System.out.print(p + " ");
            System.out.println("\n");
        }
    }
}
