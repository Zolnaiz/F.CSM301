package com.prj2;

import java.util.Arrays;

/**
 * LeetCode 455. Хомхойлох арга: эрэмбэлээд хамгийн бага шуналтай хүүхдэд түүнийг хангах хамгийн
 * жижиг жигнэмгийг өгнө. Θ(n lg n + m lg m) хугацаа, нэмэлт Θ(1) санах ой (байрандаа эрэмбэлнэ).
 */
public class AssignCookies {

    public int findContentChildren(int[] g, int[] s) {
        Arrays.sort(g);
        Arrays.sort(s);
        int child = 0;
        for (int cookie : s) {
            if (child < g.length && cookie >= g[child]) child++;
        }
        return child;
    }
}
