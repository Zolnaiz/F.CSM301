package com.lab05;

import java.util.HashSet;
import java.util.Set;

public final class Caching {

    /**
     * Оновчтой кэш (B төвшин), furthest-in-future. Кэш дүүрсэн үед кэш дэх хуудас бүрийн
     * дараагийн хандалтыг цаашаа шугаман хайлтаар олж, хамгийн хойно хандагдах (эсвэл огт
     * хандагдахгүй) хуудсыг хасна. Нэг хасалт O(k·n), хамгийн муу үед нийт O(n²·k).
     */
    public static long misses(int k, int[] requests) {
        if (k < 0) throw new IllegalArgumentException("k сөрөг байж болохгүй");
        if (k == 0) return requests.length;
        Set<Integer> cache = new HashSet<>();
        long misses = 0;
        for (int i = 0; i < requests.length; i++) {
            int page = requests[i];
            if (cache.contains(page)) continue;
            misses++;
            if (cache.size() == k) {
                int victim = 0;
                int furthest = -1;
                for (int q : cache) {
                    int next = i + 1;
                    while (next < requests.length && requests[next] != q) next++;
                    if (next > furthest) {
                        furthest = next;
                        victim = q;
                    }
                    if (next == requests.length) break; // цаашид огт хандагдахгүй
                }
                cache.remove(victim);
            }
            cache.add(page);
        }
        return misses;
    }

    private Caching() {}
}
