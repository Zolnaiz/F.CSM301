package com.lab02;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class RankingDistanceTest {

    @Test
    void distance() {
        for (Map<String, String> r : Tsv.rows("ranking_distance_01.tsv")) {
            assertEquals(Long.parseLong(r.get("expected")),
                    RankingDistance.distance(Tsv.ints(r.get("A")), Tsv.ints(r.get("B"))),
                    "зөрөө " + r.get("id"));
        }
    }

    @Test
    void identicalIsZero() {
        int[] a = new int[50];
        for (int i = 0; i < 50; i++) a[i] = i + 1;
        assertEquals(0, RankingDistance.distance(a, a.clone()));
    }

    @Test
    void reversedIsMaximum() {
        for (int n : new int[] {2, 5, 10, 50}) {
            int[] a = new int[n];
            int[] b = new int[n];
            for (int i = 0; i < n; i++) { a[i] = i + 1; b[i] = n - i; }
            assertEquals((long) n * (n - 1) / 2, RankingDistance.distance(a, b), "n=" + n);
        }
    }
}
