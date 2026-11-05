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

    /**
     * Сайжруулсан diff: Myers-ийн O((N+M)·D) алгоритм (git diff-ийн үндсэн арга). v[k] нь d алхмаар
     * k = x − y диагональ дээр хүрэх хамгийн хол x. D = N + M − 2·LCS тул ерөнхий мөрийн тоо
     * diff()-тэй ижил. Санах ой O(D²): d бүрийн [−d, d] цонхыг хадгална.
     */
    public static List<String> diffMyers(List<String> a, List<String> b) {
        int n = a.size();
        int m = b.size();
        int max = n + m;
        int off = max + 1;
        int[] v = new int[2 * max + 3];
        List<int[]> trace = new ArrayList<>();
        outer:
        for (int d = 0; d <= max; d++) {
            trace.add(java.util.Arrays.copyOfRange(v, off - d - 1, off + d + 2)); // [−d−1, d+1]
            for (int k = -d; k <= d; k += 2) {
                int x = (k == -d || (k != d && v[off + k - 1] < v[off + k + 1]))
                        ? v[off + k + 1]          // доош: B-ээс нэмнэ
                        : v[off + k - 1] + 1;     // баруун: A-аас хасна
                int y = x - k;
                while (x < n && y < m && a.get(x).equals(b.get(y))) { // диагональ
                    x++;
                    y++;
                }
                v[off + k] = x;
                if (x >= n && y >= m) break outer;
            }
        }

        List<String> out = new ArrayList<>();
        int x = n;
        int y = m;
        for (int d = trace.size() - 1; d >= 0; d--) {
            int[] vd = trace.get(d); // vd[i] = v[k] үед i = k + d + 1
            int k = x - y;
            int prevK = (k == -d || (k != d && vd[k - 1 + d + 1] < vd[k + 1 + d + 1])) ? k + 1 : k - 1;
            int prevX = d > 0 ? vd[prevK + d + 1] : 0;
            int prevY = d > 0 ? prevX - prevK : 0;
            while (x > prevX && y > prevY) {
                x--;
                y--;
                out.add(" " + a.get(x));
            }
            if (d > 0) out.add(x == prevX ? "+" + b.get(prevY) : "-" + a.get(prevX));
            x = prevX;
            y = prevY;
        }
        java.util.Collections.reverse(out);
        return out;
    }

    private Lcs() {}
}
