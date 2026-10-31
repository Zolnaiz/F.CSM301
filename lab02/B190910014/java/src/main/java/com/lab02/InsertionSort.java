package com.lab02;

public final class InsertionSort {

    public record Result(int[] sorted, long shifts) {}

    /**
     * Өсөхөөр эрэмбэлнэ. A[j + 1] = A[j] мөр биелэгдсэн тоог буцаана.
     */
    public static Result sort(int[] a) {
        a = a.clone();
        long shifts = 0;
        for (int i = 1; i < a.length; i++) {
            int key = a[i];
            int j = i - 1;
            while (j >= 0 && a[j] > key) {
                a[j + 1] = a[j];
                shifts++;
                j--;
            }
            a[j + 1] = key;
        }
        return new Result(a, shifts);
    }

    private InsertionSort() {}
}
