import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Locale;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Empirical Timing Benchmark Suite.
 *
 * Compares chosen algorithm (MainSolution: Greedy+DSU) against the rejected
 * alternative (RejectedAlternative: Search with feasibility pruning).
 *
 * Benchmarking Protocol:
 *   - JIT compiler warm-up prior to measurement loops.
 *   - Small sizes: n in {10, 15, 20, 25, 30} on random and same_deadline.
 *     Verifies that both algorithms yield identical maximum profit.
 *   - Large scale: n in {1,000, 10,000, 100,000, 500,000, 1,000,000} with D = 10,000
 *     on all three workloads for MainSolution.
 *   - Computes robust statistics: median, minimum, and maximum runtime over repetitions.
 *   - Writes results/timing.csv.
 *
 * Author: Sowmya P Nagarajan (Roll No. 24I358)
 */
public class Benchmark {

    static final int[] SMALL_SIZES = {10, 15, 20, 25, 30};
    static final int[] LARGE_SIZES = {1_000, 10_000, 100_000, 500_000, 1_000_000};
    static final String[] ALL_WORKLOADS = {"random", "same_deadline", "chain"};

    static long sink; // Prevents JVM dead-code optimization

    interface TimedExecution {
        long execute();
    }

    static double[] measure(TimedExecution task, int repetitions) {
        double[] runtimes = new double[repetitions];
        for (int r = 0; r < repetitions; r++) {
            long t0 = System.nanoTime();
            sink += task.execute();
            runtimes[r] = (System.nanoTime() - t0) / 1e6; // Convert to milliseconds
        }
        Arrays.sort(runtimes);
        double median = runtimes[runtimes.length / 2];
        double min = runtimes[0];
        double max = runtimes[runtimes.length - 1];
        return new double[]{median, min, max};
    }

    public static void runTimingSuite(PrintWriter csv) {
        csv.println("algorithm,workload,n,slots,reps,median_ms,min_ms,max_ms,total_profit,search_nodes");

        System.out.println("Starting JIT Warm-up phase...");
        for (int i = 0; i < 5; i++) {
            int[][] w = GenerateInputs.generate("random", 100_000, GenerateInputs.LARGE_D, 1);
            sink += MainSolution.solve(w[0], w[1], GenerateInputs.LARGE_D).totalProfit;
        }
        for (int i = 0; i < 5; i++) {
            int[][] w = GenerateInputs.generate("random", 20, 10, 1);
            sink += RejectedAlternative.solve(w[0], w[1], 10).totalProfit;
        }
        System.out.println("Warm-up complete.\n");

        int[] allSizes = new int[SMALL_SIZES.length + LARGE_SIZES.length];
        System.arraycopy(SMALL_SIZES, 0, allSizes, 0, SMALL_SIZES.length);
        System.arraycopy(LARGE_SIZES, 0, allSizes, SMALL_SIZES.length, LARGE_SIZES.length);

        // 1) Evaluate MainSolution across all sizes and workloads
        System.out.println("=== Evaluating MainSolution (Greedy + DSU) ===");
        for (String wl : ALL_WORKLOADS) {
            for (int n : allSizes) {
                int D = GenerateInputs.slotsFor(wl, n);
                int[][] input = GenerateInputs.generate(wl, n, D, 42 + n);
                int reps = (n >= 500_000) ? 5 : 9;

                final int[] dl = input[0];
                final int[] pr = input[1];
                final int slots = D;
                long[] profitBox = new long[1];

                double[] stats = measure(() -> {
                    MainSolution.Result res = MainSolution.solve(dl, pr, slots);
                    profitBox[0] = res.totalProfit;
                    return res.totalProfit;
                }, reps);

                csv.printf(Locale.ROOT, "greedy_dsu,%s,%d,%d,%d,%.6f,%.6f,%.6f,%d,0%n",
                        wl, n, D, reps, stats[0], stats[1], stats[2], profitBox[0]);

                System.out.printf(Locale.ROOT, "  greedy_dsu   %-13s n=%-8d D=%-6d -> %10.3f ms | profit=%d%n",
                        wl, n, D, stats[0], profitBox[0]);
            }
        }

        // 2) Evaluate RejectedAlternative on small sizes
        System.out.println("\n=== Evaluating RejectedAlternative (Search + Pruning) ===");
        for (String wl : new String[]{"random", "same_deadline"}) {
            for (int n : SMALL_SIZES) {
                int D = GenerateInputs.slotsFor(wl, n);
                int[][] input = GenerateInputs.generate(wl, n, D, 42 + n);
                final int[] dl = input[0];
                final int[] pr = input[1];
                final int slots = D;

                long greedyProfit = MainSolution.solve(dl, pr, slots).totalProfit;

                // Calibrate repetitions based on trial run
                long t0 = System.nanoTime();
                RejectedAlternative.Result firstRes = RejectedAlternative.solve(dl, pr, slots);
                double trialMs = (System.nanoTime() - t0) / 1e6;

                int reps = (trialMs < 100) ? 9 : (trialMs < 1500 ? 3 : 1);
                RejectedAlternative.Result[] box = new RejectedAlternative.Result[1];

                double[] stats = measure(() -> {
                    box[0] = RejectedAlternative.solve(dl, pr, slots);
                    return box[0].totalProfit;
                }, reps);

                RejectedAlternative.Result res = box[0];

                if (res.totalProfit != greedyProfit) {
                    throw new IllegalStateException(String.format(
                            "MISMATCH! Greedy=%d, Search=%d for wl=%s, n=%d",
                            greedyProfit, res.totalProfit, wl, n));
                }

                csv.printf(Locale.ROOT, "backtracking,%s,%d,%d,%d,%.6f,%.6f,%.6f,%d,%d%n",
                        wl, n, D, reps, stats[0], stats[1], stats[2], res.totalProfit, res.nodesVisited);

                System.out.printf(Locale.ROOT, "  backtracking %-13s n=%-8d D=%-6d -> %10.3f ms | profit=%d | nodes=%d%n",
                        wl, n, D, stats[0], res.totalProfit, res.nodesVisited);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        String dir = (args.length > 0) ? args[0] : "results";
        File outDir = new File(dir);
        outDir.mkdirs();

        File timingCsv = new File(outDir, "timing.csv");
        System.out.printf("Starting empirical benchmark. Writing to %s%n", timingCsv.getAbsolutePath());

        try (PrintWriter csv = new PrintWriter(new FileWriter(timingCsv))) {
            runTimingSuite(csv);
        }

        System.out.println("\nEmpirical benchmark completed successfully.");
    }
}
