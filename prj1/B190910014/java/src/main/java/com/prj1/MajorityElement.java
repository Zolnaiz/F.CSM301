package com.prj1;

/** LeetCode 169. Хэсэгчлэх арга: T(n) = 2T(n/2) + Θ(n) = Θ(n lg n), нэмэлт санах ой Θ(lg n). */
public class MajorityElement {

    public int majorityElement(int[] nums) {
        return majority(nums, 0, nums.length);
    }

    /** nums[lo, hi)-ийн олонх гишүүн. */
    private int majority(int[] nums, int lo, int hi) {
        if (hi - lo == 1) return nums[lo];
        int mid = (lo + hi) >>> 1;
        int left = majority(nums, lo, mid);
        int right = majority(nums, mid, hi);
        if (left == right) return left;
        // Олонх гишүүн аль нэг хагаст заавал олонх байна — хоёр нэр дэвшигчийг тоолно.
        int leftCount = 0;
        int rightCount = 0;
        for (int i = lo; i < hi; i++) {
            if (nums[i] == left) leftCount++;
            else if (nums[i] == right) rightCount++;
        }
        return leftCount > rightCount ? left : right;
    }
}
