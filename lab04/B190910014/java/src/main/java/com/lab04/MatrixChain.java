package com.lab04;

public final class MatrixChain {

    public record Result(long minMults, String parens) {}

    /**
     * Matrix-Chain-Order ба Print-Optimal-Parens (CLRS 14.2). A_i нь p[i-1] × p[i].
     * m[i][j]: A_i…A_j-ийн хамгийн бага скаляр үржүүлэлт, s[i][j]: сүүлд хуваах цэг.
     * Хугацаа Θ(n³), санах ой Θ(n²).
     */
    public static Result order(int[] p) {
        int n = p.length - 1;
        long[][] m = new long[n + 1][n + 1];
        int[][] s = new int[n + 1][n + 1];
        for (int len = 2; len <= n; len++) { // гинжийн урт
            for (int i = 1; i <= n - len + 1; i++) {
                int j = i + len - 1;
                m[i][j] = Long.MAX_VALUE;
                for (int k = i; k < j; k++) {
                    long q = m[i][k] + m[k + 1][j] + (long) p[i - 1] * p[k] * p[j];
                    if (q < m[i][j]) {
                        m[i][j] = q;
                        s[i][j] = k;
                    }
                }
            }
        }
        StringBuilder sb = new StringBuilder();
        parens(s, 1, n, sb);
        return new Result(m[1][n], sb.toString());
    }

    private static void parens(int[][] s, int i, int j, StringBuilder sb) {
        if (i == j) {
            sb.append('A').append(i);
            return;
        }
        sb.append('(');
        parens(s, i, s[i][j], sb);
        parens(s, s[i][j] + 1, j, sb);
        sb.append(')');
    }

    private MatrixChain() {}
}
