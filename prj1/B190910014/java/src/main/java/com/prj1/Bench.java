package com.prj1;

import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.function.Supplier;

/**
 * Бие даалт 1-ийн хэмжилт: хугацаа (ms) ба тухайн дуудалтад хуваарилсан санах ой (KB).
 * prj1/B190910014/java хавтаснаас:
 *   javac -d build src/main/java/com/prj1/*.java && java -Xss64m -cp build com.prj1.Bench
 * Үр дүн: ../out/results_java.tsv
 */
public final class Bench {

    private static final Path OUT = Paths.get("..").toAbsolutePath().normalize().resolve("out");
    private static final com.sun.management.ThreadMXBean THREADS =
            (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
    private static final Random RNG = new Random(14);
    private static final List<String> ROWS = new ArrayList<>();

    private static void record(String problem, String variant, String kase, int n,
                               Supplier<Object> fn, String extra) {
        // JIT халаах ба багцын хэмжээг сонгох: нэг багц ≥ 20 ms байхаар давталтын тоог өсгөнө.
        System.gc(); // өмнөх хэмжилтийн хог энэ хэмжилтэд орохгүй
        int iters = 1;
        while (true) {
            long t0 = System.nanoTime();
            for (int i = 0; i < iters; i++) fn.get();
            if (System.nanoTime() - t0 >= 20_000_000L || iters >= 1 << 20) break;
            iters *= 2;
        }
        long tid = Thread.currentThread().getId();
        double[] times = new double[5];
        long allocated = 0;
        for (int b = 0; b < times.length; b++) {
            long a0 = THREADS.getThreadAllocatedBytes(tid);
            long t0 = System.nanoTime();
            for (int i = 0; i < iters; i++) fn.get();
            times[b] = (System.nanoTime() - t0) / 1e6 / iters; // нэг дуудалтын дундаж
            allocated = (THREADS.getThreadAllocatedBytes(tid) - a0) / iters;
        }
        Arrays.sort(times);
        double ms = times[times.length / 2];
        double kb = allocated / 1024.0;
        ROWS.add(String.join("\t", problem, variant, kase, String.valueOf(n),
                String.format(Locale.ROOT, "%.3f", ms), String.format(Locale.ROOT, "%.1f", kb), extra));
        System.out.printf("  %s %-9s %-7s n=%-8d %10.3f ms %10.1f KB %s%n", problem, variant, kase, n, ms, kb, extra);
    }

    public static void main(String[] args) throws IOException {
        for (int n : new int[] {1_000, 10_000, 100_000, 1_000_000}) {
            int[] nums = majorityInput(n);
            record("p1", "dc", "random", n, () -> new MajorityElement().majorityElement(nums), "");
        }
        for (int n : new int[] {1_000, 10_000, 100_000, 1_000_000}) {
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = i;
            record("p2", "basic", "sorted", n, () -> new SortedArrayToBst().sortedArrayToBST(nums), "");
        }
        for (int n : new int[] {100, 1_000, 10_000, 100_000}) {
            for (String kase : new String[] {"nice", "split"}) {
                String s = niceInput(n, kase.equals("split"));
                record("p3", "dc", kase, n, () -> new LongestNiceSubstring().longestNiceSubstring(s), "");
            }
        }
        for (int k = 2; k <= 10; k++) {
            String expr = expression(k);
            DifferentWays basic = new DifferentWays();
            basic.diffWaysToCompute(expr);
            record("p4", "basic", "random", k, () -> new DifferentWays().diffWaysToCompute(expr), "calls=" + basic.calls);
            DifferentWaysImproved improved = new DifferentWaysImproved();
            improved.diffWaysToCompute(expr);
            record("p4", "improved", "random", k, () -> new DifferentWaysImproved().diffWaysToCompute(expr),
                    "calls=" + improved.calls);
        }
        for (int n : new int[] {500, 1_000, 2_000, 4_000}) {
            for (String kase : new String[] {"random", "chain"}) {
                TreeNode tree = kase.equals("random") ? randomTree(n) : chain(n);
                int[] pre = Traversal.preorder(tree);
                int[] ino = Traversal.inorder(tree);
                record("p5", "basic", kase, n, () -> new BuildTree().buildTree(pre, ino), "");
                record("p5", "improved", kase, n, () -> new BuildTreeImproved().buildTree(pre, ino), "");
            }
        }
        Files.createDirectories(OUT);
        Path path = OUT.resolve("results_java.tsv");
        Files.writeString(path, "problem\tvariant\tcase\tn\ttime_ms\talloc_kb\textra\n"
                + String.join("\n", ROWS) + "\n", StandardCharsets.UTF_8);
        System.out.println("\n  -> " + path);
    }

    private static int[] majorityInput(int n) {
        int k = n / 2 + 1;
        List<Integer> list = new ArrayList<>(n);
        for (int i = 0; i < n; i++) list.add(i < k ? 7 : RNG.nextInt(2_000_001) - 1_000_000);
        Collections.shuffle(list, RNG);
        return list.stream().mapToInt(Integer::intValue).toArray();
    }

    /** split=true: «z» үсгийн том хэлбэр байхгүй тул түүгээр олон хуваалт хийгдэнэ. */
    private static String niceInput(int n, boolean split) {
        String alphabet = split ? "abcdeABCDEz" : "abcdeABCDE";
        StringBuilder sb = new StringBuilder(n);
        for (int i = 0; i < n; i++) sb.append(alphabet.charAt(RNG.nextInt(alphabet.length())));
        return sb.toString();
    }

    private static String expression(int k) {
        StringBuilder sb = new StringBuilder().append(1 + RNG.nextInt(99));
        for (int i = 0; i < k; i++) sb.append("+-*".charAt(RNG.nextInt(3))).append(1 + RNG.nextInt(99));
        return sb.toString();
    }

    private static TreeNode randomTree(int n) {
        List<Integer> vals = new ArrayList<>();
        Set<Integer> seen = new HashSet<>();
        while (vals.size() < n) {
            int v = RNG.nextInt(2_000_001) - 1_000_000;
            if (seen.add(v)) vals.add(v);
        }
        return make(vals, 0, n);
    }

    private static TreeNode make(List<Integer> vals, int lo, int hi) {
        if (lo >= hi) return null;
        int k = lo + RNG.nextInt(hi - lo);
        return new TreeNode(vals.get(k), make(vals, lo, k), make(vals, k + 1, hi));
    }

    private static TreeNode chain(int n) {
        TreeNode root = null;
        for (int v = 0; v < n; v++) root = new TreeNode(v, root, null);
        return root;
    }

    /** Модыг давталтаар тойрох туслах функцүүд. */
    static final class Traversal {
        static int[] inorder(TreeNode root) {
            List<Integer> out = new ArrayList<>();
            Deque<TreeNode> stack = new ArrayDeque<>();
            TreeNode node = root;
            while (node != null || !stack.isEmpty()) {
                while (node != null) { stack.push(node); node = node.left; }
                node = stack.pop();
                out.add(node.val);
                node = node.right;
            }
            return out.stream().mapToInt(Integer::intValue).toArray();
        }

        static int[] preorder(TreeNode root) {
            List<Integer> out = new ArrayList<>();
            Deque<TreeNode> stack = new ArrayDeque<>();
            if (root != null) stack.push(root);
            while (!stack.isEmpty()) {
                TreeNode node = stack.pop();
                out.add(node.val);
                if (node.right != null) stack.push(node.right);
                if (node.left != null) stack.push(node.left);
            }
            return out.stream().mapToInt(Integer::intValue).toArray();
        }

        private Traversal() {}
    }

    private Bench() {}
}
