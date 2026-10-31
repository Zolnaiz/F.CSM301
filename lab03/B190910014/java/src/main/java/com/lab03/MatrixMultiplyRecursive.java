package com.lab03;

public final class MatrixMultiplyRecursive {

    /** Matrix-Multiply-Recursive(A, B, C, n). n нь 2-ын зэрэг байна. */
    public static MatrixMultiply.Result multiply(long[][] a, long[][] b) {
        int n = Matrices.checkSquare(a, b);
        if (n == 0 || (n & (n - 1)) != 0) {
            throw new IllegalArgumentException("n нь 2-ын зэрэг байх ёстой");
        }
        long[][] c = new long[n][n];
        long mults = recurse(a, b, c, 0, 0, 0, n);
        return new MatrixMultiply.Result(c, mults);
    }

    /**
     * C[i.., j..] += A[i.., k..] · B[k.., j..] (n×n дэд матрицууд).
     * Дэд матрицыг хуулахгүй, зүүн дээд булангийн товъёгоор дамжуулна.
     */
    private static long recurse(long[][] a, long[][] b, long[][] c,
                                int i, int j, int k, int n) {
        if (n == 1) {
            c[i][j] = c[i][j] + a[i][k] * b[k][j];
            return 1;
        }
        int h = n / 2;
        long mults = 0;
        mults += recurse(a, b, c, i,     j,     k,     h); // C11 += A11·B11
        mults += recurse(a, b, c, i,     j + h, k,     h); // C12 += A11·B12
        mults += recurse(a, b, c, i + h, j,     k,     h); // C21 += A21·B11
        mults += recurse(a, b, c, i + h, j + h, k,     h); // C22 += A21·B12
        mults += recurse(a, b, c, i,     j,     k + h, h); // C11 += A12·B21
        mults += recurse(a, b, c, i,     j + h, k + h, h); // C12 += A12·B22
        mults += recurse(a, b, c, i + h, j,     k + h, h); // C21 += A22·B21
        mults += recurse(a, b, c, i + h, j + h, k + h, h); // C22 += A22·B22
        return mults;
    }

    private MatrixMultiplyRecursive() {}
}
