package com.prj1;

/**
 * LeetCode 1763. Хэсэгчлэх арга: эсрэг томын хэлбэр нь мөрөнд байхгүй «муу» үсгүүдээр нэг дор
 * хуваана. Хэсэг бүрээс дор хаяж нэг үсгийн төрөл алга болдог тул гүн ≤ 52, нийт Θ(n).
 */
public class LongestNiceSubstring {

    public String longestNiceSubstring(String s) {
        return solve(s, 0, s.length());
    }

    /** s[lo, hi) дахь хамгийн урт сайхан дэд мөр. */
    private String solve(String s, int lo, int hi) {
        if (hi - lo < 2) return "";
        boolean[] present = new boolean[128];
        for (int i = lo; i < hi; i++) present[s.charAt(i)] = true;

        String best = "";
        int start = lo;
        boolean split = false;
        for (int i = lo; i < hi; i++) {
            if (!present[swapCase(s.charAt(i))]) { // муу үсэг
                split = true;
                String part = solve(s, start, i);
                if (part.length() > best.length()) best = part; // тэнцүү бол эхнийх
                start = i + 1;
            }
        }
        if (!split) return s.substring(lo, hi);
        String part = solve(s, start, hi);
        return part.length() > best.length() ? part : best;
    }

    private static char swapCase(char c) {
        return Character.isUpperCase(c) ? Character.toLowerCase(c) : Character.toUpperCase(c);
    }
}
