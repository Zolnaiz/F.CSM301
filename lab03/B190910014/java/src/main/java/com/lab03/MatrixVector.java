package com.lab03;

public final class MatrixVector {

    public record Result(long[] y, long ops) {}

    /** y = A·x. Мөр бүрд n үржүүлэх + n нэмэх тул нийт 2n² үйлдэл. */
    public static Result matrixVector(long[][] a, long[] x) {
        int n = a.length;
        boolean ok = x.length == n;
        for (int i = 0; ok && i < n; i++) ok = a[i].length == n;
        if (!ok) throw new IllegalArgumentException("A нь n×n, x нь n урттай байх ёстой");
        long[] y = new long[n];
        long ops = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                y[i] = y[i] + a[i][j] * x[j];
                ops += 2;
            }
        }
        return new Result(y, ops);
    }

    /** w_i = u_i · v_i. n үржүүлэх үйлдэл. */
    public static Result hadamard(long[] u, long[] v) {
        if (u.length != v.length) {
            throw new IllegalArgumentException("векторууд ижил урттай байх ёстой");
        }
        long[] w = new long[u.length];
        for (int i = 0; i < u.length; i++) w[i] = u[i] * v[i];
        return new Result(w, u.length);
    }

    private MatrixVector() {}
}
