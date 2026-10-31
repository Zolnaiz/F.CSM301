package com.lab02;

public final class BinaryInsertionSort {

    public record Result(int[] sorted, long comparisons, long shifts) {}

    /**
     * Өсөхөөр эрэмбэлнэ. A[i]-тэй тэнцүү гишүүд байвал A[i]-г тэдгээрийн ард
     * оруулна. Хайлтын харьцуулалт болон зөөлтийн тоог буцаана.
     */
    public static Result sort(int[] a) {
        a = a.clone();
        long comparisons = 0;
        long shifts = 0;
        for (int i = 1; i < a.length; i++) {
            int key = a[i];
            // A[0..i-1]-ээс key-ээс их эхний гишүүний байрлалыг хайна.
            int lo = 0;
            int hi = i;
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                comparisons++;
                if (a[mid] <= key) {
                    lo = mid + 1;
                } else {
                    hi = mid;
                }
            }
            for (int j = i - 1; j >= lo; j--) {
                a[j + 1] = a[j];
                shifts++;
            }
            a[lo] = key;
        }
        return new Result(a, comparisons, shifts);
    }

    private BinaryInsertionSort() {}
}
