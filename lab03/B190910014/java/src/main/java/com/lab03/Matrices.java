package com.lab03;

/** Матрицын туслах функцүүд. */
public final class Matrices {

    /** A, B хоёулаа ижил n×n хэмжээтэй эсэхийг шалгаж, n-г буцаана. */
    public static int checkSquare(long[][] a, long[][] b) {
        int n = a.length;
        boolean ok = b.length == n;
        for (int i = 0; ok && i < n; i++) {
            ok = a[i].length == n && b[i].length == n;
        }
        if (!ok) {
            throw new IllegalArgumentException("A ба B ижил n×n хэмжээтэй байх ёстой");
        }
        return n;
    }

    private Matrices() {}
}
