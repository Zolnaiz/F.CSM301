"""LeetCode 455. Assign Cookies — https://leetcode.com/problems/assign-cookies/"""
from typing import List


class Solution:
    """Хомхойлох арга: шуналын хэмжээ g ба жигнэмэгийн хэмжээ s-ийг эрэмбэлээд, хамгийн бага
    шуналтай хүүхдэд түүнийг хангах хамгийн жижиг жигнэмгийг өгнө (хоёр заагч).

    Θ(n lg n + m lg m) хугацаа (эрэмбэлэлт), заагчийн хэсэг Θ(n + m), нэмэлт санах ой Θ(1)
    (байрандаа эрэмбэлнэ).
    """

    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()
        s.sort()
        child = 0
        for cookie in s:
            if child < len(g) and cookie >= g[child]:
                child += 1
        return child
