package com.lab03;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class MatrixVectorTest {

    @Test
    void matrixVector() {
        for (Map<String, String> r : Tsv.rows("matvec_01.tsv")) {
            MatrixVector.Result res = MatrixVector.matrixVector(Tsv.matrix(r.get("A")), Tsv.vector(r.get("x")));
            long n = Long.parseLong(r.get("n"));
            assertArrayEquals(Tsv.vector(r.get("expected")), res.y(), r.get("id"));
            assertEquals(Long.parseLong(r.get("ops")), res.ops(), r.get("id"));
            assertEquals(2 * n * n, res.ops(), r.get("id"));
        }
    }

    @Test
    void hadamard() {
        MatrixVector.Result res = MatrixVector.hadamard(new long[] {1, -2, 3, 4}, new long[] {5, 6, -7, 0});
        assertArrayEquals(new long[] {5, -12, -21, 0}, res.y());
        assertEquals(4, res.ops());
    }

    @Test
    void badSizeThrows() {
        assertThrows(IllegalArgumentException.class,
                () -> MatrixVector.matrixVector(Tsv.matrix("1,2;3,4"), Tsv.vector("1,2,3")));
        assertThrows(IllegalArgumentException.class,
                () -> MatrixVector.hadamard(new long[] {1, 2}, new long[] {1}));
    }
}
