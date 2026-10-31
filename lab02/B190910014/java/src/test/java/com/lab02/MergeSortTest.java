package com.lab02;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class MergeSortTest {

    @Test
    void sorts() {
        for (Map<String, String> r : Tsv.rows("sort_01.tsv")) {
            assertArrayEquals(Tsv.ints(r.get("expected")),
                    MergeSort.sort(Tsv.ints(r.get("input"))).sorted(),
                    "эрэмбэлэлт " + r.get("id"));
        }
    }

    @Test
    void writeCount() {
        for (Map<String, String> r : Tsv.rows("merge_writes_01.tsv")) {
            assertEquals(Long.parseLong(r.get("writes")),
                    MergeSort.sort(Tsv.ints(r.get("input"))).writes(),
                    "бичилт " + r.get("id"));
        }
    }

    @Test
    void powerOfTwoIsNLgN() {
        for (int k = 1; k <= 10; k++) {
            int n = 1 << k;
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = n - i;
            assertEquals((long) n * k, MergeSort.sort(a).writes(), "k=" + k);
        }
    }

    @Test
    void writeCountIndependentOfContent() {
        long w1 = MergeSort.sort(new int[] {1, 2, 3, 4, 5, 6, 7, 8}).writes();
        long w2 = MergeSort.sort(new int[] {8, 7, 6, 5, 4, 3, 2, 1}).writes();
        long w3 = MergeSort.sort(new int[] {3, 1, 4, 1, 5, 9, 2, 6}).writes();
        assertEquals(w1, w2);
        assertEquals(w1, w3);
    }
}
