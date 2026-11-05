package com.lab03;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

/** A түвшин: fib_matrix, сайжруулсан Гаусс, Якобийн арга, cutoff-той Штрассен. */
class ALevelTest {

    @Test
    void fibMatrixMatchesBottomUp() {
        long a = 0;
        long b = 1; // F(0), F(1)
        for (int n = 0; n <= 1000; n++) {
            FibMatrix.Result r = FibMatrix.fib(n);
            assertEquals(a, r.value(), "n=" + n);
            if (n >= 1) {
                long expected = 8L * (64 - Long.numberOfLeadingZeros(n) + Long.bitCount(n));
                assertEquals(expected, r.mults(), "n=" + n);
            }
            long next = (a + b) % FibMatrix.MOD;
            a = b;
            b = next;
        }
        assertThrows(IllegalArgumentException.class, () -> FibMatrix.fib(-1));
    }

    @Test
    void gaussFastSolutionAndOps() {
        for (Map<String, String> r : Tsv.rows("gauss_01.tsv")) {
            GaussSolve.Result res = GaussSolve.solveFast(Tsv.matrix(r.get("A")), Tsv.vector(r.get("b")));
            long[] expected = Tsv.vector(r.get("x"));
            for (int i = 0; i < expected.length; i++) assertEquals(expected[i], res.x()[i], 1e-9, r.get("id"));
            long n = Long.parseLong(r.get("n"));
            assertEquals(GaussSolve.fastOps(n), res.ops(), r.get("id"));
            assertEquals(GaussSolve.ops(n) - n * (n - 1), res.ops(), r.get("id"));
        }
    }

    @Test
    void jacobiSolutionAndOps() {
        for (Map<String, String> r : Tsv.rows("gauss_01.tsv")) {
            GaussSolve.JacobiResult res = GaussSolve.solveJacobi(Tsv.matrix(r.get("A")), Tsv.vector(r.get("b")));
            long[] expected = Tsv.vector(r.get("x"));
            for (int i = 0; i < expected.length; i++) assertEquals(expected[i], res.x()[i], 1e-9, r.get("id"));
            long n = Long.parseLong(r.get("n"));
            assertTrue(res.iterations() >= 1 && res.iterations() < 1000, r.get("id"));
            assertEquals(2L * res.iterations() * n * n, res.ops(), r.get("id"));
        }
    }

    @Test
    void jacobiMatchesGaussOnRandomSystems() {
        Random rng = new Random(7);
        for (int n : new int[] {1, 3, 20, 100, 200}) {
            long[][] a = new long[n][n];
            long[] b = new long[n];
            for (int i = 0; i < n; i++) {
                long off = 0;
                for (int j = 0; j < n; j++) {
                    a[i][j] = rng.nextInt(19) - 9;
                    if (j != i) off += Math.abs(a[i][j]);
                }
                a[i][i] = off + 1;
                b[i] = rng.nextInt(101) - 50;
            }
            double[] g = GaussSolve.solve(a, b).x();
            double[] j = GaussSolve.solveJacobi(a, b).x();
            for (int i = 0; i < n; i++) assertEquals(g[i], j[i], 1e-9 * Math.max(1, Math.abs(g[i])), "n=" + n);
        }
        assertEquals(0, GaussSolve.solveJacobi(new long[0][0], new long[0]).iterations());
        assertThrows(IllegalArgumentException.class,
                () -> GaussSolve.solveJacobi(new long[][] {{1, 2}, {3, 4}}, new long[] {1, 2}));
    }

    @Test
    void strassenCutoffMatches() {
        Random rng = new Random(12);
        for (int n : new int[] {16, 64}) {
            long[][] a = new long[n][n];
            long[][] b = new long[n][n];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    a[i][j] = rng.nextInt(19) - 9;
                    b[i][j] = rng.nextInt(19) - 9;
                }
            }
            long[][] expected = MatrixMultiply.multiply(a, b).c();
            for (int cutoff : new int[] {2, 8, 32}) {
                assertArrayEquals(expected, Strassen.multiply(a, b, cutoff).c(), "n=" + n + " cutoff=" + cutoff);
            }
        }
    }
}
