package com.lab05;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public final class Activity {

    /**
     * Хамгийн эрт дуусах ажиллагааг сонгох хомхойлох арга. Дуусах хугацаагаар эрэмбэлээд
     * (Θ(n lg n)), өмнө сонгосных дуусахаас хойш эхэлсэн эхнийхийг авна. Интервал [s, f).
     * Сонгосон ажиллагааны 1-ээс эхэлсэн дугаарыг буцаана.
     */
    public static int[] select(int[] s, int[] f) {
        if (s.length != f.length) throw new IllegalArgumentException("s, f ижил урттай байх ёстой");
        Integer[] order = new Integer[s.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, Comparator.comparingInt(i -> f[i]));
        List<Integer> chosen = new ArrayList<>();
        long lastFinish = Long.MIN_VALUE;
        for (int i : order) {
            if (s[i] >= lastFinish) {
                chosen.add(i + 1);
                lastFinish = f[i];
            }
        }
        return chosen.stream().mapToInt(Integer::intValue).toArray();
    }

    /** Шинжилгээ (б), (в): хамгийн богино ажиллагааг түрүүлж сонгох (оновчгүй) дүрэм. */
    public static int[] shortestFirst(int[] s, int[] f) {
        Integer[] order = new Integer[s.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, Comparator.comparingInt(i -> f[i] - s[i]));
        List<Integer> chosen = new ArrayList<>();
        for (int i : order) {
            boolean ok = true;
            for (int j : chosen) ok &= s[i] >= f[j - 1] || s[j - 1] >= f[i];
            if (ok) chosen.add(i + 1);
        }
        return chosen.stream().mapToInt(Integer::intValue).toArray();
    }

    private Activity() {}
}
