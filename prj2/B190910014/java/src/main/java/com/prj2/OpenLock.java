package com.prj2;

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * LeetCode 752 (B төвшин). Гүехэн хайлт: «0000»-оос эхэлж, төвшин бүрд 8 хөршийг (дугуй бүрийг
 * ±1) нэмнэ. Төлөвийг String-ээр, үзсэнийг HashSet-ээр хадгална. O(10⁴·8·4), Θ(10⁴) санах ой.
 */
public class OpenLock {

    /** Дарааллаас гаргасан төлөвийн тоо (хэмжилтэд). */
    public long expanded = 0;

    public int openLock(String[] deadends, String target) {
        Set<String> dead = new HashSet<>(Arrays.asList(deadends));
        if (dead.contains("0000")) return -1;
        if (target.equals("0000")) return 0;
        Set<String> seen = new HashSet<>();
        seen.add("0000");
        ArrayDeque<String> queue = new ArrayDeque<>();
        queue.add("0000");
        for (int dist = 1; !queue.isEmpty(); dist++) {
            for (int size = queue.size(); size > 0; size--) { // нэг төвшин
                String state = queue.poll();
                expanded++;
                char[] digits = state.toCharArray();
                for (int i = 0; i < 4; i++) {
                    char original = digits[i];
                    for (int d = -1; d <= 1; d += 2) {
                        digits[i] = (char) ('0' + (original - '0' + d + 10) % 10);
                        String next = new String(digits);
                        if (seen.contains(next) || dead.contains(next)) continue;
                        if (next.equals(target)) return dist;
                        seen.add(next);
                        queue.add(next);
                    }
                    digits[i] = original;
                }
            }
        }
        return -1;
    }
}
