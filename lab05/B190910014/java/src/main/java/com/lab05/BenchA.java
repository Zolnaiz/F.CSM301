package com.lab05;

import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.function.Supplier;

/**
 * Лаб 5 хэмжилт (Python-ы bench_a.py-тэй ижил). lab05/<Student-ID>/java-аас:
 *   javac -d build src/main/java/com/lab05/*.java
 *   java -cp build com.lab05.BenchA [c] [huffman] [caching]   -> ../out/a_<хэсэг>_java.tsv
 * Хугацаа: JIT халаах 1 дуудалтын дараа 5 удаагийн медиан (≥ 5 с бол 1 удаа).
 * Санах ой: нэг дуудалтад хуваарилсан байт (ThreadMXBean), KB.
 */
public final class BenchA {

    private static final Path STUDENT_DIR = Paths.get("..").toAbsolutePath().normalize();
    private static final com.sun.management.ThreadMXBean THREADS =
            (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
    private static final int[] TOGROG = {1, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 20000};

    record M(Object result, double ms, double kb) {}

    static M measure(Supplier<Object> fn) {
        long tid = Thread.currentThread().getId();
        long a0 = THREADS.getThreadAllocatedBytes(tid);
        long t0 = System.nanoTime();
        Object result = fn.get();
        double first = (System.nanoTime() - t0) / 1e6;
        double kb = (THREADS.getThreadAllocatedBytes(tid) - a0) / 1024.0;
        if (first >= 5000) return new M(result, first, kb);
        double[] times = new double[5];
        for (int r = 0; r < times.length; r++) {
            t0 = System.nanoTime();
            fn.get();
            times[r] = (System.nanoTime() - t0) / 1e6;
        }
        Arrays.sort(times);
        return new M(result, times[2], kb);
    }

    static void save(String name, String header, List<String> rows) throws IOException {
        Path p = STUDENT_DIR.resolve("out").resolve("a_" + name + "_java.tsv");
        Files.createDirectories(p.getParent());
        Files.writeString(p, header + "\n" + String.join("\n", rows) + "\n", StandardCharsets.UTF_8);
        System.out.println("  -> " + p + "\n");
    }

    static String f(double x) {
        return String.format(Locale.ROOT, "%.3f", x);
    }

    static String row(Object... cells) {
        StringJoiner j = new StringJoiner("\t");
        for (Object c : cells) j.add(String.valueOf(c));
        System.out.println("  " + j);
        return j.toString();
    }

    static void benchC() throws IOException {
        Random rng = new Random(5);
        List<String> rows = new ArrayList<>();
        for (int n : new int[] {10_000, 100_000, 1_000_000}) {
            int[] s = new int[n], fin = new int[n], w = new int[n], v = new int[n];
            for (int i = 0; i < n; i++) {
                s[i] = rng.nextInt(10 * n + 1);
                fin[i] = s[i] + 1 + rng.nextInt(100);
                w[i] = 1 + rng.nextInt(100);
                v[i] = 1 + rng.nextInt(100);
            }
            M a = measure(() -> Activity.select(s, fin));
            rows.add(row("activity_select", n, ((int[]) a.result()).length, f(a.ms()), String.format(Locale.ROOT, "%.1f", a.kb())));
            M k = measure(() -> Knapsack.fractional(w, v, 25 * n));
            rows.add(row("fractional_knapsack", n, String.format(Locale.ROOT, "%.2f", (double) k.result()), f(k.ms()),
                    String.format(Locale.ROOT, "%.1f", k.kb())));
        }
        for (int x : new int[] {3760, 1_000_000, 1_000_000_000}) {
            M m = measure(() -> Change.makeChange(TOGROG, x));
            rows.add(row("make_change", x, Arrays.stream((int[]) m.result()).sum(), String.format(Locale.ROOT, "%.5f", m.ms()),
                    String.format(Locale.ROOT, "%.1f", m.kb())));
        }
        for (int x : new int[] {10_000, 100_000, 1_000_000}) {
            M m = measure(() -> Change.minCoins(TOGROG, x));
            rows.add(row("min_coins", x, m.result(), f(m.ms()), String.format(Locale.ROOT, "%.1f", m.kb())));
        }
        save("c", "problem\tn_or_x\tresult\ttime_ms\talloc_kb", rows);
    }

    interface Codec {
        String decode(String bits, Map<String, String> codes);
    }

    static void benchHuffman() throws IOException {
        String base = Files.readString(STUDENT_DIR.getParent().resolve("test_data").resolve("mn_text.txt"),
                StandardCharsets.UTF_8).replace("\r\n", "\n"); // Windows-ийн CRLF -> LF (Python-той ижил)
        List<String> rows = new ArrayList<>();
        for (int k : new int[] {1, 2, 4, 8, 16}) {
            String text = base.repeat(k);
            Map<String, String> codes = Huffman.build(frequencies(text));
            String bits = Huffman.encode(text, codes);
            for (String variant : new String[] {"basic", "fast"}) {
                boolean fast = variant.equals("fast");
                Supplier<Object> run = () -> {
                    Map<String, String> c = Huffman.build(frequencies(text));
                    String b = fast ? HuffmanFast.encode(text, c) : Huffman.encode(text, c);
                    return fast ? HuffmanFast.decode(b, c) : Huffman.decode(b, c);
                };
                if (!text.equals(run.get())) throw new IllegalStateException("тайлалт буруу");
                M total = measure(run);
                M dec = measure(() -> fast ? HuffmanFast.decode(bits, codes) : Huffman.decode(bits, codes));
                rows.add(row(variant, text.codePointCount(0, text.length()), bits.length(), f(total.ms()), f(dec.ms()),
                        String.format(Locale.ROOT, "%.1f", total.kb()), String.format(Locale.ROOT, "%.1f", dec.kb())));
            }
        }
        save("huffman", "variant\tchars\tbits\ttotal_ms\tdecode_ms\talloc_kb\tdecode_alloc_kb", rows);
    }

    static Map<String, Long> frequencies(String text) {
        Map<String, Long> freq = new HashMap<>();
        text.codePoints().forEach(cp -> freq.merge(new String(Character.toChars(cp)), 1L, Long::sum));
        return freq;
    }

    static void benchCaching() throws IOException {
        String line = Files.readAllLines(STUDENT_DIR.resolve("test_data").resolve("personal.tsv"),
                StandardCharsets.UTF_8).get(1);
        String[] parts = line.split("\t")[1].split(",");
        int[] requests = Arrays.stream(parts).mapToInt(Integer::parseInt).toArray();
        List<String> rows = new ArrayList<>();
        boolean basicStopped = false;
        for (int n : new int[] {1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000, 200_000}) {
            int[] req = Arrays.copyOf(requests, n);
            M fast = measure(() -> CachingFast.misses(64, req));
            rows.add(row("fast", n, 64, fast.result(), f(fast.ms()), String.format(Locale.ROOT, "%.1f", fast.kb())));
            if (!basicStopped) {
                M basic = measure(() -> Caching.misses(64, req));
                if (!basic.result().equals(fast.result())) throw new IllegalStateException("алдааны тоо зөрөв");
                rows.add(row("basic", n, 64, basic.result(), f(basic.ms()), String.format(Locale.ROOT, "%.1f", basic.kb())));
                basicStopped = basic.ms() >= 10_000;
            }
        }
        save("caching", "variant\tn\tk\tmisses\ttime_ms\talloc_kb", rows);
    }

    public static void main(String[] args) throws IOException {
        List<String> sections = args.length > 0 ? List.of(args) : List.of("c", "huffman", "caching");
        for (String s : sections) {
            switch (s) {
                case "c" -> benchC();
                case "huffman" -> benchHuffman();
                case "caching" -> benchCaching();
                default -> throw new IllegalArgumentException("хэсэг: c, huffman, caching");
            }
        }
    }

    private BenchA() {}
}
