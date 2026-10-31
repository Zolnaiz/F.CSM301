package com.lab03;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class StrassenTest {

    /** n = 512-оос дээш нь удаан тул тоог бодитоор ажиллуулж шалгахгүй. */
    private static final int RUN_LIMIT = 256;

    /** (a) хариу 2, 3-р даалгавартай ижил. */
    @Test
    void product() {
        for (Map<String, String> r : Tsv.rows("matmul_01.tsv")) {
            assertArrayEquals(Tsv.matrix(r.get("expected")),
                    Strassen.multiply(Tsv.matrix(r.get("A")), Tsv.matrix(r.get("B"))).c(),
                    "n=" + r.get("n"));
        }
    }

    @Test
    void randomMatchesIterative() {
        Random rng = new Random(7);
        for (int n : new int[] {16, 32, 64}) {
            long[][] a = new long[n][n];
            long[][] b = new long[n][n];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    a[i][j] = rng.nextInt(19) - 9;
                    b[i][j] = rng.nextInt(19) - 9;
                }
            }
            assertArrayEquals(MatrixMultiply.multiply(a, b).c(), Strassen.multiply(a, b).c(), "n=" + n);
        }
    }

    /** (b) үржүүлэлтийн тоо яг 7^lg n = n^lg 7. */
    @Test
    void multCount() {
        for (Map<String, String> r : Tsv.rows("strassen_counts_01.tsv")) {
            int n = Integer.parseInt(r.get("n"));
            long expected = Long.parseLong(r.get("strassen_mults"));
            int lg = Integer.numberOfTrailingZeros(n);
            assertEquals((long) Math.pow(7, lg), expected, "n=" + n);
            assertEquals((long) n * n * n, Long.parseLong(r.get("naive_mults")), "n=" + n);
            if (n > RUN_LIMIT) continue;
            long[][] zero = new long[n][n];
            assertEquals(expected, Strassen.multiply(zero, zero).mults(), "n=" + n);
        }
    }

    /** Сайжруулсан хувилбар: хариу ижил, үржүүлэлт 7^lg(n/c) · c³. */
    @Test
    void cutoffMatchesIterative() {
        Random rng = new Random(11);
        int n = 128;
        long[][] a = new long[n][n];
        long[][] b = new long[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                a[i][j] = rng.nextInt(19) - 9;
                b[i][j] = rng.nextInt(19) - 9;
            }
        }
        long[][] expected = MatrixMultiply.multiply(a, b).c();
        for (int cutoff : new int[] {1, 16, 64, 128}) {
            MatrixMultiply.Result r = Strassen.multiply(a, b, cutoff);
            assertArrayEquals(expected, r.c(), "cutoff=" + cutoff);
            int levels = Integer.numberOfTrailingZeros(n / cutoff);
            long c3 = (long) cutoff * cutoff * cutoff;
            assertEquals((long) Math.pow(7, levels) * c3, r.mults(), "cutoff=" + cutoff);
        }
    }

    @Test
    void badSizeThrows() {
        assertThrows(IllegalArgumentException.class, () -> Strassen.multiply(
                Tsv.matrix("1,2,3;4,5,6;7,8,9"), Tsv.matrix("1,2,3;4,5,6;7,8,9")));
    }
}
