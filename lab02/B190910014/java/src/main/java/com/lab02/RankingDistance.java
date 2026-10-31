package com.lab02;

import java.util.Arrays;

public final class RankingDistance {

    /**
     * Хоёр эрэмбийн хоорондох зайг буцаана.
     *
     * <p>B-ийн ном бүрийг A дахь байрлалаар нь сольвол A-тай зөрсөн {x, y} хос
     * бүр шинэ дараалалд урвуу хос болно. Тиймээс зөрөө нь урвуу хосын тоо.
     */
    public static long distance(int[] a, int[] b) {
        if (a.length != b.length) {
            throw new IllegalArgumentException("A ба B ижил урттай байх ёстой");
        }
        int[] position = new int[a.length + 1];
        for (int i = 0; i < a.length; i++) {
            position[a[i]] = i;
        }
        int[] seq = new int[b.length];
        for (int i = 0; i < b.length; i++) {
            seq[i] = position[b[i]];
        }
        return sortAndCount(seq, 0, seq.length - 1);
    }

    private static long sortAndCount(int[] seq, int p, int r) {
        if (p >= r) {
            return 0;
        }
        int q = (p + r) / 2;
        long inversions = sortAndCount(seq, p, q);
        inversions += sortAndCount(seq, q + 1, r);
        return inversions + mergeCount(seq, p, q, r);
    }

    /** seq[p..q], seq[q+1..r]-г нэгтгэж, хоёр хэсгийн хоорондох урвуу хосыг тоолно. */
    private static long mergeCount(int[] seq, int p, int q, int r) {
        int[] left = Arrays.copyOfRange(seq, p, q + 1);
        int[] right = Arrays.copyOfRange(seq, q + 1, r + 1);
        int i = 0;
        int j = 0;
        int k = p;
        long inversions = 0;
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                seq[k++] = left[i++];
            } else {
                // left[i..] бүгд right[j]-ээс их тул бүгд right[j]-тэй урвуу хос.
                seq[k++] = right[j++];
                inversions += left.length - i;
            }
        }
        while (i < left.length) {
            seq[k++] = left[i++];
        }
        while (j < right.length) {
            seq[k++] = right[j++];
        }
        return inversions;
    }

    private RankingDistance() {}
}
