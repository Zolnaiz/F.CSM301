package com.prj2;

/**
 * LeetCode 45 — сайжруулсан (A төвшин). Хомхойлох арга = далд BFS: k үсрэлтээр хүрэх байрлалууд
 * тасралтгүй муж бөгөөд төвшин дуусах бүрд хамгийн хол хүрэх цэг уруу шилжинэ. Θ(n), Θ(1) санах ой.
 */
public class JumpGameImproved {

    public int jump(int[] nums) {
        int jumps = 0;
        int currentEnd = 0;
        int farthest = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == currentEnd) { // энэ төвшин дууслаа
                jumps++;
                currentEnd = farthest;
                if (currentEnd >= nums.length - 1) break;
            }
        }
        return jumps;
    }
}
