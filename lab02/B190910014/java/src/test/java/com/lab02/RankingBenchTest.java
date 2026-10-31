package com.lab02;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class RankingBenchTest {

    private static final int[] SIZES = {100, 1_000, 10_000, 100_000, 1_000_000};
    private static final int REPEATS = 5;

    @Test
    void benchmark() throws IOException {
        List<Object[]> results = new ArrayList<>();
        for (int n : SIZES) {
            Path p = Tsv.MINE.resolve("personal_" + n + ".tsv");
            if (!Files.exists(p)) continue;

            int[] a = new int[n];
            int[] b = new int[n];
            try (var lines = Files.lines(p, StandardCharsets.UTF_8)) {
                Iterator<String> it = lines.iterator();
                it.next();                       // эхний мөр нь n
                for (int i = 0; i < n && it.hasNext(); i++) {
                    String[] f = it.next().trim().split("\\s+");
                    a[i] = Integer.parseInt(f[0]);
                    b[i] = Integer.parseInt(f[1]);
                }
            }

            long distance = RankingDistance.distance(a, b);
            double[] times = new double[REPEATS];
            for (int i = 0; i < REPEATS; i++) {
                long t0 = System.nanoTime();
                RankingDistance.distance(a, b);
                times[i] = (System.nanoTime() - t0) / 1e6;
            }
            Arrays.sort(times);
            double median = times[REPEATS / 2];
            results.add(new Object[] {n, distance, String.format("%.3f", median)});
            System.out.printf("  n=%-9d distance=%-14d %9.3f ms%n", n, distance, median);
        }

        Assumptions.assumeFalse(results.isEmpty(),
                "personal_*.tsv олдсонгүй. Эхлээд: cd lab02/<Student-ID> && "
                + "python3 ../tools/gen_lab02.py <Student-ID>");

        Path out = Tsv.writeResults("java", new String[] {"n", "distance", "time_ms"},
                results);
        System.out.println("\n  -> " + out);
    }
}
