package com.prj1;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.*;
import org.junit.jupiter.api.*;

class ProblemsTest {

    private final Random rng = new Random(2026);

    // --- туслах функцүүд ---------------------------------------------------
    static List<Integer> inorder(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = node.left; }
            node = stack.pop();
            out.add(node.val);
            node = node.right;
        }
        return out;
    }

    static List<Integer> preorder(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            out.add(node.val);
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
        }
        return out;
    }

    /** Өндөр, тэнцвэргүй бол -1. */
    static int balancedHeight(TreeNode node) {
        if (node == null) return 0;
        int l = balancedHeight(node.left);
        int r = balancedHeight(node.right);
        if (l < 0 || r < 0 || Math.abs(l - r) > 1) return -1;
        return Math.max(l, r) + 1;
    }

    // --- 1. Majority Element ----------------------------------------------
    @Test
    void p1Majority() {
        MajorityElement s = new MajorityElement();
        assertEquals(3, s.majorityElement(new int[] {3, 2, 3}));
        assertEquals(2, s.majorityElement(new int[] {2, 2, 1, 1, 1, 2, 2}));
        for (int t = 0; t < 300; t++) {
            int n = 1 + rng.nextInt(60);
            int major = rng.nextInt(11) - 5;
            int k = n / 2 + 1 + rng.nextInt(n - n / 2);
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < n; i++) list.add(i < k ? major : rng.nextInt(11) - 5);
            Collections.shuffle(list, rng);
            int[] nums = list.stream().mapToInt(Integer::intValue).toArray();
            Map<Integer, Long> cnt = list.stream().collect(Collectors.groupingBy(x -> x, Collectors.counting()));
            int expected = Collections.max(cnt.entrySet(), Map.Entry.comparingByValue()).getKey();
            assertEquals(expected, s.majorityElement(nums));
        }
    }

    // --- 2. Sorted Array to BST -------------------------------------------
    @Test
    void p2BalancedBst() {
        for (int n : new int[] {0, 1, 2, 3, 7, 8, 100, 1000}) {
            int[] nums = IntStream.range(0, n).map(i -> 3 * i - 50).toArray();
            TreeNode root = new SortedArrayToBst().sortedArrayToBST(nums);
            assertEquals(Arrays.stream(nums).boxed().toList(), inorder(root), "n=" + n);
            int h = balancedHeight(root);
            assertEquals(32 - Integer.numberOfLeadingZeros(n), h, "n=" + n); // ⌈lg(n+1)⌉
        }
    }

    // --- 3. Longest Nice Substring ----------------------------------------
    static String niceBrute(String s) {
        String best = "";
        for (int i = 0; i < s.length(); i++) {
            for (int j = i + 1; j <= s.length(); j++) {
                String t = s.substring(i, j);
                if (t.length() > best.length() && t.chars().allMatch(c -> t.indexOf(
                        Character.isUpperCase(c) ? Character.toLowerCase(c) : Character.toUpperCase(c)) >= 0)) {
                    best = t;
                }
            }
        }
        return best;
    }

    @Test
    void p3Nice() {
        LongestNiceSubstring s = new LongestNiceSubstring();
        assertEquals("aAa", s.longestNiceSubstring("YazaAay"));
        assertEquals("Bb", s.longestNiceSubstring("Bb"));
        assertEquals("", s.longestNiceSubstring("c"));
        assertEquals("dD", s.longestNiceSubstring("dDzeE"));
        String alphabet = "aAbBcC";
        for (int t = 0; t < 2000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rng.nextInt(15);
            for (int i = 0; i < len; i++) sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
            String str = sb.toString();
            assertEquals(niceBrute(str), s.longestNiceSubstring(str), str);
        }
    }

    // --- 4. Different Ways to Add Parentheses -----------------------------
    static final long[] CATALAN = {1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862};

    @Test
    void p4Examples() {
        for (boolean improved : new boolean[] {false, true}) {
            List<Integer> a = improved ? new DifferentWaysImproved().diffWaysToCompute("2*3-4*5")
                    : new DifferentWays().diffWaysToCompute("2*3-4*5");
            assertEquals(List.of(-34, -14, -10, -10, 10), a.stream().sorted().toList());
        }
    }

    @Test
    void p4ImprovedMatchesBasic() {
        for (int k = 0; k < 9; k++) {
            for (int t = 0; t < 5; t++) {
                StringBuilder sb = new StringBuilder().append(rng.nextInt(100));
                for (int i = 0; i < k; i++) sb.append("+-*".charAt(rng.nextInt(3))).append(rng.nextInt(100));
                String expr = sb.toString();
                DifferentWays basic = new DifferentWays();
                DifferentWaysImproved improved = new DifferentWaysImproved();
                List<Integer> a = basic.diffWaysToCompute(expr).stream().sorted().toList();
                List<Integer> b = improved.diffWaysToCompute(expr).stream().sorted().toList();
                assertEquals(a, b, expr);
                assertEquals(CATALAN[k], b.size(), expr);
                assertEquals((long) Math.pow(3, k), basic.calls, expr); // C(k) = 1 + 2·ΣC(j) = 3^k
                assertEquals((long) (k + 1) * (k + 2) / 2, improved.calls, expr);
            }
        }
    }

    // --- 5. Construct Binary Tree -----------------------------------------
    TreeNode randomTree(List<Integer> vals) {
        if (vals.isEmpty()) return null;
        int k = rng.nextInt(vals.size());
        return new TreeNode(vals.get(k), randomTree(vals.subList(0, k)), randomTree(vals.subList(k + 1, vals.size())));
    }

    static TreeNode chain(int n) {
        TreeNode root = null;
        for (int v = 0; v < n; v++) root = new TreeNode(v, root, null);
        return root;
    }

    @Test
    void p5BuildTree() {
        List<TreeNode> trees = new ArrayList<>();
        for (int t = 0; t < 200; t++) {
            List<Integer> vals = new ArrayList<>();
            for (int v = -3000; v <= 3000; v++) vals.add(v);
            Collections.shuffle(vals, rng);
            trees.add(randomTree(vals.subList(0, rng.nextInt(61))));
        }
        trees.add(chain(2000));
        for (TreeNode tree : trees) {
            int[] pre = preorder(tree).stream().mapToInt(Integer::intValue).toArray();
            int[] ino = inorder(tree).stream().mapToInt(Integer::intValue).toArray();
            for (TreeNode root : new TreeNode[] {new BuildTree().buildTree(pre, ino),
                                                 new BuildTreeImproved().buildTree(pre, ino)}) {
                assertEquals(preorder(tree), preorder(root));
                assertEquals(inorder(tree), inorder(root));
            }
        }
    }
}
