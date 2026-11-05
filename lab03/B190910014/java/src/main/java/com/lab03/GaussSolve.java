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

    /**
     * Сайжруулсан Гаусс (A түвшин). Тэглэгдэх k-р баганыг тооцоолохгүй (j = k+1..n−1 л шинэчилнэ),
     * тэргүүлэх мөр ба шинэчлэх мөрийн заагчийг давталтаас гадна авна. Үйлдэл (4n³ + 9n² − n)/6.
     */
    public static Result solveFast(long[][] a, long[] b) {
        int n = a.length;
        boolean ok = b.length == n;
        for (int i = 0; ok && i < n; i++) ok = a[i].length == n;
        if (!ok) throw new IllegalArgumentException("A нь n×n, b нь n урттай байх ёстой");
        double[][] m = new double[n][n];
        double[] v = new double[n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) m[i][j] = a[i][j];
            v[i] = b[i];
        }
        long ops = 0;
        for (int k = 0; k < n - 1; k++) {
            double[] pivotRow = m[k];
            double pivot = pivotRow[k];
            if (pivot == 0) throw new IllegalArgumentException("хувиргалтын гишүүн тэг боллоо");
            for (int i = k + 1; i < n; i++) {
                double[] row = m[i];
                double factor = row[k] / pivot;
                row[k] = 0;
                for (int j = k + 1; j < n; j++) row[j] -= factor * pivotRow[j];
                v[i] -= factor * v[k];
            }
            long rows = n - 1 - k;
            ops += rows * (1 + 2 * rows + 2);
        }
        double[] x = new double[n];
        for (int i = n - 1; i >= 0; i--) {
            double[] row = m[i];
            double s = 0;
            for (int j = i + 1; j < n; j++) s += row[j] * x[j];
            x[i] = (v[i] - s) / row[i];
            ops += 2L * (n - 1 - i) + 2;
        }
        return new Result(x, ops);
    }

    /** solveFast-ийн үйлдлийн тоо: (4n³ + 9n² − n) / 6. */
    public static long fastOps(long n) {
        return (4 * n * n * n + 9 * n * n - n) / 6;
    }

    public record JacobiResult(double[] x, long ops, int iterations) {}

    /** Якобийн арга, tol = 1e-12, хамгийн ихдээ 1000 давталт. */
    public static JacobiResult solveJacobi(long[][] a, long[] b) {
        return solveJacobi(a, b, 1e-12, 1000);
    }

    /**
     * Якобийн давталтын арга (A түвшин): x⁽ᵗ⁺¹⁾ᵢ = (bᵢ − Σⱼ≠ᵢ aᵢⱼ x⁽ᵗ⁾ⱼ) / aᵢᵢ. Хатуу диагональ
     * давамгай A-д нийлэлт баталгаатай. Нэг давталт 2n² үйлдэл (матриц–вектор үржүүлэлттэй ижил).
     * max|Δx| ≤ tol·max(1, max|x|) болоход зогсоно.
     */
    public static JacobiResult solveJacobi(long[][] a, long[] b, double tol, int maxIter) {
        int n = a.length;
        boolean ok = b.length == n;
        for (int i = 0; ok && i < n; i++) ok = a[i].length == n;
        if (!ok) throw new IllegalArgumentException("A нь n×n, b нь n урттай байх ёстой");
        double[][] m = new double[n][n];
        double[] v = new double[n];
        for (int i = 0; i < n; i++) {
            long off = 0;
            for (int j = 0; j < n; j++) {
                m[i][j] = a[i][j];
                if (j != i) off += Math.abs(a[i][j]);
            }
            if (Math.abs(a[i][i]) <= off) {
                throw new IllegalArgumentException("Якобийн арга хатуу диагональ давамгай матриц шаардана");
            }
            v[i] = b[i];
        }
        if (n == 0) return new JacobiResult(new double[0], 0, 0);
        double[] x = new double[n];
        double[] next = new double[n];
        for (int it = 1; it <= maxIter; it++) {
            double delta = 0;
            double size = 1;
            for (int i = 0; i < n; i++) {
                double[] row = m[i];
                double s = 0;
                for (int j = 0; j < n; j++) s += row[j] * x[j];
                s -= row[i] * x[i];
                next[i] = (v[i] - s) / row[i];
                delta = Math.max(delta, Math.abs(next[i] - x[i]));
                size = Math.max(size, Math.abs(next[i]));
            }
            double[] t = x;
            x = next;
            next = t;
            if (delta <= tol * size) return new JacobiResult(x, 2L * it * n * n, it);
        }
        throw new IllegalArgumentException("Якобийн давталт " + maxIter + " алхамд нийлсэнгүй");
    }

    private GaussSolve() {}
}
