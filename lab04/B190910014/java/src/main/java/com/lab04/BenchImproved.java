package com.lab04;

import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.function.Supplier;

/**
 * A түвшин: өмнөх ба сайжруулсан шийдлийн хугацаа (ms) ба нэг дуудалтад хуваарилсан санах ой (KB).
 * lab04/<Student-ID>/java хавтаснаас:
 *   javac -d build src/main/java/com/lab04/*.java && java -cp build com.lab04.BenchImproved
 * Үр дүн: ../out/improved_java.tsv
 */
public final class BenchImproved {

    private static final Path STUDENT_DIR = Paths.get("..").toAbsolutePath().normalize();
    private static final com.sun.management.ThreadMXBean THREADS =
            (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
    private static final List<String> ROWS = new ArrayList<>();

    private static void record(String task, String variant, int n, Supplier<Object> fn, String extra) {
        System.gc();
        int iters = 1;
        while (true) { // JIT халаах ба багц ≥ 20 ms
            long t0 = System.nanoTime();
            for (int i = 0; i < iters; i++) fn.get();
            if (System.nanoTime() - t0 >= 20_000_000L || iters >= 1 << 16) break;
            iters *= 2;
        }
        long tid = Thread.currentThread().getId();
        double[] times = new double[5];
        long allocated = 0;
        for (int b = 0; b < times.length; b++) {
            long a0 = THREADS.getThreadAllocatedBytes(tid);
            long t0 = System.nanoTime();
            for (int i = 0; i < iters; i++) fn.get();
            times[b] = (System.nanoTime() - t0) / 1e6 / iters;
            allocated = (THREADS.getThreadAllocatedBytes(tid) - a0) / iters;
        }
        Arrays.sort(times);
        double ms = times[2];
        double kb = allocated / 1024.0;
        ROWS.add(String.join("\t", task, variant, String.valueOf(n),
                String.format(Locale.ROOT, "%.3f", ms), String.format(Locale.ROOT, "%.1f", kb), extra));
        System.out.printf("  %-5s %-9s n=%-6d %11.3f ms %11.1f KB %s%n", task, variant, n, ms, kb, extra);
    }

    private static List<String[]> rows(String name) throws IOException {
        List<String> lines = Files.readAllLines(STUDENT_DIR.resolve("test_data").resolve(name), StandardCharsets.UTF_8);
        List<String[]> out = new ArrayList<>();
        for (String line : lines.subList(1, lines.size())) if (!line.isEmpty()) out.add(line.split("\t"));
        return out;
    }

    public static void main(String[] args) throws IOException {
        for (String[] r : rows("personal_diff.tsv")) {
            List<String> a = List.of(r[1].split(","));
            List<String> b = List.of(r[2].split(","));
            long common = Lcs.diffMyers(a, b).stream().filter(s -> s.charAt(0) == ' ').count();
            String d = "D=" + (a.size() + b.size() - 2 * common);
            record("diff", "dp", a.size(), () -> Lcs.diff(a, b), d);
            record("diff", "myers", a.size(), () -> Lcs.diffMyers(a, b), d);
        }
        List<String[]> chain = rows("personal_chain.tsv");
        int[] pAll = Arrays.stream(chain.get(chain.size() - 1)[1].split(",")).mapToInt(Integer::parseInt).toArray();
        for (int n : new int[] {4, 6, 8, 10, 12, 14, 16}) {
            int[] p = Arrays.copyOf(pAll, n + 1);
            long calls = MatrixChain.recursive(p).calls();
            record("chain", "recursive", n, () -> MatrixChain.recursive(p), "calls=" + calls);
            record("chain", "dp", n, () -> MatrixChain.order(p), "calls=" + n * (n + 1) / 2);
        }
        Path path = STUDENT_DIR.resolve("out").resolve("improved_java.tsv");
        Files.createDirectories(path.getParent());
        Files.writeString(path, "task\tvariant\tn\ttime_ms\talloc_kb\textra\n" + String.join("\n", ROWS) + "\n",
                StandardCharsets.UTF_8);
        System.out.println("\n  -> " + path);
    }

    private BenchImproved() {}
}
