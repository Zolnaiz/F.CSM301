package com.lab05;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class ChangeTest {

    @Test
    void makeChangeUsesFewestNotes() {
        for (Map<String, String> r : Tsv.rows("change_01.tsv")) {
            int[] d = Tsv.ints(r.get("d"));
            int x = Integer.parseInt(r.get("x"));
            String id = r.get("id");
            int[] counts = Change.makeChange(d, x);
            assertEquals(d.length, counts.length, id);
            long sum = 0, total = 0;
            for (int j = 0; j < d.length; j++) {
                assertTrue(counts[j] >= 0, id);
                sum += (long) counts[j] * d[j];
                total += counts[j];
            }
            assertEquals(x, sum, id);
            assertEquals(Long.parseLong(r.get("total")), total, id);
        }
    }

    @Test
    void minCoinsMatchesGreedyOnCanonicalSystems() {
        for (Map<String, String> r : Tsv.rows("change_01.tsv")) {
            assertEquals(Integer.parseInt(r.get("total")),
                    Change.minCoins(Tsv.ints(r.get("d")), Integer.parseInt(r.get("x"))), r.get("id"));
        }
    }

    @Test
    void minCoinsOnNonCanonicalSystem() {
        assertEquals(2, Change.minCoins(new int[] {1, 3, 4}, 6));
        assertEquals(2, Change.minCoins(new int[] {1, 5, 10, 20, 25, 50}, 40));
    }
}
