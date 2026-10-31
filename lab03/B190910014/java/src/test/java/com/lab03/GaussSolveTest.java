package com.lab03;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class GaussSolveTest {

    /** (b) gauss_01.tsv: шийд ба үйлдлийн тоо. */
    @Test
    void solutionAndOps() {
        for (Map<String, String> r : Tsv.rows("gauss_01.tsv")) {
            GaussSolve.Result res = GaussSolve.solve(Tsv.matrix(r.get("A")), Tsv.vector(r.get("b")));
            long[] expected = Tsv.vector(r.get("x"));
            for (int i = 0; i < expected.length; i++) {
                assertEquals(expected[i], res.x()[i], 1e-9, r.get("id") + " x" + i);
            }
            assertEquals(Long.parseLong(r.get("ops")), res.ops(), r.get("id"));
            assertEquals(GaussSolve.ops(Long.parseLong(r.get("n"))), res.ops(), r.get("id"));
        }
    }

    /** (b) n = 10, 50, 100, 200 үед үйлдлийн тоо ⅔n³ уруу дөхнө. */
    @Test
    void opsApproachTwoThirdsNCubed() {
        double previous = Double.MAX_VALUE;
        for (int n : new int[] {10, 50, 100, 200}) {
            Random rng = new Random(n);
            long[][] a = new long[n][n];
            long[] xTrue = new long[n];
            for (int i = 0; i < n; i++) {
                long off = 0;
                for (int j = 0; j < n; j++) {
                    a[i][j] = rng.nextInt(19) - 9;
                    if (j != i) off += Math.abs(a[i][j]);
                }
                a[i][i] = off + 1 + rng.nextInt(9);
                xTrue[i] = rng.nextInt(11) - 5;
            }
            long[] b = MatrixVector.matrixVector(a, xTrue).y();
            GaussSolve.Result res = GaussSolve.solve(a, b);
            for (int i = 0; i < n; i++) assertEquals(xTrue[i], res.x()[i], 1e-6, "n=" + n);
            assertEquals(GaussSolve.ops(n), res.ops(), "n=" + n);
            double ratio = res.ops() / (2.0 * n * n * n / 3);
            assertTrue(ratio < previous, "n=" + n);
            previous = ratio;
        }
        assertTrue(previous < 1.02);
    }

    @Test
    void badSizeThrows() {
        assertThrows(IllegalArgumentException.class,
                () -> GaussSolve.solve(Tsv.matrix("1,2;3,4"), Tsv.vector("1,2,3")));
    }
}
