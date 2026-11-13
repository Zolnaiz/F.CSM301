package com.prj2;

import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.function.Function;
import java.util.function.Supplier;

/**
 * Бие даалт 2 — хэмжилт (python/bench.py-тэй ижил оролт). prj2/<ID>/java-аас:
 *   javac -d build src/main/java/com/prj2/*.java && java -cp build com.prj2.Bench
 * Хугацаа: JIT халаасны дараа ≥ 20 ms багцын 5 хэмжилтийн медиан. Санах ой: нэг дуудалтад
 * хуваарилсан байт (ThreadMXBean), оролтыг оролцуулахгүй.
 */
public final class Bench {

    private static final com.sun.management.ThreadMXBean THREADS =
            (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
    private static final List<String> ROWS = new ArrayList<>();

    static <A> void record(String problem, String variant, String kase, long n, Supplier<A> makeArgs,
                           Function<A, Object> fn, Function<Object, String> extra) {
        long tid = Thread.currentThread().getId();
        A args = makeArgs.get();
        long t0 = System.nanoTime();
        Object result = fn.apply(args);
        double first = (System.nanoTime() - t0) / 1e6;
        double ms = first;
        if (first < 5000) {
            for (int w = 0; w < 3; w++) fn.apply(makeArgs.get()); // JIT
            int iters = (int) Math.max(1, Math.min(100_000, 20 / Math.max(first, 1e-4)));
            double[] times = new double[5];
            for (int r = 0; r < times.length; r++) {
                List<A> batch = new ArrayList<>();
                for (int i = 0; i < iters; i++) batch.add(makeArgs.get());
                t0 = System.nanoTime();
                for (A a : batch) fn.apply(a);
                times[r] = (System.nanoTime() - t0) / 1e6 / iters;
            }
            Arrays.sort(times);
            ms = times[2];
        }
        A fresh = makeArgs.get();
        long a0 = THREADS.getThreadAllocatedBytes(tid);
        fn.apply(fresh);
        double kb = (THREADS.getThreadAllocatedBytes(tid) - a0) / 1024.0;
        String row = String.join("\t", problem, variant, kase, String.valueOf(n),
                String.format(Locale.ROOT, "%.4f", ms), String.format(Locale.ROOT, "%.1f", kb), extra.apply(result));
        ROWS.add(row);
        System.out.printf("  %s %-9s %-8s n=%-9d %12.4f ms %12.1f KB  %s%n", problem, variant, kase, n, ms, kb,
                extra.apply(result));
    }

    record Pair(String a, String b) {}

    public static void main(String[] args) throws IOException {
        Random rng = new Random(2026);

        for (int n : new int[] {1000, 10_000, 100_000}) {
            String hay = "a".repeat(n - 1) + "b";
            String needle = "a".repeat(99) + "b";
            String text = random(rng, "abcd", n);
            String pat = random(rng, "abcd", 100);
            for (String kase : new String[] {"worst", "random"}) {
                Pair p = kase.equals("worst") ? new Pair(hay, needle) : new Pair(text, pat);
                record("p1", "kmp", kase, n, () -> p, x -> new StrStr().strStr(x.a(), x.b()), String::valueOf);
                record("p1", "naive", kase, n, () -> p, x -> new StrStr().strStrNaive(x.a(), x.b()), String::valueOf);
            }
        }

        for (int side : new int[] {50, 200, 1000}) {
            record("p2", "bfs", "full", (long) side * side, () -> {
                int[][] img = new int[side][side];
                for (int[] row : img) Arrays.fill(row, 1);
                return img;
            }, img -> new FloodFill().floodFill(img, 0, 0, 2), r -> "");
        }

        for (int n : new int[] {10_000, 100_000, 1_000_000}) {
            int[] g = rng.ints(n, 1, Integer.MAX_VALUE).toArray();
            int[] s = rng.ints(n, 1, Integer.MAX_VALUE).toArray();
            record("p3", "greedy", "random", n, () -> new int[][] {g.clone(), s.clone()},
                    x -> new AssignCookies().findContentChildren(x[0], x[1]), String::valueOf);
        }

        for (int n : new int[] {1000, 10_000, 100_000}) {
            int[] nums = rng.ints(n, 1, 1001).toArray();
            if (n <= 100_000) {
                record("p4", "dp", "random", n, () -> nums, a -> {
                    JumpGame j = new JumpGame();
                    return new long[] {j.jump(a), j.steps};
                }, r -> "jumps=" + ((long[]) r)[0] + ";steps=" + ((long[]) r)[1]);
            }
            record("p4", "greedy", "random", n, () -> nums, a -> new JumpGameImproved().jump(a), r -> "jumps=" + r);
        }

        Set<String> randomDead = new TreeSet<>();
        for (int i = 0; i < 500; i++) randomDead.add(String.format("%04d", rng.nextInt(10000)));
        randomDead.remove("0000");
        randomDead.remove("7319");
        Map<String, Object[]> cases = new LinkedHashMap<>();
        cases.put("far", new Object[] {new String[0], "5555"});
        cases.put("example", new Object[] {new String[] {"0201", "0101", "0102", "1212", "2002"}, "0202"});
        cases.put("random", new Object[] {randomDead.toArray(new String[0]), "7319"});
        cases.put("blocked", new Object[] {new String[] {"8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"}, "8888"});
        for (var e : cases.entrySet()) {
            String[] dead = (String[]) e.getValue()[0];
            String target = (String) e.getValue()[1];
            record("p5", "bfs", e.getKey(), dead.length, () -> dead, d -> {
                OpenLock o = new OpenLock();
                return new long[] {o.openLock(d, target), o.expanded};
            }, r -> "answer=" + ((long[]) r)[0] + ";expanded=" + ((long[]) r)[1]);
            record("p5", "bidir", e.getKey(), dead.length, () -> dead, d -> {
                OpenLockImproved o = new OpenLockImproved();
                return new long[] {o.openLock(d, target), o.expanded};
            }, r -> "answer=" + ((long[]) r)[0] + ";expanded=" + ((long[]) r)[1]);
        }

        Path out = Paths.get("..").toAbsolutePath().normalize().resolve("out").resolve("results_java.tsv");
        Files.createDirectories(out.getParent());
        Files.writeString(out, "problem\tvariant\tcase\tn\ttime_ms\talloc_kb\textra\n" + String.join("\n", ROWS) + "\n",
                StandardCharsets.UTF_8);
        System.out.println("\n  -> " + out);
    }

    private static String random(Random rng, String alphabet, int n) {
        StringBuilder sb = new StringBuilder(n);
        for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
        return sb.toString();
    }

    private Bench() {}
}
