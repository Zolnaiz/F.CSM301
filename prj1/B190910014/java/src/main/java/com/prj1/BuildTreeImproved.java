package com.prj1;

import java.util.HashMap;
import java.util.Map;

/**
 * LeetCode 105 — сайжруулсан (A төвшин). inorder-ийн утга → товъёгийг тольд (HashMap) хадгалж
 * (хайлт Θ(1)), массив хуулахгүй, зөвхөн товъёгоор дамжуулна. Хугацаа, санах ой Θ(n).
 */
public class BuildTreeImproved {

    private int[] preorder;
    private Map<Integer, Integer> position;
    private int nextRoot;

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        this.preorder = preorder;
        this.position = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) position.put(inorder[i], i);
        this.nextRoot = 0;
        return build(0, inorder.length - 1);
    }

    /** inorder[lo..hi]-ийн мод. preorder-т зүүн дэд мод түрүүлж ирдэг. */
    private TreeNode build(int lo, int hi) {
        if (lo > hi) return null;
        int value = preorder[nextRoot++];
        int k = position.get(value);
        TreeNode root = new TreeNode(value);
        root.left = build(lo, k - 1);
        root.right = build(k + 1, hi);
        return root;
    }
}
