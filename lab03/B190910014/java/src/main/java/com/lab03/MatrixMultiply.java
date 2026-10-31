package com.lab03;

public final class MatrixMultiply {

    public record Result(long[][] c, long mults) {}

    /** Matrix-Multiply(A, B, C, n): C = A·B үржвэр болон скаляр үржүүлэлтийн тоо. */
    public static Result multiply(long[][] a, long[][] b) {
        int n = Matrices.checkSquare(a, b);
        long[][] c = new long[n][n]; // Java шинэ массивыг 0-ээр дүүргэдэг: Θ(n²)
        long mults = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    c[i][j] = c[i][j] + a[i][k] * b[k][j];
                    mults++;
                }
            }
        }
        return new Result(c, mults);
    }

    private MatrixMultiply() {}
}
