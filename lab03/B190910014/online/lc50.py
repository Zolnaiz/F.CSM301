"""LeetCode 50. Pow(x, n) — https://leetcode.com/problems/powx-n/"""


class Solution:
    """Хэсэгчлэх арга: xⁿ = (x^(n/2))² (· x). T(n) = T(n/2) + Θ(1) = Θ(lg n)."""

    def myPow(self, x: float, n: int) -> float:
        def power(k: int) -> float:  # k ≥ 0
            if k == 0:
                return 1.0
            half = power(k // 2)  # дэд бодлогыг ганцхан удаа бодно
            return half * half if k % 2 == 0 else half * half * x

        # n сөрөг бол x⁻ⁿ = (1/x)ⁿ. Python-ы int халихгүй тул -n аюулгүй.
        return power(n) if n >= 0 else 1.0 / power(-n)
