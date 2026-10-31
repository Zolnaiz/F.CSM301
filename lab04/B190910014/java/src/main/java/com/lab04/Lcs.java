package com.lab04;

import java.util.ArrayList;
import java.util.List;

public final class Lcs {

    /**
     * LCS-Length (CLRS 14.4). Хүснэгтийн зөвхөн өмнөх мөр хэрэгтэй тул хоёр мөр хадгална:
     * хугацаа Θ(mn), санах ой Θ(n).
     */
    public static int length(String x, String y) {
        int m = x.length();
        int n = y.length();
        int[] prev = new int[n + 1];
        for (int i = 1; i <= m; i++) {
            int[] curr = new int[n + 1];
            for (int j = 1; j <= n; j++) {
                curr[j] = x.charAt(i - 1) == y.charAt(j - 1)
                        ? prev[j - 1] + 1
                        : Math.max(prev[j], curr[j - 1]);
            }
            prev = curr;
        }
        return prev[n];
    }

    /**
     * Мөрийн ялгаа (diff): LCS-ийн мөрүүд « », зөвхөн A-д байгаа нь «-», зөвхөн B-д байгаа нь «+».
     * c[i][j] нь a[i..], b[j..] сүүлүүдийн LCS-ийн урт тул ялгааг эхнээс нь уншиж болно.
     * Хугацаа, санах ой Θ(mn).
     */
    public static List<String> diff(List<String> a, List<String> b) {
        int m = a.size();
        int n = b.size();
        int[][] c = new int[m + 1][n + 1];
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                c[i][j] = a.get(i).equals(b.get(j))
                        ? c[i + 1][j + 1] + 1
                        : Math.max(c[i + 1][j], c[i][j + 1]);
            }
        }
        List<String> out = new ArrayList<>();
        int i = 0;
        int j = 0;
        while (i < m && j < n) {
            if (a.get(i).equals(b.get(j))) {
                out.add(" " + a.get(i++));
                j++;
            } else if (c[i + 1][j] >= c[i][j + 1]) { // a[i]-г хасахад LCS буурахгүй
                out.add("-" + a.get(i++));
            } else {
                out.add("+" + b.get(j++));
            }
        }
        while (i < m) out.add("-" + a.get(i++));
        while (j < n) out.add("+" + b.get(j++));
        return out;
    }

    private Lcs() {}
}
