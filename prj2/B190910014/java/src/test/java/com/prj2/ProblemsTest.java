package com.prj2;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.*;

/** LeetCode-ийн жишээ + энгийн аргатай санамсаргүй тулгалт. */
class ProblemsTest {

    private final Random rng = new Random(13);

    @Test
    void p1StrStr() {
        StrStr s = new StrStr();
        assertEquals(0, s.strStr("sadbutsad", "sad"));
        assertEquals(-1, s.strStr("leetcode", "leeto"));
        assertEquals(4, s.strStr("mississippi", "issip"));
        assertEquals(3, s.strStr("aaaaab", "aab"));
        for (int t = 0; t < 3000; t++) {
            String h = randomString("ab", 1 + rng.nextInt(30));
            String n = randomString("ab", 1 + rng.nextInt(6));
            int expected = h.indexOf(n); // зөвхөн тест дээр шалгах зорилгоор
            assertEquals(expected, s.strStr(h, n), h + " / " + n);
            assertEquals(expected, s.strStrNaive(h, n), h + " / " + n);
        }
    }

    private String randomString(String alphabet, int len) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < len; i++) sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
        return sb.toString();
    }

    @Test
    void p2FloodFill() {
        int[][] out = new FloodFill().floodFill(new int[][] {{1, 1, 1}, {1, 1, 0}, {1, 0, 1}}, 1, 1, 2);
        assertArrayEquals(new int[][] {{2, 2, 2}, {2, 2, 0}, {2, 0, 1}}, out);
        for (int t = 0; t < 300; t++) {
            int rows = 1 + rng.nextInt(7);
            int cols = 1 + rng.nextInt(7);
            int[][] image = new int[rows][cols];
            for (int[] row : image) for (int c = 0; c < cols; c++) row[c] = rng.nextInt(3);
            int sr = rng.nextInt(rows);
            int sc = rng.nextInt(cols);
            int color = rng.nextInt(3);
            int[][] expected = reference(image, sr, sc, color);
            int[][] copy = Arrays.stream(image).map(int[]::clone).toArray(int[][]::new);
            assertArrayEquals(expected, new FloodFill().floodFill(copy, sr, sc, color));
        }
    }

    /** Дахин дуудах DFS — жижиг зурагт лавлах хариу. */
    private static int[][] reference(int[][] image, int sr, int sc, int color) {
        int[][] img = Arrays.stream(image).map(int[]::clone).toArray(int[][]::new);
        if (img[sr][sc] != color) dfs(img, sr, sc, img[sr][sc], color);
        return img;
    }

    private static void dfs(int[][] img, int r, int c, int old, int color) {
        if (r < 0 || r >= img.length || c < 0 || c >= img[0].length || img[r][c] != old) return;
        img[r][c] = color;
        dfs(img, r + 1, c, old, color);
        dfs(img, r - 1, c, old, color);
        dfs(img, r, c + 1, old, color);
        dfs(img, r, c - 1, old, color);
    }

    @Test
    void p3Cookies() {
        assertEquals(1, new AssignCookies().findContentChildren(new int[] {1, 2, 3}, new int[] {1, 1}));
        assertEquals(2, new AssignCookies().findContentChildren(new int[] {1, 2}, new int[] {1, 2, 3}));
        for (int t = 0; t < 500; t++) {
            int[] g = rng.ints(rng.nextInt(8), 1, 10).toArray();
            int[] s = rng.ints(rng.nextInt(8), 1, 10).toArray();
            assertEquals(matching(g, s), new AssignCookies().findContentChildren(g.clone(), s.clone()));
        }
    }

    /** Хоёр талт графын хамгийн их хослол (Кун). */
    private static int matching(int[] g, int[] s) {
        int[] match = new int[s.length];
        Arrays.fill(match, -1);
        int result = 0;
        for (int i = 0; i < g.length; i++) if (augment(i, g, s, match, new boolean[s.length])) result++;
        return result;
    }

    private static boolean augment(int i, int[] g, int[] s, int[] match, boolean[] seen) {
        for (int j = 0; j < s.length; j++) {
            if (s[j] >= g[i] && !seen[j]) {
                seen[j] = true;
                if (match[j] == -1 || augment(match[j], g, s, match, seen)) {
                    match[j] = i;
                    return true;
                }
            }
        }
        return false;
    }

    @Test
    void p4JumpGame() {
        for (int[] nums : new int[][] {{2, 3, 1, 1, 4}, {2, 3, 0, 1, 4}}) {
            assertEquals(2, new JumpGame().jump(nums));
            assertEquals(2, new JumpGameImproved().jump(nums));
        }
        assertEquals(0, new JumpGameImproved().jump(new int[] {0}));
        for (int t = 0; t < 500; t++) {
            int n = 1 + rng.nextInt(40);
            int[] nums = new int[n];
            int reach = 0;
            for (int i = 0; i < n; i++) {
                nums[i] = rng.nextInt(1 + rng.nextInt(6));
                if (i < n - 1 && reach <= i && nums[i] == 0) nums[i] = 1;
                reach = Math.max(reach, i + nums[i]);
            }
            assertEquals(new JumpGame().jump(nums), new JumpGameImproved().jump(nums), Arrays.toString(nums));
        }
        JumpGame basic = new JumpGame();
        int[] big = new int[300];
        Arrays.fill(big, 300);
        assertEquals(1, basic.jump(big));
        assertEquals(299L * 300 / 2, basic.steps);
    }

    @Test
    void p5OpenLock() {
        String[][] dead = {{"0201", "0101", "0102", "1212", "2002"}, {"8888"},
                {"8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"}, {"0000"}, {"0001"}};
        String[] target = {"0202", "0009", "8888", "8888", "0001"};
        int[] expected = {6, 1, -1, -1, -1};
        for (int i = 0; i < dead.length; i++) {
            assertEquals(expected[i], new OpenLock().openLock(dead[i], target[i]));
            assertEquals(expected[i], new OpenLockImproved().openLock(dead[i], target[i]));
        }
        for (int t = 0; t < 300; t++) {
            Set<String> d = new HashSet<>();
            for (int k = rng.nextInt(401); k > 0; k--) d.add(String.format("%04d", rng.nextInt(10000)));
            String goal = String.format("%04d", rng.nextInt(10000));
            String[] arr = d.toArray(new String[0]);
            assertEquals(new OpenLock().openLock(arr, goal), new OpenLockImproved().openLock(arr, goal), goal);
        }
    }
}
