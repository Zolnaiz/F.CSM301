package com.lab03;

public final class GaussSolve {

    public record Result(double[] x, long ops) {}

    /** Гауссын арга (мөрийн хувиргалтгүй). Шийд x ба *, /, +, - үйлдлийн тоо. */
    public static Result solve(long[][] a, long[] b) {
        int n = a.length;
        boolean ok = b.length == n;
        for (int i = 0; ok && i < n; i++) ok = a[i].length == n;
        if (!ok) throw new IllegalArgumentException("A нь n×n, b нь n урттай байх ёстой");

        double[][] m = new double[n][n]; // оролтыг өөрчлөхгүйн тулд хуулна
        double[] v = new double[n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) m[i][j] = a[i][j];
            v[i] = b[i];
        }
        long ops = 0;

        // Шууд явц: k-р баганын доорх гишүүдийг тэглэнэ.
        for (int k = 0; k < n - 1; k++) {
            if (m[k][k] == 0) throw new IllegalArgumentException("хувиргалтын гишүүн тэг боллоо");
            for (int i = k + 1; i < n; i++) {
                double factor = m[i][k] / m[k][k];
                ops++;
                for (int j = k; j < n; j++) {
                    m[i][j] = m[i][j] - factor * m[k][j];
                    ops += 2;
                }
                v[i] = v[i] - factor * v[k];
                ops += 2;
            }
        }

        // Буцах орлуулга: доороос дээш x-ийг олно.
        double[] x = new double[n];
        for (int i = n - 1; i >= 0; i--) {
            double s = 0;
            for (int j = i + 1; j < n; j++) {
                s = s + m[i][j] * x[j];
                ops += 2;
            }
            x[i] = (v[i] - s) / m[i][i];
            ops += 2;
        }
        return new Result(x, ops);
    }

    /** solve-ийн үйлдлийн тоо: (4n³ + 15n² − 7n) / 6 ≈ ⅔n³. */
    public static long ops(long n) {
        return (4 * n * n * n + 15 * n * n - 7 * n) / 6;
    }

    private GaussSolve() {}
}
