package com.lab03;

import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.function.Supplier;

/**
 * A түвшин: Штрассен (цэвэр ба cutoff) ба Гаусс (анхны ба сайжруулсан), мөн 1–5-р бодлого ба
 * fib_matrix — хувийн өгөгдөл дээр хугацаа (ms, ≥ 50 ms багцын 7 хэмжилтийн медиан) ба нэг
 * дуудалтад хуваарилсан санах ой (KB, ThreadMXBean). lab03/<Student-ID>/java-аас:
 *   javac -d build src/main/java/com/lab03/*.java
 *   java -cp build com.lab03.BenchA [strassen] [gauss] [problems]   -> ../out/a_<хэсэг>_java.tsv
 */
public final class BenchA {

    private static final Path STUDENT_DIR = Paths.get("..").toAbsolutePath().normalize();
    private static final com.sun.management.ThreadMXBean THREADS =
            (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();

    private record Case(String name, long n, Supplier<Object> fn) {}

    private static String measure(Case c) {
        System.gc();
        int iters = 1;
        while (true) { // багцын хэмжээг тогтоох нь JIT-ийг бас халаана
            long t0 = System.nanoTime();
            for (int i = 0; i < iters; i++) c.fn().get();
            if (System.nanoTime() - t0 >= 50_000_000L || iters >= 1 << 14) break;
            iters *= 2;
        }
        long tid = Thread.currentThread().getId();
        double[] times = new double[7];
        long allocated = 0;
        for (int r = 0; r < times.length; r++) {
            long a0 = THREADS.getThreadAllocatedBytes(tid);
            long t0 = System.nanoTime();
            for (int i = 0; i < iters; i++) c.fn().get();
            times[r] = (System.nanoTime() - t0) / 1e6 / iters;
            allocated = (THREADS.getThreadAllocatedBytes(tid) - a0) / iters;
        }
        Arrays.sort(times);
        double ms = times[times.length / 2];
        double kb = allocated / 1024.0;
        System.out.printf("  %-28s n=%-4d %12.3f ms %12.1f KB%n", c.name(), c.n(), ms, kb);
        return String.join("\t", c.name(), String.valueOf(c.n()),
                String.format(Locale.ROOT, "%.3f", ms), String.format(Locale.ROOT, "%.1f", kb));
    }

    private static long[][][] load(int n) throws IOException {
        List<String> lines = Files.readAllLines(STUDENT_DIR.resolve("test_data").resolve("personal_" + n + ".tsv"),
                StandardCharsets.UTF_8);
        long[][] a = new long[n][n];
        long[][] b = new long[n][n];
        for (int i = 0; i < 2 * n; i++) {
            String[] f = lines.get(i + 1).trim().split("\t");
            long[] row = i < n ? a[i] : b[i - n];
            for (int j = 0; j < n; j++) row[j] = Long.parseLong(f[j]);
        }
        return new long[][][] {a, b};
    }

    /** Хувийн A-г диагональ давамгай болгож, x = B-ийн эхний багана байх (A, b = Ax)-ийг буцаана. */
    private static Object[] system(int n) throws IOException {
        long[][][] ab = load(n);
        long[][] a = ab[0];
        for (int i = 0; i < n; i++) {
            long off = 0;
            for (int j = 0; j < n; j++) if (j != i) off += Math.abs(a[i][j]);
            a[i][i] = off + 1;
        }
        long[] x = new long[n];
        for (int i = 0; i < n; i++) x[i] = ab[1][i][0];
        return new Object[] {a, MatrixVector.matrixVector(a, x).y()};
    }

    private static List<Case> cases(String section) throws IOException {
        List<Case> cs = new ArrayList<>();
        switch (section) {
            case "strassen" -> {
                for (int n : new int[] {64, 128, 256, 512}) {
                    long[][][] ab = load(n);
                    cs.add(new Case("naive", n, () -> MatrixMultiply.multiply(ab[0], ab[1])));
                    cs.add(new Case("pure", n, () -> Strassen.multiply(ab[0], ab[1])));
                    cs.add(new Case("cutoff32", n, () -> Strassen.multiply(ab[0], ab[1], 32)));
                    cs.add(new Case("cutoff64", n, () -> Strassen.multiply(ab[0], ab[1], 64)));
                }
            }
            case "gauss" -> {
                for (int n : new int[] {64, 128, 256, 512}) {
                    Object[] s = system(n);
                    long[][] a = (long[][]) s[0];
                    long[] rhs = (long[]) s[1];
                    cs.add(new Case("basic", n, () -> GaussSolve.solve(a, rhs)));
                    cs.add(new Case("fast", n, () -> GaussSolve.solveFast(a, rhs)));
                    cs.add(new Case("jacobi", n, () -> GaussSolve.solveJacobi(a, rhs)));
                }
            }
            case "problems" -> {
                int n = 128;
                long[][][] ab = load(n);
                long[] x = new long[n];
                for (int i = 0; i < n; i++) x[i] = ab[1][i][0];
                Object[] s = system(n);
                cs.add(new Case("1 matrix_multiply", n, () -> MatrixMultiply.multiply(ab[0], ab[1])));
                cs.add(new Case("2 matrix_multiply_recursive", n, () -> MatrixMultiplyRecursive.multiply(ab[0], ab[1])));
                cs.add(new Case("3 matrix_vector", n, () -> MatrixVector.matrixVector(ab[0], x)));
                cs.add(new Case("4 strassen", n, () -> Strassen.multiply(ab[0], ab[1])));
                cs.add(new Case("5 gauss_solve", n, () -> GaussSolve.solve((long[][]) s[0], (long[]) s[1])));
                cs.add(new Case("fib_matrix", 1_000_000_000_000_000_000L, () -> FibMatrix.fib(1_000_000_000_000_000_000L)));
            }
            default -> throw new IllegalArgumentException("хэсэг: strassen, gauss, problems");
        }
        return cs;
    }

    public static void main(String[] args) throws IOException {
        String[] sections = args.length > 0 ? args : new String[] {"strassen", "gauss", "problems"};
        for (String section : sections) {
            List<String> rows = new ArrayList<>();
            for (Case c : cases(section)) rows.add(measure(c));
            Path path = STUDENT_DIR.resolve("out").resolve("a_" + section + "_java.tsv");
            Files.createDirectories(path.getParent());
            Files.writeString(path, "variant\tn\ttime_ms\talloc_kb\n" + String.join("\n", rows) + "\n",
                    StandardCharsets.UTF_8);
            System.out.println("  -> " + path + "\n");
        }
    }

    private BenchA() {}
}
