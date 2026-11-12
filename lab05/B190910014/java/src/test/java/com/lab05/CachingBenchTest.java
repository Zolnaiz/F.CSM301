package com.lab05;

import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class CachingBenchTest {

    private static final int K = 64;
    private static final int[] SIZES = {1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000, 200_000};
    private static final double TIME_LIMIT_MS = 10_000;

    @Test
    void benchmark() {
        Assumptions.assumeTrue(Files.exists(Tsv.MINE.resolve("personal.tsv")),
                "personal.tsv олдсонгүй. Эхлээд: cd lab05/<Student-ID> && "
                + "python3 ../tools/gen_lab05.py <Student-ID>");

        int[] requests = Tsv.ints(Tsv.rows("personal.tsv").get(0).get("requests"));
        List<Object[]> results = new ArrayList<>();
        for (int n : SIZES) {
            if (n > requests.length) break;
            int[] prefix = Arrays.copyOf(requests, n);
            long t0 = System.nanoTime();
            long misses = Caching.misses(K, prefix);
            double ms = (System.nanoTime() - t0) / 1e6;
            results.add(new Object[] {n, K, misses, String.format(Locale.ROOT, "%.3f", ms)});
            System.out.printf("  n=%-8d k=%d misses=%-8d %10.3f ms%n", n, K, misses, ms);
            if (ms >= TIME_LIMIT_MS) {
                System.out.println("  хугацаа хэтэрсэн тул үлдсэн оролтыг алгаслаа");
                break;
            }
        }

        Path out = Tsv.writeResults("caching", "java",
                new String[] {"n", "k", "misses", "time_ms"}, results);
        System.out.println("\n  -> " + out);
    }
}
