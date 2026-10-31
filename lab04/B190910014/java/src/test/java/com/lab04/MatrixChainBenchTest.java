package com.lab04;

import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class MatrixChainBenchTest {

    private static final int REPEATS = 5;
    private static final double TIME_LIMIT_MS = 10_000;

    @Test
    void benchmark() {
        Assumptions.assumeTrue(Files.exists(Tsv.MINE.resolve("personal_chain.tsv")),
                "personal_chain.tsv олдсонгүй. Эхлээд: cd lab04/<Student-ID> && "
                + "python3 ../tools/gen_lab04.py <Student-ID>");

        List<Object[]> results = new ArrayList<>();
        for (Map<String, String> r : Tsv.rows("personal_chain.tsv")) {
            int[] p = Tsv.ints(r.get("p"));
            int n = p.length - 1;

            long t0 = System.nanoTime();
            MatrixChain.Result res = MatrixChain.order(p);
            double first = (System.nanoTime() - t0) / 1e6;
            List<Double> times = new ArrayList<>(List.of(first));
            if (first < TIME_LIMIT_MS) {
                for (int i = 1; i < REPEATS; i++) {
                    t0 = System.nanoTime();
                    MatrixChain.order(p);
                    times.add((System.nanoTime() - t0) / 1e6);
                }
            }
            Collections.sort(times);
            double median = times.get(times.size() / 2);
            results.add(new Object[] {n, res.minMults(), String.format(Locale.ROOT, "%.3f", median)});
            System.out.printf("  n=%-6d min_mults=%-12d %9.3f ms%n", n, res.minMults(), median);
            if (first >= TIME_LIMIT_MS) {
                System.out.println("  хугацаа хэтэрсэн тул үлдсэн оролтыг алгаслаа");
                break;
            }
        }

        Path out = Tsv.writeResults("chain", "java",
                new String[] {"n", "min_mults", "time_ms"}, results);
        System.out.println("\n  -> " + out);
    }
}
