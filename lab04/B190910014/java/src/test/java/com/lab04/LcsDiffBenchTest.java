package com.lab04;

import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class LcsDiffBenchTest {

    private static final int REPEATS = 3;
    private static final double TIME_LIMIT_MS = 10_000;

    @Test
    void benchmark() {
        Assumptions.assumeTrue(Files.exists(Tsv.MINE.resolve("personal_diff.tsv")),
                "personal_diff.tsv олдсонгүй. Эхлээд: cd lab04/<Student-ID> && "
                + "python3 ../tools/gen_lab04.py <Student-ID>");

        List<Object[]> results = new ArrayList<>();
        for (Map<String, String> r : Tsv.rows("personal_diff.tsv")) {
            List<String> a = Tsv.strs(r.get("A"));
            List<String> b = Tsv.strs(r.get("B"));

            long t0 = System.nanoTime();
            List<String> out = Lcs.diff(a, b);
            double first = (System.nanoTime() - t0) / 1e6;
            long common = out.stream().filter(s -> s.startsWith(" ")).count();
            List<Double> times = new ArrayList<>(List.of(first));
            if (first < TIME_LIMIT_MS) {
                for (int i = 1; i < REPEATS; i++) {
                    t0 = System.nanoTime();
                    Lcs.diff(a, b);
                    times.add((System.nanoTime() - t0) / 1e6);
                }
            }
            Collections.sort(times);
            double median = times.get(times.size() / 2);
            results.add(new Object[] {a.size(), b.size(), common, String.format(Locale.ROOT, "%.3f", median)});
            System.out.printf("  |A|=%-6d |B|=%-6d common=%-6d %9.3f ms%n", a.size(), b.size(),
                    common, median);
            if (first >= TIME_LIMIT_MS) {
                System.out.println("  хугацаа хэтэрсэн тул үлдсэн оролтыг алгаслаа");
                break;
            }
        }

        Path out = Tsv.writeResults("diff", "java",
                new String[] {"m", "n", "common", "time_ms"}, results);
        System.out.println("\n  -> " + out);
    }
}
