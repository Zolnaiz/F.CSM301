package com.lab05;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class ActivityTest {

    @Test
    void selectsMaximumCompatibleSet() {
        for (Map<String, String> r : Tsv.rows("activity_01.tsv")) {
            int[] s = Tsv.ints(r.get("s"));
            int[] f = Tsv.ints(r.get("f"));
            int n = Integer.parseInt(r.get("n"));
            String id = r.get("id");
            int[] chosen = Activity.select(s, f);

            Set<Integer> seen = new HashSet<>();
            for (int i : chosen) {
                assertTrue(i >= 1 && i <= n, id);
                assertTrue(seen.add(i), id);
            }
            for (int a : chosen) {
                for (int b : chosen) {
                    if (a < b) {
                        assertTrue(s[a - 1] >= f[b - 1] || s[b - 1] >= f[a - 1],
                                id + ": " + a + ", " + b + " давхцаж байна");
                    }
                }
            }
            assertEquals(Integer.parseInt(r.get("expected_count")), chosen.length, id);
        }
    }
}
