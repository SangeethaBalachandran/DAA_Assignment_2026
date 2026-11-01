import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Locale;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Q4 Empirical Benchmark: Running time of four slot-finding data structures
 * on 1,000,000 jobs and 10,000 slots across three workloads.
 *
 * Writes results to results/q4_slot_finder_timing.csv.
 *
 * Author: Dhekshika D (Roll No. 24I314)
 */
public class Q4Benchmark {

    static long sink; // Prevents compiler dead-code elimination

    interface TimedTask {
        long run();
    }

    static double timeMs(TimedTask task, int repetitions) {
        double[] ms = new double[repetitions];
        for (int r = 0; r < repetitions; r++) {
            long t0 = System.nanoTime();
            sink += task.run();
            ms[r] = (System.nanoTime() - t0) / 1e6;
        }
        Arrays.sort(ms);
        return ms[ms.length / 2]; // return median
    }

    public static void runBenchmark(String outputDir) throws Exception {
        final int n = 1_000_000;
        final int D = 10_000;
        String[] workloads = {"random", "same_deadline", "chain"};

        File outFolder = new File(outputDir);
        outFolder.mkdirs();
        File csvFile = new File(outFolder, "q4_slot_finder_timing.csv");

        System.out.printf("Starting Q4 Benchmark (n=%d, D=%d)...%n", n, D);

        try (PrintWriter csv = new PrintWriter(new FileWriter(csvFile))) {
            csv.println("structure,workload,n,slots,sort_ms,find_phase_ms,total_ms,total_profit,operations");

            for (String wl : workloads) {
                System.out.printf("%n=== Workload: %s ===%n", wl);
                int[][] input = GenerateInputs.generate(wl, n, D, 7);
                final int[] dl = input[0];
                final int[] pr = input[1];

                // 1) Measure sort time (common to all methods)
                long[][] keysBox = new long[1][];
                double sortMs = timeMs(() -> {
                    long[] keys = new long[n];
                    for (int i = 0; i < n; i++) {
                        keys[i] = ((long) (Integer.MAX_VALUE - pr[i]) << 32) | (long) i;
                    }
                    Arrays.sort(keys);
                    keysBox[0] = keys;
                    return keys[0];
                }, 5);

                int[] sd = new int[n];
                int[] sp = new int[n];
                for (int k = 0; k < n; k++) {
                    int j = (int) keysBox[0][k];
                    sd[k] = dl[j];
                    sp[k] = pr[j];
                }

                String[] structures = {
                    "linear_scan",
                    "tree_set_bst",
                    "segment_tree",
                    "dsu_path_compression"
                };

                long expectedProfit = -1;

                for (String name : structures) {
                    // Warm-up JIT with prefix
                    int wn = 20_000;
                    int[] wd = Arrays.copyOf(sd, wn);
                    int[] wp = Arrays.copyOf(sp, wn);
                    for (int w = 0; w < 3; w++) {
                        switch (name) {
                            case "linear_scan": sink += SlotFinders.linearScan(wd, wp, D)[0]; break;
                            case "tree_set_bst": sink += SlotFinders.treeSet(wd, wp, D)[0]; break;
                            case "segment_tree": sink += SlotFinders.segmentTree(wd, wp, D)[0]; break;
                            default: sink += SlotFinders.dsu(wd, wp, D, false)[0]; break;
                        }
                    }

                    final long[][] box = new long[1][];
                    int reps = name.equals("linear_scan") ? 1 : 5;

                    double findMs = timeMs(() -> {
                        switch (name) {
                            case "linear_scan":
                                box[0] = SlotFinders.linearScan(sd, sp, D);
                                break;
                            case "tree_set_bst":
                                box[0] = SlotFinders.treeSet(sd, sp, D);
                                break;
                            case "segment_tree":
                                box[0] = SlotFinders.segmentTree(sd, sp, D);
                                break;
                            default:
                                box[0] = SlotFinders.dsu(sd, sp, D, false);
                                break;
                        }
                        return box[0][0];
                    }, reps);

                    long ops = box[0][1];
                    if (name.startsWith("dsu")) {
                        // Separate hop count run
                        ops = SlotFinders.dsu(sd, sp, D, true)[1];
                    }

                    if (expectedProfit < 0) {
                        expectedProfit = box[0][0];
                    } else if (expectedProfit != box[0][0]) {
                        throw new IllegalStateException("Profit mismatch in " + name + " on " + wl);
                    }

                    String opsStr = (ops == 0) ? "" : Long.toString(ops);
                    csv.printf(Locale.ROOT, "%s,%s,%d,%d,%.3f,%.3f,%.3f,%d,%s%n",
                            name, wl, n, D, sortMs, findMs, sortMs + findMs, box[0][0], opsStr);

                    System.out.printf(Locale.ROOT, "  %-22s sort: %7.1f ms | find: %10.1f ms | profit: %d | ops: %s%n",
                            name, sortMs, findMs, box[0][0], (ops == 0 ? "-" : Long.toString(ops)));
                }
            }
        }
        System.out.println("Q4 Benchmark complete. Results written to: " + csvFile.getAbsolutePath());
    }

    public static void main(String[] args) throws Exception {
        String dir = (args.length > 0) ? args[0] : "results";
        runBenchmark(dir);
    }
}
