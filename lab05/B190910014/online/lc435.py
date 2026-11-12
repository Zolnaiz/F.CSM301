"""LeetCode 435 — Non-overlapping Intervals. https://leetcode.com/problems/non-overlapping-intervals/

Хасах хамгийн цөөн интервал = n − (давхцалгүй хамгийн олон интервал). Сүүлийнх нь яг
ажиллагааг түүвэрлэх бодлого (1-р бодлого): төгсгөлөөр эрэмбэлээд хамгийн эрт дуусахыг
сонгоно. [1, 2] ба [2, 3] давхцахгүй. Θ(n lg n) хугацаа, эрэмбэлэлтээс бусад нь Θ(1) санах ой.
"""
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda iv: iv[1])
        kept = 0
        end = float("-inf")
        for start, finish in intervals:
            if start >= end:
                kept += 1
                end = finish
        return len(intervals) - kept
