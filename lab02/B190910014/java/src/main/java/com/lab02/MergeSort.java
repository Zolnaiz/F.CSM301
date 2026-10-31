package com.lab02;

import java.util.Arrays;

public final class MergeSort {

    public record Result(int[] sorted, long writes) {}

    /**
     * Өсөхөөр эрэмбэлнэ. Merge доторх A[k] = ... бичилтийн нийт тоог буцаана.
     */
    public static Result sort(int[] a) {
        a = a.clone();
        long writes = mergeSort(a, 0, a.length - 1);
        return new Result(a, writes);
    }

    private static long mergeSort(int[] a, int p, int r) {
        if (p >= r) {
            return 0;
        }
        int q = (p + r) / 2;
        long writes = mergeSort(a, p, q);
        writes += mergeSort(a, q + 1, r);
        return writes + merge(a, p, q, r);
    }

    /** A[p..q], A[q+1..r] хоёр эрэмбэлэгдсэн хэсгийг нэгтгэнэ. */
    private static long merge(int[] a, int p, int q, int r) {
        int[] left = Arrays.copyOfRange(a, p, q + 1);
        int[] right = Arrays.copyOfRange(a, q + 1, r + 1);
        int i = 0;
        int j = 0;
        int k = p;
        long writes = 0;
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                a[k] = left[i];
                i++;
            } else {
                a[k] = right[j];
                j++;
            }
            k++;
            writes++;
        }
        while (i < left.length) {
            a[k] = left[i];
            i++;
            k++;
            writes++;
        }
        while (j < right.length) {
            a[k] = right[j];
            j++;
            k++;
            writes++;
        }
        return writes;
    }

    private MergeSort() {}
}
