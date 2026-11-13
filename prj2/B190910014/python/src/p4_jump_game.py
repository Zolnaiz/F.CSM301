"""LeetCode 45. Jump Game II (B төвшин) — https://leetcode.com/problems/jump-game-ii/

Динамик программчлал: dp[i] — 0-ээс i-д хүрэх хамгийн цөөн үсрэлт.
dp[j] = min(dp[j], dp[i] + 1), j = i+1 … i+nums[i]. Хугацаа O(n · max nums[i]) ≤ O(n²),
санах ой Θ(n).
"""
from typing import List


class Solution:
    def __init__(self) -> None:
        self.steps = 0  # dp-г шинэчилсэн тоо (хэмжилтэд)

    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        inf = n
        dp = [inf] * n
        dp[0] = 0
        for i in range(n - 1):
            if dp[i] == inf:
                continue
            nxt = dp[i] + 1
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                self.steps += 1
                if nxt < dp[j]:
                    dp[j] = nxt
        return dp[-1]
