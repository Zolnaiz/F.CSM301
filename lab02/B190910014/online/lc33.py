"""LeetCode 33. Search in Rotated Sorted Array —
https://leetcode.com/problems/search-in-rotated-sorted-array/
"""
from typing import List


class Solution:
    """Хөрвүүлсэн жагсаалтад хоёртын хайлт. Θ(lg n)."""

    def search(self, nums: List[int], target: int) -> int:
        def find(p: int, r: int) -> int:
            if p > r:
                return -1
            q = (p + r) // 2
            if nums[q] == target:
                return q
            if nums[p] <= nums[q]:
                # Зүүн тал nums[p..q] эрэмбэлэгдсэн.
                if nums[p] <= target < nums[q]:
                    return find(p, q - 1)
                return find(q + 1, r)
            # Баруун тал nums[q..r] эрэмбэлэгдсэн.
            if nums[q] < target <= nums[r]:
                return find(q + 1, r)
            return find(p, q - 1)

        return find(0, len(nums) - 1)
