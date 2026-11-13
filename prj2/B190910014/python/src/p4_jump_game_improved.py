"""LeetCode 45. Jump Game II — сайжруулсан (A төвшин): хомхойлох арга = далд гүехэн хайлт.

k үсрэлтээр хүрч болох байрлалууд нь тасралтгүй муж [lo, hi] үүсгэнэ (BFS-ийн k-р төвшин).
Дараагийн төвшний хамгийн хол хүрэх цэг нь max(i + nums[i]), i ∈ [lo, hi]. Иймд төвшин бүрээс
«хамгийн хол хүргэх» байрлалыг сонгох нь хомхойлох сонголт бөгөөд массивыг нэг гүйнэ.
Θ(n) хугацаа, Θ(1) санах ой.
"""
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = 0
        current_end = 0  # одоогийн төвшний (jumps үсрэлтээр хүрэх) хамгийн хол байрлал
        farthest = 0     # дараагийн төвшний хамгийн хол байрлал
        for i in range(len(nums) - 1):
            if i + nums[i] > farthest:
                farthest = i + nums[i]
            if i == current_end:  # энэ төвшин дууслаа — нэг үсрэлт нэмнэ
                jumps += 1
                current_end = farthest
                if current_end >= len(nums) - 1:
                    break
        return jumps
