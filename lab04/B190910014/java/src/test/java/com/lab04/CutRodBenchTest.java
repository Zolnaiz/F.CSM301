package com.lab04;

import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class CutRodBenchTest {

    private static final int REPEATS = 5;

    @Test
    void benchmark() {
        Assumptions.assumeTrue(Files.exists(Tsv.MINE.resolve("personal.tsv")),
                "personal.tsv олдсонгүй. Эхлээд: cd lab04/<Student-ID> && "
                + "python3 ../tools/gen_lab04.py <Student-ID>");

        List<Object[]> results = new ArrayList<>();
        for (Map<String, String> r : Tsv.rows("personal.tsv")) {
            int[] p = Tsv.ints(r.get("p"));
            int n = p.length;

            CutRod.Result res = CutRod.bottomUp(p);
            double[] times = new double[REPEATS];
            for (int i = 0; i < REPEATS; i++) {
                long t0 = System.nanoTime();
                CutRod.bottomUp(p);
                times[i] = (System.nanoTime() - t0) / 1e6;
            }
            Arrays.sort(times);
            double median = times[REPEATS / 2];
            results.add(new Object[] {n, res.revenue(), res.innerLoopCount(),
                    String.format("%.3f", median)});
            System.out.printf("  n=%-6d revenue=%-10d loops=%-10d %9.3f ms%n", n,
                    res.revenue(), res.innerLoopCount(), median);
        }

        Path out = Tsv.writeResults("java",
                new String[] {"n", "revenue", "loop_count", "time_ms"}, results);
        System.out.println("\n  -> " + out);
    }
}
