package com.prj1;

import java.util.Arrays;

/**
 * LeetCode 105 (B төвшин). preorder[0] нь үндэс; түүнийг inorder-оос шугаман хайлтаар олж,
 * массивыг хуулж хуваана. Хамгийн муу үед T(n) = T(n−1) + Θ(n) = Θ(n²) хугацаа, санах ой.
 */
public class BuildTree {

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder.length == 0) return null;
        TreeNode root = new TreeNode(preorder[0]);
        int k = 0;
        while (inorder[k] != preorder[0]) k++; // Θ(n) хайлт
        root.left = buildTree(Arrays.copyOfRange(preorder, 1, k + 1), Arrays.copyOfRange(inorder, 0, k));
        root.right = buildTree(Arrays.copyOfRange(preorder, k + 1, preorder.length),
                Arrays.copyOfRange(inorder, k + 1, inorder.length));
        return root;
    }
}
