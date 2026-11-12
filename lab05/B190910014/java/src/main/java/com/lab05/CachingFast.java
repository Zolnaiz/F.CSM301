package com.lab05;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * Оновчтой кэш — сайжруулсан (A төвшин). nextUse[i]-г төгсгөлөөс нэг гүйж Θ(n)-д олоод, кэш
 * дэх хуудсуудыг дараагийн хандалтаар нь хамгийн их овоонд (long массив дээрх binary heap)
 * хадгална. Дахин хандахад шинэ оролт нэмж, хуучныг «хуучирсан» гэж үлдээнэ (lazy deletion).
 * Овоо 4k + 64-өөс томровол кэшийн k оролтоос шинээр байгуулна. Нийт O(n lg k) хугацаа,
 * O(n) санах ой (nextUse массив), овоо O(k).
 */
public final class CachingFast {

    public static int[] nextUse(int[] requests) {
        int n = requests.length;
        int[] next = new int[n];
        Map<Integer, Integer> last = new HashMap<>();
        for (int i = n - 1; i >= 0; i--) {
            next[i] = last.getOrDefault(requests[i], n); // n нь «∞»
            last.put(requests[i], i);
        }
        return next;
    }

    public static long misses(int k, int[] requests) {
        if (k < 0) throw new IllegalArgumentException("k сөрөг байж болохгүй");
        if (k == 0) return requests.length;
        int[] next = nextUse(requests);
        Map<Integer, Integer> cache = new HashMap<>(2 * k); // хуудас → дараагийн хандалт
        LongMaxHeap heap = new LongMaxHeap();
        long misses = 0;
        for (int i = 0; i < requests.length; i++) {
            int page = requests[i];
            if (!cache.containsKey(page)) {
                misses++;
                if (cache.size() == k) {
                    while (true) {
                        long top = heap.pop();
                        int victim = (int) top; // доод 32 бит
                        Integer current = cache.get(victim);
                        if (current != null && current == (int) (top >>> 32)) { // хуучирсан биш
                            cache.remove(victim);
                            break;
                        }
                    }
                }
            }
            cache.put(page, next[i]);
            heap.push(((long) next[i] << 32) | (page & 0xffffffffL));
            if (heap.size > 4 * k + 64) { // хуучирсан оролтыг цэвэрлэж овоог O(k) хэмжээнд барина
                heap = new LongMaxHeap();
                for (var e : cache.entrySet()) heap.push(((long) e.getValue() << 32) | (e.getKey() & 0xffffffffL));
            }
        }
        return misses;
    }

    /** Боксгүй long утгын хамгийн их овоо. */
    static final class LongMaxHeap {
        private long[] a = new long[16];
        private int size;

        void push(long x) {
            if (size == a.length) a = Arrays.copyOf(a, 2 * size);
            int i = size++;
            while (i > 0 && a[(i - 1) / 2] < x) {
                a[i] = a[(i - 1) / 2];
                i = (i - 1) / 2;
            }
            a[i] = x;
        }

        long pop() {
            long top = a[0];
            long x = a[--size];
            int i = 0;
            while (2 * i + 1 < size) {
                int c = 2 * i + 1;
                if (c + 1 < size && a[c + 1] > a[c]) c++;
                if (a[c] <= x) break;
                a[i] = a[c];
                i = c;
            }
            a[i] = x;
            return top;
        }
    }

    private CachingFast() {}
}
