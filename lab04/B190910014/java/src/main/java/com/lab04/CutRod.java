package com.lab04;

import java.util.ArrayList;
import java.util.List;

public final class CutRod {

    public record Result(long revenue, long innerLoopCount) {}

    public record ExtendedResult(long revenue, int[] cuts) {}

    /**
     * Bottom-Up-Cut-Rod (CLRS 14.1). p[i-1] нь i урттай хэсгийн үнэ. Дотоод давталт j = 1..n
     * бүрд j удаа эргэх тул нийт n(n+1)/2 = Θ(n²).
     */
    public static Result bottomUp(int[] p) {
        int n = p.length;
        long[] r = new long[n + 1]; // r[j]: j урттай савааны хамгийн их орлого
        long loops = 0;
        for (int j = 1; j <= n; j++) {
            long q = Long.MIN_VALUE;
            for (int i = 1; i <= j; i++) { // эхний хэсгийн урт i
                q = Math.max(q, p[i - 1] + r[j - i]);
                loops++;
            }
            r[j] = q;
        }
        return new Result(r[n], loops);
    }

    /** Extended-Bottom-Up-Cut-Rod ба Print-Cut-Rod-Solution: орлого ба хэсгүүдийн урт. */
    public static ExtendedResult extended(int[] p) {
        int n = p.length;
        long[] r = new long[n + 1];
        int[] s = new int[n + 1]; // s[j]: эхлээд огтлох хэсгийн оновчтой урт
        for (int j = 1; j <= n; j++) {
            long q = Long.MIN_VALUE;
            for (int i = 1; i <= j; i++) {
                if (p[i - 1] + r[j - i] > q) {
                    q = p[i - 1] + r[j - i];
                    s[j] = i;
                }
            }
            r[j] = q;
        }
        List<Integer> cuts = new ArrayList<>();
        for (int len = n; len > 0; len -= s[len]) cuts.add(s[len]);
        return new ExtendedResult(r[n], cuts.stream().mapToInt(Integer::intValue).toArray());
    }

    private CutRod() {}
}
