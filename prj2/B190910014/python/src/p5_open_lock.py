"""LeetCode 752. Open the Lock (B төвшин) — https://leetcode.com/problems/open-the-lock/

Гүехэн хайлт (BFS): «0000»-оос эхэлж, төвшин бүрд дугуй бүрийг ±1 эргүүлсэн 8 хөршийг
нэмнэ. Түгжих хослол (deadends) уруу орохгүй. BFS анх хүрсэн төвшин нь хамгийн цөөн эргүүлэлт.
Төлөв (мөр) 10⁴, ирмэг 8·10⁴ тул O(10⁴ · 8 · 4) хугацаа, Θ(10⁴) санах ой.
"""
from collections import deque
from typing import List


class Solution:
    def __init__(self) -> None:
        self.expanded = 0  # дарааллаас гаргасан төлөвийн тоо (хэмжилтэд)

    def openLock(self, deadends: List[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead:
            return -1
        if target == "0000":
            return 0
        seen = {"0000"}
        queue = deque([("0000", 0)])
        while queue:
            state, dist = queue.popleft()
            self.expanded += 1
            for i in range(4):
                digit = int(state[i])
                for d in (-1, 1):
                    nxt = state[:i] + str((digit + d) % 10) + state[i + 1:]
                    if nxt in seen or nxt in dead:  # зорилго өөрөө түгжих хослол бол хүрэхгүй
                        continue
                    if nxt == target:
                        return dist + 1
                    seen.add(nxt)
                    queue.append((nxt, dist + 1))
        return -1
