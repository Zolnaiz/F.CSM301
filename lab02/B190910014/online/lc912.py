"""LeetCode 912. Sort an Array — https://leetcode.com/problems/sort-an-array/"""
from typing import List


class SolutionInsertion:
    """1-р оролдлого: зөөх эрэмбэлэлт, Θ(n^2). n = 5·10^4 үед хугацаа хэтэрнэ."""

    def sortArray(self, nums: List[int]) -> List[int]:
        for i in range(1, len(nums)):
            key = nums[i]
            j = i - 1
            while j >= 0 and nums[j] > key:
                nums[j + 1] = nums[j]
                j -= 1
            nums[j + 1] = key
        return nums


class Solution:
    """2-р оролдлого: нэгтгэн эрэмбэлэлт, Θ(n lg n) хугацаа, Θ(n) нэмэлт санах ой."""

    def sortArray(self, nums: List[int]) -> List[int]:
        buf = [0] * len(nums)

        def merge_sort(lo: int, hi: int) -> None:  # nums[lo:hi]
            if hi - lo < 2:
                return
            mid = (lo + hi) // 2
            merge_sort(lo, mid)
            merge_sort(mid, hi)
            buf[lo:hi] = nums[lo:hi]
            i, j = lo, mid
            for k in range(lo, hi):
                if j >= hi or (i < mid and buf[i] <= buf[j]):
                    nums[k] = buf[i]
                    i += 1
                else:
                    nums[k] = buf[j]
                    j += 1

        merge_sort(0, len(nums))
        return nums
