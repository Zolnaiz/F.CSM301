package com.lab05;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class HuffmanBenchTest {

    private static final int REPEATS = 3;
    private static final int[] FACTORS = {1, 2, 4, 8, 16};

    @Test
    void benchmark() throws IOException {
        Assumptions.assumeTrue(Files.exists(Tsv.MINE.resolve("personal.tsv")),
                "personal.tsv олдсонгүй. Эхлээд: cd lab05/<Student-ID> && "
                + "python3 ../tools/gen_lab05.py <Student-ID>");

        String base = Files.readString(Tsv.SHARED.resolve("mn_text.txt"), StandardCharsets.UTF_8);
        List<Object[]> results = new ArrayList<>();
        for (int k : FACTORS) {
            String text = base.repeat(k);
            double[] times = new double[REPEATS];
            long bits = 0;
            for (int i = 0; i < REPEATS; i++) {
                long t0 = System.nanoTime();
                Map<String, String> codes = Huffman.build(HuffmanTest.frequencies(text));
                String enc = Huffman.encode(text, codes);
                Huffman.decode(enc, codes);
                times[i] = (System.nanoTime() - t0) / 1e6;
                bits = enc.length();
            }
            Arrays.sort(times);
            double median = times[REPEATS / 2];
            long chars = text.codePointCount(0, text.length());
            results.add(new Object[] {chars, bits, String.format(Locale.ROOT, "%.3f", median)});
            System.out.printf("  chars=%-9d bits=%-10d %10.3f ms%n", chars, bits, median);
        }

        Path out = Tsv.writeResults("huffman", "java",
                new String[] {"chars", "bits", "time_ms"}, results);
        System.out.println("\n  -> " + out);
    }
}
