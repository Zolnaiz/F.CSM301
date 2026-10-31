package com.lab04;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class CutRodTest {

    @Test
    void revenueAndLoopCount() {
        for (Map<String, String> r : Tsv.rows("rod_01.tsv")) {
            CutRod.Result res = CutRod.bottomUp(Tsv.ints(r.get("p")));
            assertEquals(Long.parseLong(r.get("expected_revenue")), res.revenue(), r.get("id"));
            assertEquals(Long.parseLong(r.get("expected_loop_count")), res.innerLoopCount(),
                    r.get("id"));
        }
    }

    @Test
    void innerLoopCountMatchesNTimesNPlusOneOverTwo() {
        for (int n : new int[] {1, 2, 3, 5, 10}) {
            int[] p = new int[n];
            Arrays.fill(p, 1);
            long expected = (long) n * (n + 1) / 2;
            assertEquals(expected, CutRod.bottomUp(p).innerLoopCount(), "n=" + n);
        }
    }

    @Test
    void cutsAreAValidOptimalPartition() {
        for (Map<String, String> r : Tsv.rows("rod_cuts_01.tsv")) {
            int[] p = Tsv.ints(r.get("p"));
            int n = Integer.parseInt(r.get("n"));
            long expectedRevenue = Long.parseLong(r.get("expected_revenue"));
            CutRod.ExtendedResult res = CutRod.extended(p);

            int sum = 0;
            long priceSum = 0;
            for (int c : res.cuts()) {
                assertTrue(c >= 1 && c <= n, r.get("id"));
                sum += c;
                priceSum += p[c - 1];
            }
            assertEquals(n, sum, r.get("id"));
            assertEquals(expectedRevenue, priceSum, r.get("id"));
            assertEquals(expectedRevenue, res.revenue(), r.get("id"));
        }
    }
}
