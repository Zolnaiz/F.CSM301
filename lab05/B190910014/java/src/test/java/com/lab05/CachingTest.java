package com.lab05;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

class CachingTest {

    @Test
    void furthestInFutureMissCount() {
        for (Map<String, String> r : Tsv.rows("caching_01.tsv")) {
            long got = Caching.misses(Integer.parseInt(r.get("k")), Tsv.ints(r.get("requests")));
            assertEquals(Long.parseLong(r.get("furthest")), got, r.get("id"));
        }
    }
}
