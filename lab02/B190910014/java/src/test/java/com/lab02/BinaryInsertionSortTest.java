package com.lab02;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class BinaryInsertionSortTest {

    @Test
    void sorts() {
        for (Map<String, String> r : Tsv.rows("sort_01.tsv")) {
            assertArrayEquals(Tsv.ints(r.get("expected")),
                    BinaryInsertionSort.sort(Tsv.ints(r.get("input"))).sorted(),
                    "эрэмбэлэлт " + r.get("id"));
        }
    }

    @Test
    void shiftCountMatchesTaskOne() {
        for (Map<String, String> r : Tsv.rows("insertion_shifts_01.tsv")) {
            assertEquals(Long.parseLong(r.get("shifts")),
                    BinaryInsertionSort.sort(Tsv.ints(r.get("input"))).shifts(),
                    "зөөлт " + r.get("id"));
        }
    }

    @Test
    void comparisonBound() {
        for (Map<String, String> r : Tsv.rows("insertion_shifts_01.tsv")) {
            int n = Integer.parseInt(r.get("n"));
            if (n < 2) continue;
            long bound = (long) n * (long) Math.ceil(Math.log(n) / Math.log(2));
            assertTrue(BinaryInsertionSort.sort(Tsv.ints(r.get("input"))).comparisons()
                            <= bound, "харьцуулалт " + r.get("id"));
        }
    }

    @Test
    void stableForEqualKeys() {
        int[] a = new int[16];
        Arrays.fill(a, 5);
        assertEquals(0, BinaryInsertionSort.sort(a).shifts());
    }

    @Test
    void agreesWithInsertionSort() {
        Random rng = new Random(2);
        for (int t = 0; t < 20; t++) {
            int[] a = new int[rng.nextInt(41)];
            for (int i = 0; i < a.length; i++) a[i] = rng.nextInt(101) - 50;
            var exp = InsertionSort.sort(a);
            var got = BinaryInsertionSort.sort(a);
            assertArrayEquals(exp.sorted(), got.sorted());
            assertEquals(exp.shifts(), got.shifts());
        }
    }
}
