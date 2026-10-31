"""LeetCode 241. Different Ways to Add Parentheses (B түвшин) —
https://leetcode.com/problems/different-ways-to-add-parentheses/
"""
from typing import List


def apply(x: int, y: int, op: str) -> int:
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    return x * y


class Solution:
    """Үйлдэл бүрээр хоёр хувааж, хоёр талын бүх хариуг хослуулна.

    Ижил дэд илэрхийллийг олон дахин бодно, мөн дэд мөрийг хуулна.
    """

    def __init__(self) -> None:
        self.calls = 0  # дахин дуудалтын тоо (хэмжилтэд)

    def diffWaysToCompute(self, expression: str) -> List[int]:
        self.calls += 1
        results = []
        for i, ch in enumerate(expression):
            if ch in "+-*":
                left = self.diffWaysToCompute(expression[:i])
                right = self.diffWaysToCompute(expression[i + 1:])
                for x in left:
                    for y in right:
                        results.append(apply(x, y, ch))
        if not results:  # үйлдэлгүй — ганц тоо
            results.append(int(expression))
        return results
