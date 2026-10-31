package com.prj1;

/** LeetCode 108. Дунд гишүүнийг үндэс болгоно: T(n) = 2T(n/2) + Θ(1) = Θ(n). */
public class SortedArrayToBst {

    public TreeNode sortedArrayToBST(int[] nums) {
        return build(nums, 0, nums.length - 1);
    }

    /** nums[lo..hi]-аас тэнцвэртэй хайлтын мод. */
    private TreeNode build(int[] nums, int lo, int hi) {
        if (lo > hi) return null;
        int mid = (lo + hi) >>> 1;
        return new TreeNode(nums[mid], build(nums, lo, mid - 1), build(nums, mid + 1, hi));
    }
}
