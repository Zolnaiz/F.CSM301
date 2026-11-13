package com.prj2;

import java.util.Arrays;

/** LeetCode 45 (B төвшин). Динамик программчлал: dp[j] = min(dp[j], dp[i] + 1). O(n²), Θ(n) санах ой. */
public class JumpGame {

    /** dp-г шинэчилсэн тоо (хэмжилтэд). */
    public long steps = 0;

    public int jump(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[0] = 0;
        for (int i = 0; i < n - 1; i++) {
            if (dp[i] == Integer.MAX_VALUE) continue;
            int end = (int) Math.min(n - 1, (long) i + nums[i]);
            for (int j = i + 1; j <= end; j++) {
                steps++;
                if (dp[i] + 1 < dp[j]) dp[j] = dp[i] + 1;
            }
        }
        return dp[n - 1];
    }
}
