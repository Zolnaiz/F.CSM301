package com.lab05;

import java.util.Arrays;

public final class Change {

    /** Кассчны (хомхойлох) арга: хамгийн их дүнгээс эхлэн аль болох олныг авна. Θ(m). */
    public static int[] makeChange(int[] d, int x) {
        boolean ok = d.length > 0 && d[0] == 1;
        for (int j = 1; ok && j < d.length; j++) ok = d[j - 1] < d[j];
        if (!ok) throw new IllegalArgumentException("d нь 1-ээс эхэлсэн өсөх дараалал байх ёстой");
        if (x < 0) throw new IllegalArgumentException("x сөрөг байж болохгүй");
        int[] counts = new int[d.length];
        for (int j = d.length - 1; j >= 0; j--) {
            counts[j] = x / d[j];
            x %= d[j];
        }
        return counts;
    }

    /** Уншлага (а): хамгийн цөөн дэвсгэрт — динамик программчлал, Θ(m·x) хугацаа, Θ(x) санах ой. */
    public static int minCoins(int[] d, int x) {
        if (x < 0) throw new IllegalArgumentException("x сөрөг байж болохгүй");
        int[] best = table(d, x);
        if (best[x] > x) throw new IllegalArgumentException(x + "-ийг бүрдүүлэх боломжгүй");
        return best[x];
    }

    /** best[y] = 1 + min(best[y − dⱼ]), y = 0…limit. */
    public static int[] table(int[] d, int limit) {
        int[] coins = d.clone();
        Arrays.sort(coins);
        int[] best = new int[limit + 1];
        for (int y = 1; y <= limit; y++) {
            int b = limit + 1;
            for (int c : coins) {
                if (c > y) break;
                b = Math.min(b, best[y - c] + 1);
            }
            best[y] = b;
        }
        return best;
    }

    /** Козен–Заксын теорем: c₃ < x < c_(m−1) + c_m мужид хомхойлох арга оновчгүй хамгийн бага x, эсвэл −1. */
    public static int firstCounterexample(int[] d) {
        if (d.length < 3) return -1;
        int hi = d[d.length - 2] + d[d.length - 1];
        int[] best = table(d, hi);
        for (int x = d[2] + 1; x < hi; x++) {
            int greedy = 0;
            for (int c : makeChange(d, x)) greedy += c;
            if (greedy != best[x]) return x;
        }
        return -1;
    }

    private Change() {}
}
