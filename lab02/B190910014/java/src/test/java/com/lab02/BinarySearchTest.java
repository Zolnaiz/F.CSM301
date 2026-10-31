package com.lab02;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class BinarySearchTest {

    @Test
    void index() {
        for (Map<String, String> r : Tsv.rows("binary_search_01.tsv")) {
            assertEquals(Integer.parseInt(r.get("index0")),
                    BinarySearch.search(Tsv.ints(r.get("A")),
                            Integer.parseInt(r.get("x"))).index(),
                    "индекс " + r.get("id"));
        }
    }

    @Test
    void callCount() {
        for (Map<String, String> r : Tsv.rows("binary_search_01.tsv")) {
            assertEquals(Long.parseLong(r.get("calls")),
                    BinarySearch.search(Tsv.ints(r.get("A")),
                            Integer.parseInt(r.get("x"))).calls(),
                    "дуудалт " + r.get("id"));
        }
    }

    @Test
    void callCountWithinBound() {
        for (Map<String, String> r : Tsv.rows("binary_search_01.tsv")) {
            int n = Integer.parseInt(r.get("n"));
            long bound = (long) Math.floor(Math.log(n) / Math.log(2)) + 2;
            assertTrue(BinarySearch.search(Tsv.ints(r.get("A")),
                            Integer.parseInt(r.get("x"))).calls() <= bound,
                    "хязгаар " + r.get("id"));
        }
    }
}
