package com.lab03;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class MatrixMultiplyRecursiveTest {

    /** (a) хариу болон үржүүлэлтийн тоо 2-р даалгавартай яг ижил. */
    @Test
    void sameAsIterative() {
        for (Map<String, String> r : Tsv.rows("matmul_01.tsv")) {
            long[][] a = Tsv.matrix(r.get("A"));
            long[][] b = Tsv.matrix(r.get("B"));
            MatrixMultiply.Result got = MatrixMultiplyRecursive.multiply(a, b);
            MatrixMultiply.Result exp = MatrixMultiply.multiply(a, b);
            assertArrayEquals(Tsv.matrix(r.get("expected")), got.c(), "n=" + r.get("n"));
            assertEquals(exp.mults(), got.mults(), "n=" + r.get("n"));
        }
    }

    @Test
    void random16x16And32x32() {
        Random rng = new Random(3);
        for (int n : new int[] {16, 32}) {
            long[][] a = new long[n][n];
            long[][] b = new long[n][n];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    a[i][j] = rng.nextInt(19) - 9;
                    b[i][j] = rng.nextInt(19) - 9;
                }
            }
            assertArrayEquals(MatrixMultiply.multiply(a, b).c(),
                    MatrixMultiplyRecursive.multiply(a, b).c(), "n=" + n);
        }
    }

    /** Хэмжээ таарахгүй эсвэл n нь 2-ын зэрэг биш. */
    @Test
    void badSizeThrows() {
        assertThrows(IllegalArgumentException.class, () -> MatrixMultiplyRecursive.multiply(
                Tsv.matrix("1,2;3,4"), Tsv.matrix("1,2,3;4,5,6;7,8,9")));
        assertThrows(IllegalArgumentException.class, () -> MatrixMultiplyRecursive.multiply(
                Tsv.matrix("1,2,3;4,5,6;7,8,9"), Tsv.matrix("1,2,3;4,5,6;7,8,9")));
    }
}
