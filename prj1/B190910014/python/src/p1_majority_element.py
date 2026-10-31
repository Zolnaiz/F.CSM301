"""LeetCode 169. Majority Element — https://leetcode.com/problems/majority-element/"""
from typing import List


class Solution:
    """Хэсэгчлэх арга. T(n) = 2T(n/2) + Θ(n) = Θ(n lg n), нэмэлт санах ой Θ(lg n)."""

    def majorityElement(self, nums: List[int]) -> int:
        def majority(lo: int, hi: int) -> int:  # nums[lo:hi]-ийн олонх гишүүн
            if hi - lo == 1:
                return nums[lo]
            mid = (lo + hi) // 2
            left = majority(lo, mid)
            right = majority(mid, hi)
            if left == right:
                return left
            # Олонх гишүүн аль нэг хагаст заавал олонх байна — хоёр нэр дэвшигчийг тоолно.
            left_count = sum(1 for i in range(lo, hi) if nums[i] == left)
            right_count = sum(1 for i in range(lo, hi) if nums[i] == right)
            return left if left_count > right_count else right

        return majority(0, len(nums))
