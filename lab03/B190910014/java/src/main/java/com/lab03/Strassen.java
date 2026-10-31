package com.lab03;

public final class Strassen {

    /** Штрассены алгоритм. C = A·B ба скаляр үржүүлэлтийн тоог буцаана. */
    public static MatrixMultiply.Result multiply(long[][] a, long[][] b) {
        return multiply(a, b, 1);
    }

    /**
     * Сайжруулсан хувилбар: n ≤ cutoff болмогц давталттай арга руу шилжинэ.
     * cutoff = 1 бол лекцийн цэвэр Штрассен.
     */
    public static MatrixMultiply.Result multiply(long[][] a, long[][] b, int cutoff) {
        int n = Matrices.checkSquare(a, b);
        if (n == 0 || (n & (n - 1)) != 0) {
            throw new IllegalArgumentException("n нь 2-ын зэрэг байх ёстой");
        }
        if (cutoff < 1) {
            throw new IllegalArgumentException("cutoff ≥ 1 байх ёстой");
        }
        long[] mults = new long[1];
        long[][] c = strassen(a, b, mults, cutoff);
        return new MatrixMultiply.Result(c, mults[0]);
    }

    private static long[][] strassen(long[][] a, long[][] b, long[] mults, int cutoff) {
        int n = a.length;
        if (n == 1) {
            mults[0]++;
            return new long[][] {{a[0][0] * b[0][0]}};
        }
        if (n <= cutoff) {
            MatrixMultiply.Result r = MatrixMultiply.multiply(a, b);
            mults[0] += r.mults();
            return r.c();
        }

        // 1-р алхам: дэд матрицад хуваах
        int h = n / 2;
        long[][] a11 = part(a, 0, 0, h), a12 = part(a, 0, h, h);
        long[][] a21 = part(a, h, 0, h), a22 = part(a, h, h, h);
        long[][] b11 = part(b, 0, 0, h), b12 = part(b, 0, h, h);
        long[][] b21 = part(b, h, 0, h), b22 = part(b, h, h, h);

        // 2-р алхам: S1, ..., S10
        long[][] s1 = sub(b12, b22);
        long[][] s2 = add(a11, a12);
        long[][] s3 = add(a21, a22);
        long[][] s4 = sub(b21, b11);
        long[][] s5 = add(a11, a22);
        long[][] s6 = add(b11, b22);
        long[][] s7 = sub(a12, a22);
        long[][] s8 = add(b21, b22);
        long[][] s9 = sub(a11, a21);
        long[][] s10 = add(b11, b12);

        // 3-р алхам: P1, ..., P7 — 8 биш 7 дахин дуудалт
        long[][] p1 = strassen(a11, s1, mults, cutoff);
        long[][] p2 = strassen(s2, b22, mults, cutoff);
        long[][] p3 = strassen(s3, b11, mults, cutoff);
        long[][] p4 = strassen(a22, s4, mults, cutoff);
        long[][] p5 = strassen(s5, s6, mults, cutoff);
        long[][] p6 = strassen(s7, s8, mults, cutoff);
        long[][] p7 = strassen(s9, s10, mults, cutoff);

        // 4-р алхам: C11, C12, C21, C22
        long[][] c = new long[n][n];
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < h; j++) {
                c[i][j] = p5[i][j] + p4[i][j] - p2[i][j] + p6[i][j];
                c[i][j + h] = p1[i][j] + p2[i][j];
                c[i + h][j] = p3[i][j] + p4[i][j];
                c[i + h][j + h] = p5[i][j] + p1[i][j] - p3[i][j] - p7[i][j];
            }
        }
        return c;
    }

    private static long[][] part(long[][] m, int r, int c, int h) {
        long[][] p = new long[h][h];
        for (int i = 0; i < h; i++) System.arraycopy(m[r + i], c, p[i], 0, h);
        return p;
    }

    private static long[][] add(long[][] x, long[][] y) {
        int n = x.length;
        long[][] z = new long[n][n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) z[i][j] = x[i][j] + y[i][j];
        return z;
    }

    private static long[][] sub(long[][] x, long[][] y) {
        int n = x.length;
        long[][] z = new long[n][n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) z[i][j] = x[i][j] - y[i][j];
        return z;
    }

    private Strassen() {}
}
