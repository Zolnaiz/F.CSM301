package com.prj2;

/**
 * LeetCode 752 — сайжруулсан (A төвшин): хоёр талын гүехэн хайлт, төлөв нь 0…9999 бүхэл тоо.
 * <ul>
 *   <li>Хөршийг 10-ын зэргээр нэмж/хасаж олно — String үүсгэхгүй; side[] нь byte массив.</li>
 *   <li>«0000» ба зорилгоос ээлжлэн, жижиг хилийг нь нэг төвшин тэлнэ. Хоёр хил уулзмагц
 *       хариу = хоёр талын төвшний нийлбэр. Нэг талын BFS ≈ b^d, хоёр талынх ≈ 2·b^(d/2) төлөв.</li>
 * </ul>
 */
public class OpenLockImproved {

    private static final int[] POW = {1000, 100, 10, 1};

    /** Тэлсэн төлөвийн тоо (хэмжилтэд). */
    public long expanded = 0;

    public int openLock(String[] deadends, String target) {
        byte[] dead = new byte[10000];
        for (String d : deadends) dead[Integer.parseInt(d)] = 1;
        int goal = Integer.parseInt(target);
        if (dead[0] == 1 || dead[goal] == 1) return -1;
        if (goal == 0) return 0;
        byte[] side = new byte[10000]; // 0 — үзээгүй, 1 — эхлэлээс, 2 — зорилгоос
        side[0] = 1;
        side[goal] = 2;
        int[][] front = {null, {0}, {goal}};
        int[] size = {0, 1, 1};
        int[] depth = {0, 0, 0};
        int[] buffer = new int[10000];
        while (size[1] > 0 && size[2] > 0) {
            int s = size[1] <= size[2] ? 1 : 2; // жижиг хилийг тэлнэ
            int other = 3 - s;
            depth[s]++;
            int count = 0;
            for (int idx = 0; idx < size[s]; idx++) {
                int x = front[s][idx];
                expanded++;
                for (int p : POW) {
                    int digit = x / p % 10;
                    for (int k = 0; k < 2; k++) {
                        int y = k == 0 ? (digit < 9 ? x + p : x - 9 * p)  // +1 (9 → 0)
                                       : (digit > 0 ? x - p : x + 9 * p); // −1 (0 → 9)
                        if (dead[y] == 1 || side[y] == s) continue;
                        if (side[y] == other) return depth[1] + depth[2];
                        side[y] = (byte) s;
                        buffer[count++] = y;
                    }
                }
            }
            front[s] = java.util.Arrays.copyOf(buffer, count);
            size[s] = count;
        }
        return -1;
    }
}
