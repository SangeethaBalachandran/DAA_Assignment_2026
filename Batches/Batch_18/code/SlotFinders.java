import java.util.TreeSet;

/**
 * Batch 18 - Cloud Computing: Nightly Batch Jobs with Deadlines.
 * Q4 Analysis: Data structures for finding the latest free slot <= deadline.
 *
 * Implements and compares four candidate structures:
 *   1) Linear Scan : backward probe from deadline down to 1. Cost O(D) per job.
 *   2) Balanced BST: java.util.TreeSet using floor(d) and remove(s). Cost O(log D).
 *   3) Segment Tree: binary range tree storing free slot counts. Cost O(log D).
 *   4) DSU + Path Compression: union-find on interval chain. Cost O(alpha(D)).
 *
 * Author: Dhekshika D (Roll No. 24I314)
 */
public class SlotFinders {

    /**
     * Structure 1: Linear Scan backwards from min(deadline, D).
     *
     * @return long array where [0] = total profit, [1] = probe count.
     */
    public static long[] linearScan(int[] sortedDeadline, int[] sortedProfit, int D) {
        boolean[] used = new boolean[D + 1];
        long profit = 0;
        long probes = 0;

        for (int k = 0; k < sortedDeadline.length; k++) {
            int d = Math.min(sortedDeadline[k], D);
            int s = d;
            while (s > 0 && used[s]) {
                s--;
            }
            probes += (d - s) + (s > 0 ? 1 : 0);
            if (s > 0) {
                used[s] = true;
                profit += sortedProfit[k];
            }
        }
        return new long[]{profit, probes};
    }

    /**
     * Structure 2: Balanced Binary Search Tree (TreeSet).
     *
     * @return long array where [0] = total profit, [1] = 0 (probes not counted).
     */
    public static long[] treeSet(int[] sortedDeadline, int[] sortedProfit, int D) {
        TreeSet<Integer> freeSlots = new TreeSet<>();
        for (int s = 1; s <= D; s++) {
            freeSlots.add(s);
        }
        long profit = 0;

        for (int k = 0; k < sortedDeadline.length; k++) {
            int d = Math.min(sortedDeadline[k], D);
            Integer slot = freeSlots.floor(d);
            if (slot != null) {
                freeSlots.remove(slot);
                profit += sortedProfit[k];
            }
        }
        return new long[]{profit, 0};
    }

    /**
     * Structure 3: Segment Tree over slots 1..D.
     */
    private static int[] segTreeCount;

    private static void segBuild(int node, int lo, int hi) {
        segTreeCount[node] = (hi - lo + 1);
        if (lo == hi) return;
        int mid = (lo + hi) >>> 1;
        segBuild(2 * node, lo, mid);
        segBuild(2 * node + 1, mid + 1, hi);
    }

    private static int segRightmost(int node, int lo, int hi, int d) {
        if (lo > d || segTreeCount[node] == 0) return 0;
        if (lo == hi) return lo;
        int mid = (lo + hi) >>> 1;
        // Search right child first for latest free slot
        int right = segRightmost(2 * node + 1, mid + 1, hi, d);
        if (right != 0) return right;
        return segRightmost(2 * node, lo, mid, d);
    }

    private static void segTake(int node, int lo, int hi, int pos) {
        segTreeCount[node]--;
        if (lo == hi) return;
        int mid = (lo + hi) >>> 1;
        if (pos <= mid) {
            segTake(2 * node, lo, mid, pos);
        } else {
            segTake(2 * node + 1, mid + 1, hi, pos);
        }
    }

    public static long[] segmentTree(int[] sortedDeadline, int[] sortedProfit, int D) {
        segTreeCount = new int[4 * D + 4];
        segBuild(1, 1, D);
        long profit = 0;

        for (int k = 0; k < sortedDeadline.length; k++) {
            int d = Math.min(sortedDeadline[k], D);
            int slot = segRightmost(1, 1, D, d);
            if (slot > 0) {
                segTake(1, 1, D, slot);
                profit += sortedProfit[k];
            }
        }
        return new long[]{profit, 0};
    }

    /**
     * Structure 4: Disjoint Set Union (DSU) with Path Compression.
     *
     * @param countHops If true, counts total parent traversals.
     * @return long array where [0] = total profit, [1] = parent hop count.
     */
    public static long[] dsu(int[] sortedDeadline, int[] sortedProfit, int D, boolean countHops) {
        int[] parent = new int[D + 1];
        for (int s = 0; s <= D; s++) {
            parent[s] = s;
        }
        long profit = 0;
        long hops = 0;

        for (int k = 0; k < sortedDeadline.length; k++) {
            int d = Math.min(sortedDeadline[k], D);

            // Find root with optional hop counting
            int root = d;
            while (parent[root] != root) {
                root = parent[root];
                if (countHops) hops++;
            }

            // Path compression
            int curr = d;
            while (parent[curr] != root) {
                int next = parent[curr];
                parent[curr] = root;
                curr = next;
            }

            if (root > 0) {
                profit += sortedProfit[k];
                // Union root with root - 1
                int rPrev = root - 1;
                while (parent[rPrev] != rPrev) {
                    rPrev = parent[rPrev];
                    if (countHops) hops++;
                }
                parent[root] = rPrev;
            }
        }

        return new long[]{profit, hops};
    }

    public static void main(String[] args) {
        // Small verification run
        int[] sd = {2, 4, 3, 4, 2, 1, 1, 3};
        int[] sp = {100, 60, 40, 30, 27, 25, 19, 15};
        int D = 4;

        System.out.println("=== Slot Finders Functional Demonstration ===");
        System.out.println("Linear scan profit : " + linearScan(sd, sp, D)[0]);
        System.out.println("TreeSet BST profit : " + treeSet(sd, sp, D)[0]);
        System.out.println("Segment Tree profit: " + segmentTree(sd, sp, D)[0]);
        System.out.println("DSU profit         : " + dsu(sd, sp, D, true)[0]);
    }
}
