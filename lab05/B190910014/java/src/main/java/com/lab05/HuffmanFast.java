package com.lab05;

import java.util.HashMap;
import java.util.Map;

/**
 * Хаффманы код — сайжруулсан кодлол ба тайлалт (A төвшин).
 * <ul>
 *   <li>encode: code point → char[] толийг нэг удаа байгуулж, тэмдэгт бүрд шинэ String
 *       үүсгэхгүй; гаралтын уртыг урьдчилан тооцож StringBuilder-ийг нэг удаа хуваарилна.</li>
 *   <li>decode: кодуудаас модыг int массивт сэргээж, бит бүрд ганц массив хандалтаар алхана
 *       (анхных бит бүрд StringBuilder.toString() + HashMap хайлт хийдэг).</li>
 * </ul>
 */
public final class HuffmanFast {

    public static Map<String, String> build(Map<String, Long> freq) {
        return Huffman.build(freq);
    }

    public static String encode(String text, Map<String, String> codes) {
        Map<Integer, char[]> byCp = new HashMap<>(2 * codes.size());
        codes.forEach((s, c) -> byCp.put(s.codePointAt(0), c.toCharArray()));
        int[] cps = text.codePoints().toArray();
        long length = 0;
        char[][] seq = new char[cps.length][];
        for (int i = 0; i < cps.length; i++) {
            seq[i] = byCp.get(cps[i]);
            length += seq[i].length;
        }
        StringBuilder sb = new StringBuilder((int) length);
        for (char[] c : seq) sb.append(c);
        return sb.toString();
    }

    public static String decode(String bits, Map<String, String> codes) {
        int maxNodes = 1;
        for (String c : codes.values()) maxNodes += c.length();
        int[] zero = new int[maxNodes];
        int[] one = new int[maxNodes];
        String[] symbol = new String[maxNodes];
        int nodes = 1;
        for (var e : codes.entrySet()) { // мод: зүүн 0, баруун 1
            int v = 0;
            for (int i = 0; i < e.getValue().length(); i++) {
                int[] child = e.getValue().charAt(i) == '0' ? zero : one;
                if (child[v] == 0) child[v] = nodes++;
                v = child[v];
            }
            symbol[v] = e.getKey();
        }
        StringBuilder out = new StringBuilder();
        int v = 0;
        for (int i = 0; i < bits.length(); i++) {
            v = bits.charAt(i) == '0' ? zero[v] : one[v];
            if (v == 0) throw new IllegalArgumentException("буруу бит");
            if (symbol[v] != null) {
                out.append(symbol[v]);
                v = 0;
            }
        }
        if (v != 0) throw new IllegalArgumentException("битийн мөр бүтэн кодоор төгсөөгүй");
        return out.toString();
    }

    private HuffmanFast() {}
}
