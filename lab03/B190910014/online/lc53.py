"""LeetCode 53. Maximum Subarray — https://leetcode.com/problems/maximum-subarray/"""
from typing import List


class SolutionDivideConquer:
    """Хэсэгчлэх арга: T(n) = 2T(n/2) + Θ(n) = Θ(n lg n)."""

    def maxSubArray(self, nums: List[int]) -> int:
        def best(lo: int, hi: int) -> int:  # nums[lo..hi]
            if lo == hi:
                return nums[lo]
            mid = (lo + hi) // 2
            # Дундуур огтолж гарах дэд массив: зүүн тал mid-ээс зүүн тийш, баруун тал mid+1-ээс баруун тийш.
            left_sum, s = float("-inf"), 0
            for i in range(mid, lo - 1, -1):
                s += nums[i]
                left_sum = max(left_sum, s)
            right_sum, s = float("-inf"), 0
            for j in range(mid + 1, hi + 1):
                s += nums[j]
                right_sum = max(right_sum, s)
            return max(best(lo, mid), best(mid + 1, hi), left_sum + right_sum)

        return best(0, len(nums) - 1)


class Solution:
    """Шугаман арга (Kadane): i-д төгсөх хамгийн их нийлбэрийг хадгална. Θ(n)."""

    def maxSubArray(self, nums: List[int]) -> int:
        ending_here = answer = nums[0]
        for v in nums[1:]:
            ending_here = max(v, ending_here + v)
            answer = max(answer, ending_here)
        return answer
