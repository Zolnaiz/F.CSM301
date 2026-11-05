"""LeetCode 300. Longest Increasing Subsequence —
https://leetcode.com/problems/longest-increasing-subsequence/
"""
from typing import List


class SolutionQuadratic:
    """1-р хувилбар: lis[i] — nums[i]-ээр төгсөх хамгийн урт өсөх дэд дараалал.

    lis[i] = 1 + max{lis[j] : j < i, nums[j] < nums[i]}. Хугацаа Θ(n²), санах ой Θ(n).
    """

    def lengthOfLIS(self, nums: List[int]) -> int:
        lis = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i] and lis[j] + 1 > lis[i]:
                    lis[i] = lis[j] + 1
        return max(lis)


class Solution:
    """2-р хувилбар (сайжруулсан): tails[L] — L+1 урттай өсөх дэд дарааллын хамгийн бага сүүл.

    tails өсөх эрэмбэтэй байдаг тул x бүрд x ≤ tails[k] байх хамгийн бага k-г хоёртын хайлтаар
    олж солино (эсвэл төгсгөлд нэмнэ). Хугацаа Θ(n lg n), санах ой Θ(n).
    """

    def lengthOfLIS(self, nums: List[int]) -> int:
        tails: list[int] = []
        for x in nums:
            lo, hi = 0, len(tails)
            while lo < hi:  # x ≤ tails[k] байх хамгийн бага k
                mid = (lo + hi) // 2
                if tails[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            if lo == len(tails):
                tails.append(x)
            else:
                tails[lo] = x
        return len(tails)
