"""LeetCode 493. Reverse Pairs — https://leetcode.com/problems/reverse-pairs/"""
from typing import List


class Solution:
    """i < j, nums[i] > 2·nums[j] хосыг нэгтгэн эрэмбэлэх явцад тоолно. Θ(n lg n)."""

    def reversePairs(self, nums: List[int]) -> int:
        buf = [0] * len(nums)

        def sort_and_count(lo: int, hi: int) -> int:  # nums[lo:hi]
            if hi - lo < 2:
                return 0
            mid = (lo + hi) // 2
            count = sort_and_count(lo, mid) + sort_and_count(mid, hi)

            # Хоёр тал тус бүр эрэмбэлэгдсэн тул j заагч зөвхөн урагшилна.
            j = mid
            for i in range(lo, mid):
                while j < hi and nums[i] > 2 * nums[j]:
                    j += 1
                count += j - mid

            buf[lo:hi] = nums[lo:hi]
            i, j = lo, mid
            for k in range(lo, hi):
                if j >= hi or (i < mid and buf[i] <= buf[j]):
                    nums[k] = buf[i]
                    i += 1
                else:
                    nums[k] = buf[j]
                    j += 1
            return count

        return sort_and_count(0, len(nums))
