package com.lab03;

/** F_n mod (10⁹ + 7)-ийг матрицын зэргээр Θ(lg n) удаа 2×2 үржүүлж олно. */
public final class FibMatrix {

    public static final long MOD = 1_000_000_007L;

    public record Result(long value, long mults) {}

    /**
     * Mⁿ = [[F(n+1), F(n)], [F(n), F(n−1)]], M = [[1, 1], [1, 0]]. Mⁿ = (M^⌊n/2⌋)², сондгой n үед
     * дахин M-ээр үржүүлнэ. 2×2-ыг 1-р бодлогын MatrixMultiply-аар үржүүлж mod авна:
     * гишүүд < p тул үржвэрийн нийлбэр ≤ 2p² < 2⁶³ буюу long-д багтана.
     */
    public static Result fib(long n) {
        if (n < 0) throw new IllegalArgumentException("n сөрөг байж болохгүй");
        long[] mults = new long[1];
        long[][] mk = power(n, mults);
        return new Result(mk[0][1], mults[0]);
    }

    private static long[][] power(long k, long[] mults) {
        if (k == 0) return new long[][] {{1, 0}, {0, 1}};
        long[][] half = power(k / 2, mults); // дэд бодлогыг ганцхан удаа
        long[][] square = mul(half, half, mults);
        if (k % 2 == 1) square = mul(square, new long[][] {{1, 1}, {1, 0}}, mults);
        return square;
    }

    private static long[][] mul(long[][] x, long[][] y, long[] mults) {
        MatrixMultiply.Result r = MatrixMultiply.multiply(x, y);
        mults[0] += r.mults();
        long[][] c = r.c();
        for (long[] row : c) for (int j = 0; j < row.length; j++) row[j] %= MOD;
        return c;
    }

    private FibMatrix() {}
}
