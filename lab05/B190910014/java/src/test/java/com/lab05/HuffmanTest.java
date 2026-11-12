package com.lab05;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class HuffmanTest {

    static long optimalBits(Collection<Long> freqs) {
        if (freqs.size() == 1) return freqs.iterator().next();
        PriorityQueue<Long> h = new PriorityQueue<>(freqs);
        long total = 0;
        while (h.size() > 1) {
            long a = h.poll(), b = h.poll();
            total += a + b;
            h.add(a + b);
        }
        return total;
    }

    static void checkCodes(Map<String, String> codes, Set<String> symbols, String label) {
        assertEquals(symbols, codes.keySet(), label);
        List<String> cs = new ArrayList<>(codes.values());
        for (String c : cs) assertTrue(!c.isEmpty() && c.matches("[01]+"), label + ": " + c);
        Collections.sort(cs);
        for (int i = 0; i + 1 < cs.size(); i++) {
            assertFalse(cs.get(i + 1).startsWith(cs.get(i)),
                    label + ": " + cs.get(i) + " нь " + cs.get(i + 1) + "-ийн угтвар");
        }
    }

    static Map<String, Long> frequencies(String text) {
        Map<String, Long> freq = new HashMap<>();
        text.codePoints().forEach(cp -> freq.merge(new String(Character.toChars(cp)), 1L, Long::sum));
        return freq;
    }

    @Test
    void tableCodesAreOptimalPrefixCodes() {
        for (Map<String, String> r : Tsv.rows("huffman_01.tsv")) {
            String id = r.get("id");
            List<String> symbols = Tsv.strs(r.get("symbols"));
            int[] freqs = Tsv.ints(r.get("freqs"));
            Map<String, Long> freq = new LinkedHashMap<>();
            StringBuilder text = new StringBuilder();
            for (int i = 0; i < freqs.length; i++) {
                freq.put(symbols.get(i), (long) freqs[i]);
                text.append(symbols.get(i).repeat(freqs[i]));
            }
            Map<String, String> codes = Huffman.build(freq);
            checkCodes(codes, freq.keySet(), id);
            long bitsTotal = 0;
            for (var e : freq.entrySet()) bitsTotal += e.getValue() * codes.get(e.getKey()).length();
            assertEquals(Long.parseLong(r.get("total_bits")), bitsTotal, id);

            String bits = Huffman.encode(text.toString(), codes);
            assertEquals(Long.parseLong(r.get("total_bits")), bits.length(), id);
            assertEquals(text.toString(), Huffman.decode(bits, codes), id);
        }
    }

    @Test
    void mongolianTextRoundTrip() throws IOException {
        String text = Files.readString(Tsv.SHARED.resolve("mn_text.txt"), StandardCharsets.UTF_8);
        Map<String, Long> freq = frequencies(text);
        Map<String, String> codes = Huffman.build(freq);
        checkCodes(codes, freq.keySet(), "mn_text");
        String bits = Huffman.encode(text, codes);
        assertEquals(optimalBits(freq.values()), bits.length());
        assertEquals(text, Huffman.decode(bits, codes));
    }
}
