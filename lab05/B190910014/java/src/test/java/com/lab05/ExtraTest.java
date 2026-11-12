package com.lab05;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;
import org.junit.jupiter.api.*;

/** Нэмэлт шалгалт: шууд аргатай тулгах, шинжилгээ ба уншлагын дүгнэлт, A төвшний хувилбарууд. */
class ExtraTest {

    private final Random rng = new Random(5);
    private static final int[] TOGROG = {1, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 20000};

    static int maxCompatible(int[] s, int[] f) {
        int n = s.length;
        int best = 0;
        for (int mask = 0; mask < 1 << n; mask++) {
            boolean ok = true;
            for (int a = 0; ok && a < n; a++) {
                for (int b = a + 1; ok && b < n; b++) {
                    if ((mask >> a & 1) == 1 && (mask >> b & 1) == 1) ok = s[a] >= f[b] || s[b] >= f[a];
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    @Test
    void activityAgainstBruteForceAndShortestFirstBound() {
        for (int t = 0; t < 300; t++) {
            int n = rng.nextInt(11);
            int[] s = new int[n];
            int[] f = new int[n];
            for (int i = 0; i < n; i++) {
                s[i] = rng.nextInt(21);
                f[i] = s[i] + 1 + rng.nextInt(8);
            }
            int opt = maxCompatible(s, f);
            assertEquals(opt, Activity.select(s, f).length);
            assertTrue(2 * Activity.shortestFirst(s, f).length >= opt);
        }
        assertArrayEquals(new int[] {2}, Activity.shortestFirst(new int[] {1, 3, 4}, new int[] {4, 5, 7}));
    }

    @Test
    void knapsackEdgeCases() {
        assertEquals(0, Knapsack.fractional(new int[0], new int[0], 10), 1e-9);
        assertEquals(13, Knapsack.fractional(new int[] {2, 3}, new int[] {4, 9}, 100), 1e-9);
        assertEquals(11, Knapsack.fractional(new int[] {0, 4}, new int[] {7, 8}, 2), 1e-9);
    }

    @Test
    void kozenZaksAndCounterexamples() {
        assertEquals(-1, Change.firstCounterexample(TOGROG));
        assertEquals(40, Change.firstCounterexample(new int[] {1, 5, 10, 20, 25, 50}));
        assertEquals(6, Change.firstCounterexample(new int[] {1, 3, 4}));
        assertEquals(48, Change.firstCounterexample(new int[] {1, 3, 6, 12, 24, 30}));
        int[] d = {1, 10, 25}; // дүн бүр өмнөхөөсөө ≥ 2 дахин их
        assertEquals(6, Arrays.stream(Change.makeChange(d, 30)).sum());
        assertEquals(3, Change.minCoins(d, 30));
        for (int x = 0; x < 500; x++) { // {1, 5, 10, 20, 50}: оновчтой шийдийн хязгаар
            int[] c = Change.makeChange(new int[] {1, 5, 10, 20, 50}, x);
            assertEquals(Change.minCoins(new int[] {1, 5, 10, 20, 50}, x), Arrays.stream(c).sum());
            assertTrue(c[0] <= 4 && c[1] <= 1 && c[2] <= 1 && c[3] <= 2 && !(c[3] == 2 && c[2] == 1));
        }
    }

    @Test
    void huffmanFastMatchesBasic() throws IOException {
        String text = Files.readString(Tsv.SHARED.resolve("mn_text.txt"), StandardCharsets.UTF_8);
        Map<String, String> codes = Huffman.build(HuffmanTest.frequencies(text));
        String bits = Huffman.encode(text, codes);
        assertEquals(bits, HuffmanFast.encode(text, codes));
        assertEquals(text, HuffmanFast.decode(bits, codes));
        for (int t = 0; t < 100; t++) {
            String alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяөү .".substring(0, 2 + rng.nextInt(36));
            StringBuilder sb = new StringBuilder();
            for (int i = 0, len = 1 + rng.nextInt(400); i < len; i++) sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
            String s = sb.toString();
            Map<String, String> c = Huffman.build(HuffmanTest.frequencies(s));
            assertEquals(s, HuffmanFast.decode(HuffmanFast.encode(s, c), c));
        }
        Map<String, String> one = Huffman.build(Map.of("x", 5L));
        assertEquals("xxx", HuffmanFast.decode(HuffmanFast.encode("xxx", one), one));
        assertThrows(IllegalArgumentException.class, () -> HuffmanFast.decode("1", Map.of("a", "0", "b", "10", "c", "11")));
        assertThrows(IllegalArgumentException.class, () -> Huffman.decode("1", Map.of("a", "0", "b", "10", "c", "11")));
    }

    static int optimalMisses(int k, int[] req, int i, Set<Integer> cache) {
        if (i == req.length) return 0;
        int p = req[i];
        if (cache.contains(p)) return optimalMisses(k, req, i + 1, cache);
        if (cache.size() < k) {
            Set<Integer> next = new HashSet<>(cache);
            next.add(p);
            return 1 + optimalMisses(k, req, i + 1, next);
        }
        int best = Integer.MAX_VALUE;
        for (int q : cache) {
            Set<Integer> next = new HashSet<>(cache);
            next.remove(q);
            next.add(p);
            best = Math.min(best, 1 + optimalMisses(k, req, i + 1, next));
        }
        return best;
    }

    @Test
    void cachingOptimalOnSmallInputsAndFastMatchesBasic() {
        for (int t = 0; t < 150; t++) {
            int k = 1 + rng.nextInt(3);
            int[] req = new int[rng.nextInt(10)];
            for (int i = 0; i < req.length; i++) req[i] = 1 + rng.nextInt(5);
            long expected = optimalMisses(k, req, 0, new HashSet<>());
            assertEquals(expected, Caching.misses(k, req));
            assertEquals(expected, CachingFast.misses(k, req));
        }
        for (Map<String, String> r : Tsv.rows("caching_01.tsv")) {
            assertEquals(Long.parseLong(r.get("furthest")),
                    CachingFast.misses(Integer.parseInt(r.get("k")), Tsv.ints(r.get("requests"))), r.get("id"));
        }
        for (int t = 0; t < 200; t++) {
            int k = rng.nextInt(9);
            int[] req = new int[rng.nextInt(301)];
            for (int i = 0; i < req.length; i++) req[i] = 1 + rng.nextInt(15);
            assertEquals(Caching.misses(k, req), CachingFast.misses(k, req));
        }
        assertArrayEquals(new int[] {2, 4, 5, 5, 5}, CachingFast.nextUse(new int[] {1, 2, 1, 3, 2}));
    }
}
