package com.lab03;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/**
 * 5-р даалгаврын хэмжилт. lab03/<Student-ID>/java хавтаснаас ажиллуулна:
 *   javac -d build src/main/java/com/lab03/*.java
 *   java -cp build com.lab03.Bench
 * Үр дүн: ../out/results_java.tsv (n, algorithm, time_ms, mults)
 */
public final class Bench {

    private static final Path STUDENT_DIR = Paths.get("..").toAbsolutePath().normalize();
    private static final Path DATA = STUDENT_DIR.resolve("test_data");
    private static final Path OUT = STUDENT_DIR.resolve("out");
    private static final double LIMIT_MS = 60_000;

    private record Algorithm(String name, Mul fn, int growth) {}

    private interface Mul {
        MatrixMultiply.Result apply(long[][] a, long[][] b);
    }

    private static final List<Algorithm> ALGORITHMS = List.of(
            new Algorithm("matrix_multiply", MatrixMultiply::multiply, 8),
            new Algorithm("matrix_multiply_recursive", MatrixMultiplyRecursive::multiply, 8),
            new Algorithm("strassen", Strassen::multiply, 7),
            new Algorithm("strassen_cutoff64", (a, b) -> Strassen.multiply(a, b, 64), 7));

    public static void main(String[] args) throws IOException {
        warmUp();
        List<String> results = new ArrayList<>();
        Map<String, Double> lastMs = new HashMap<>();
        Set<String> stopped = new HashSet<>();
        for (int n = 2; Files.exists(DATA.resolve("personal_" + n + ".tsv")); n *= 2) {
            long[][][] ab = load(n);
            long[][] reference = null;
            for (Algorithm alg : ALGORITHMS) {
                if (stopped.contains(alg.name())) continue;
                double predicted = lastMs.getOrDefault(alg.name(), 0.0) * alg.growth();
                if (predicted > LIMIT_MS) {
                    System.out.printf("  n=%-4d %-26s алгассан: ~%.0f с > 60 с%n",
                            n, alg.name(), predicted / 1000);
                    stopped.add(alg.name());
                    continue;
                }
                int repeats = n <= 128 ? 3 : 1;
                double[] times = new double[repeats];
                MatrixMultiply.Result r = null;
                for (int i = 0; i < repeats; i++) {
                    long t0 = System.nanoTime();
                    r = alg.fn().apply(ab[0], ab[1]);
                    times[i] = (System.nanoTime() - t0) / 1e6;
                }
                Arrays.sort(times);
                double ms = times[repeats / 2];
                if (reference == null) reference = r.c();
                if (!Arrays.deepEquals(reference, r.c())) {
                    throw new IllegalStateException(alg.name() + ": n=" + n + " хариу таарахгүй");
                }
                results.add(n + "\t" + alg.name() + "\t" + String.format(Locale.ROOT, "%.3f", ms)
                        + "\t" + r.mults());
                lastMs.put(alg.name(), ms);
                System.out.printf("  n=%-4d %-26s %12.3f ms  mults=%d%n", n, alg.name(), ms, r.mults());
                if (ms > LIMIT_MS) stopped.add(alg.name());
            }
        }
        Files.createDirectories(OUT);
        Path path = OUT.resolve("results_java.tsv");
        Files.writeString(path, "n\talgorithm\ttime_ms\tmults\n" + String.join("\n", results) + "\n",
                StandardCharsets.UTF_8);
        System.out.println("\n  -> " + path);
    }

    /** JIT хөрвүүлэгчийг халаах: жижиг матриц дээр олон удаа ажиллуулна. */
    private static void warmUp() {
        Random rng = new Random(1);
        long[][] a = new long[32][32];
        long[][] b = new long[32][32];
        for (int i = 0; i < 32; i++) {
            for (int j = 0; j < 32; j++) {
                a[i][j] = rng.nextInt(19) - 9;
                b[i][j] = rng.nextInt(19) - 9;
            }
        }
        for (int k = 0; k < 200; k++) {
            for (Algorithm alg : ALGORITHMS) alg.fn().apply(a, b);
        }
    }

    private static long[][][] load(int n) throws IOException {
        List<String> lines = Files.readAllLines(DATA.resolve("personal_" + n + ".tsv"), StandardCharsets.UTF_8);
        if (Integer.parseInt(lines.get(0).trim()) != n) throw new IllegalStateException("n таарахгүй");
        long[][] a = new long[n][n];
        long[][] b = new long[n][n];
        for (int i = 0; i < 2 * n; i++) {
            String[] f = lines.get(i + 1).trim().split("\t");
            long[] row = i < n ? a[i] : b[i - n];
            for (int j = 0; j < n; j++) row[j] = Long.parseLong(f[j]);
        }
        return new long[][][] {a, b};
    }

    private Bench() {}
}
