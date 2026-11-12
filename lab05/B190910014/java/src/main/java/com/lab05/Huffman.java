package com.lab05;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

/** Хаффманы код (B төвшин). */
public final class Huffman {

    /** Модны зангилаа: навч бол symbol != null. order нь ижил давтамжтай үед тогтвортой дараалал. */
    record Node(long freq, long order, String symbol, Node left, Node right) {}

    /** Бага утгын дараалал (PriorityQueue)-аар хамгийн бага давтамжтай хоёрыг нэгтгэнэ. Θ(σ lg σ). */
    public static Map<String, String> build(Map<String, Long> freq) {
        Map<String, String> codes = new HashMap<>();
        if (freq.isEmpty()) return codes;
        if (freq.size() == 1) {
            codes.put(freq.keySet().iterator().next(), "0");
            return codes;
        }
        PriorityQueue<Node> heap = new PriorityQueue<>((a, b) ->
                a.freq() != b.freq() ? Long.compare(a.freq(), b.freq()) : Long.compare(a.order(), b.order()));
        long order = 0;
        for (var e : freq.entrySet()) heap.add(new Node(e.getValue(), order++, e.getKey(), null, null));
        while (heap.size() > 1) {
            Node a = heap.poll();
            Node b = heap.poll();
            heap.add(new Node(a.freq() + b.freq(), order++, null, a, b));
        }
        Deque<Map.Entry<Node, String>> stack = new ArrayDeque<>();
        stack.push(Map.entry(heap.poll(), ""));
        while (!stack.isEmpty()) { // зүүн тийш 0, баруун тийш 1
            var top = stack.pop();
            Node node = top.getKey();
            if (node.symbol() != null) {
                codes.put(node.symbol(), top.getValue());
            } else {
                stack.push(Map.entry(node.left(), top.getValue() + "0"));
                stack.push(Map.entry(node.right(), top.getValue() + "1"));
            }
        }
        return codes;
    }

    /** Тэмдэгт (Unicode code point) бүрийг кодоор нь солино. */
    public static String encode(String text, Map<String, String> codes) {
        StringBuilder sb = new StringBuilder();
        text.codePoints().forEach(cp -> sb.append(codes.get(new String(Character.toChars(cp)))));
        return sb.toString();
    }

    /** Битийг нэг нэгээр уншиж, угтвар нь код болмогц тэмдэгт гаргана (бит бүрд мөр + толь хайлт). */
    public static String decode(String bits, Map<String, String> codes) {
        Map<String, String> reverse = new HashMap<>();
        codes.forEach((s, c) -> reverse.put(c, s));
        StringBuilder out = new StringBuilder();
        StringBuilder current = new StringBuilder();
        for (int i = 0; i < bits.length(); i++) {
            current.append(bits.charAt(i));
            String sym = reverse.get(current.toString());
            if (sym != null) {
                out.append(sym);
                current.setLength(0);
            }
        }
        if (current.length() > 0) throw new IllegalArgumentException("битийн мөр бүтэн кодоор төгсөөгүй");
        return out.toString();
    }

    private Huffman() {}
}
