"""LeetCode 241. Different Ways to Add Parentheses — сайжруулсан (A төвшин).

1. Илэрхийллийг нэг удаа тоо, үйлдлийн жагсаалт болгон задална (дэд мөр хуулахгүй).
2. Дэд бодлогыг операндын товъёгийн муж (i, j)-ээр тодорхойлж, хариуг санана (memo).
   k үйлдэлтэй илэрхийлэлд ердөө (k+1)(k+2)/2 өөр дэд бодлого бий.
"""
from typing import List


def apply(x: int, y: int, op: str) -> int:
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    return x * y


class Solution:
    def __init__(self) -> None:
        self.calls = 0  # memo-д байхгүй үед бодсон дэд бодлогын тоо (хэмжилтэд)

    def diffWaysToCompute(self, expression: str) -> List[int]:
        nums: list[int] = []
        ops: list[str] = []
        value = 0
        for ch in expression:
            if ch.isdigit():
                value = value * 10 + int(ch)
            else:
                nums.append(value)
                ops.append(ch)
                value = 0
        nums.append(value)

        memo: dict[tuple[int, int], list[int]] = {}

        def compute(i: int, j: int) -> list[int]:  # nums[i..j] операндууд
            if (i, j) in memo:
                return memo[(i, j)]
            self.calls += 1
            if i == j:
                result = [nums[i]]
            else:
                result = []
                for k in range(i, j):  # ops[k] нь nums[k], nums[k+1]-ийн хооронд
                    for x in compute(i, k):
                        for y in compute(k + 1, j):
                            result.append(apply(x, y, ops[k]))
            memo[(i, j)] = result
            return result

        return compute(0, len(nums) - 1)
