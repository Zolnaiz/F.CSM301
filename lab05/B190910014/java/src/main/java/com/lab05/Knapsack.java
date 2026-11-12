package com.lab05;

import java.util.Arrays;

public final class Knapsack {

    /**
     * Хэсэгчилж авч болох үүргэвч: эд зүйлсийг vᵢ/wᵢ-ээр буурахаар эрэмбэлж (Θ(n lg n)),
     * багтаамж дуустал авна, сүүлийнхийг хэсэгчилнэ. Жин нь 0 эд зүйлсийг бүгдийг авна.
     */
    public static double fractional(int[] w, int[] v, int W) {
        if (w.length != v.length) throw new IllegalArgumentException("w, v ижил урттай байх ёстой");
        if (W < 0) throw new IllegalArgumentException("багтаамж сөрөг байж болохгүй");
        double total = 0;
        Integer[] order = new Integer[w.length];
        int m = 0;
        for (int i = 0; i < w.length; i++) {
            if (w[i] < 0 || v[i] < 0) throw new IllegalArgumentException("жин, үнэ сөрөг байж болохгүй");
            if (w[i] == 0) total += v[i];
            else order[m++] = i;
        }
        order = Arrays.copyOf(order, m);
        // vᵢ/wᵢ > vⱼ/wⱼ ⇔ vᵢ·wⱼ > vⱼ·wᵢ — бутархайгүйгээр (long) харьцуулна.
        Arrays.sort(order, (i, j) -> Long.compare((long) v[j] * w[i], (long) v[i] * w[j]));
        long room = W;
        for (int i : order) {
            if (room == 0) break;
            if (w[i] <= room) {
                total += v[i];
                room -= w[i];
            } else {
                total += (double) v[i] * room / w[i];
                room = 0;
            }
        }
        return total;
    }

    private Knapsack() {}
}
