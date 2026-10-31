package com.lab02;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class InsertionSortTest {

    @Test
    void sorts() {
        for (Map<String, String> r : Tsv.rows("sort_01.tsv")) {
            assertArrayEquals(Tsv.ints(r.get("expected")),
                    InsertionSort.sort(Tsv.ints(r.get("input"))).sorted(),
                    "эрэмбэлэлт " + r.get("id"));
        }
    }

    @Test
    void shiftCount() {
        for (Map<String, String> r : Tsv.rows("insertion_shifts_01.tsv")) {
            assertEquals(Long.parseLong(r.get("shifts")),
                    InsertionSort.sort(Tsv.ints(r.get("input"))).shifts(),
                    "зөөлт " + r.get("id"));
        }
    }

    @Test
    void reverseSortedIsNChooseTwo() {
        for (int n : new int[] {4, 8, 16, 64}) {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = n - i;
            assertEquals((long) n * (n - 1) / 2, InsertionSort.sort(a).shifts(), "n=" + n);
        }
    }

    @Test
    void alreadySortedNeedsNoShift() {
        int[] a = new int[32];
        for (int i = 0; i < 32; i++) a[i] = i + 1;
        assertEquals(0, InsertionSort.sort(a).shifts());
    }
}
