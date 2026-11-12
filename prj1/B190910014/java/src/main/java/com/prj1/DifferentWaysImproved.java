package com.prj1;

import java.util.ArrayList;
import java.util.List;

/**
 * LeetCode 241 — сайжруулсан (A төвшин). Илэрхийллийг нэг удаа задалж, дэд бодлогыг операндын
 * товъёгийн муж (i, j)-ээр тодорхойлж, хариуг санана. Өөр дэд бодлого (k+1)(k+2)/2.
 */
public class DifferentWaysImproved {

    /** memo-д байхгүй үед бодсон дэд бодлогын тоо (хэмжилтэд). */
    public long calls = 0;

    private int[] nums;
    private char[] ops;
    private List<Integer>[][] memo;

    @SuppressWarnings("unchecked")
    public List<Integer> diffWaysToCompute(String expression) {
        List<Integer> numList = new ArrayList<>();
        StringBuilder opList = new StringBuilder();
        int value = 0;
        for (char ch : expression.toCharArray()) {
            if (Character.isDigit(ch)) {
                value = value * 10 + (ch - '0');
            } else {
                numList.add(value);
                opList.append(ch);
                value = 0;
            }
        }
        numList.add(value);
        nums = numList.stream().mapToInt(Integer::intValue).toArray();
        ops = opList.toString().toCharArray();
        memo = new List[nums.length][nums.length];
        return compute(0, nums.length - 1);
    }

    /** nums[i..j] операндуудад хаалт тавих бүх аргын утга. */
    private List<Integer> compute(int i, int j) {
        if (memo[i][j] != null) return memo[i][j];
        calls++;
        List<Integer> result = new ArrayList<>();
        if (i == j) {
            result.add(nums[i]);
        } else {
            for (int k = i; k < j; k++) { // ops[k] нь nums[k], nums[k+1]-ийн хооронд
                for (int x : compute(i, k)) {
                    for (int y : compute(k + 1, j)) result.add(DifferentWays.apply(x, y, ops[k]));
                }
            }
        }
        memo[i][j] = result;
        return result;
    }
}
