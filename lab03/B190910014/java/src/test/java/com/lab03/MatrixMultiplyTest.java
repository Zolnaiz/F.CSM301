package com.lab03;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class MatrixMultiplyTest {

    /** (a) matmul_01.tsv-ийн хариу. */
    @Test
    void product() {
        for (Map<String, String> r : Tsv.rows("matmul_01.tsv")) {
            assertArrayEquals(Tsv.matrix(r.get("expected")),
                    MatrixMultiply.multiply(Tsv.matrix(r.get("A")), Tsv.matrix(r.get("B"))).c(),
                    "n=" + r.get("n"));
        }
    }

    /** (d) скаляр үржүүлэлтийн тоо яг n³. */
    @Test
    void multsIsNCubed() {
        for (Map<String, String> r : Tsv.rows("matmul_01.tsv")) {
            long n = Long.parseLong(r.get("n"));
            assertEquals(n * n * n,
                    MatrixMultiply.multiply(Tsv.matrix(r.get("A")), Tsv.matrix(r.get("B"))).mults(),
                    "n=" + n);
        }
    }

    /** (b) C-г тэглэхгүй бол хоёр дахь дуудалтад өмнөх үр дүн нэмэгдэнэ. */
    @Test
    void secondCallGivesSameResult() {
        long[][] a = Tsv.matrix("1,2;3,4");
        long[][] b = Tsv.matrix("5,6;7,8");
        long[][] first = MatrixMultiply.multiply(a, b).c();
        long[][] second = MatrixMultiply.multiply(a, b).c();
        assertArrayEquals(Tsv.matrix("19,22;43,50"), first);
        assertArrayEquals(first, second);
    }

    /** (c) хэмжээ таарахгүй. */
    @Test
    void sizeMismatchThrows() {
        String[][] cases = {
            {"1,2;3,4", "1,2,3;4,5,6;7,8,9"},
            {"1,2,3;4,5,6", "1,2;3,4"},
            {"1,2;3,4", "1,2;3"},
        };
        for (String[] c : cases) {
            assertThrows(IllegalArgumentException.class,
                    () -> MatrixMultiply.multiply(Tsv.matrix(c[0]), Tsv.matrix(c[1])),
                    c[0] + " × " + c[1]);
        }
    }
}
