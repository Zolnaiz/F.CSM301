package com.lab02;

public final class BinarySearch {

    public record Result(int index, long calls) {}

    /**
     * Эрэмбэлэгдсэн, давхардалгүй массиваас хайх.
     * Олдсон товъёг (олдохгүй бол -1) болон нийт дуудалтын тоог буцаана.
     */
    public static Result search(int[] a, int x) {
        return search(a, x, 0, a.length - 1);
    }

    /** Recursive-Binary-Search(A, x, p, r). */
    private static Result search(int[] a, int x, int p, int r) {
        if (p > r) {
            return new Result(-1, 1);
        }
        int q = (p + r) / 2;
        if (a[q] == x) {
            return new Result(q, 1);
        }
        Result sub = a[q] < x ? search(a, x, q + 1, r) : search(a, x, p, q - 1);
        return new Result(sub.index(), sub.calls() + 1);
    }

    private BinarySearch() {}
}
