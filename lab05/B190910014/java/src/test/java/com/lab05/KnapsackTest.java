package com.lab05;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class KnapsackTest {

    @Test
    void fractionalValueToTwoDecimals() {
        for (Map<String, String> r : Tsv.rows("knapsack_01.tsv")) {
            double got = Knapsack.fractional(Tsv.ints(r.get("w")), Tsv.ints(r.get("v")),
                    Integer.parseInt(r.get("W")));
            assertEquals(r.get("fractional"), String.format(Locale.ROOT, "%.2f", got), r.get("id"));
        }
    }
}
