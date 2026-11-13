"""LeetCode 752. Open the Lock — сайжруулсан (A төвшин): хоёр талын гүехэн хайлт.

1. Төлөвийг мөрийн оронд 0…9999 бүхэл тоогоор кодолж, хөршийг 10-ын зэргээр нэмж/хасаж
   олно (мөр зүсэх, шинэ мөр үүсгэх зардал алга). visited/dead нь 10⁴ урттай bytearray.
2. «0000» ба зорилгоос **хоёр талаас** BFS хийж, алхам бүрд **жижиг** хилийг нэг төвшин
   тэлнэ. Хоёр хил уулзмагц хариу = хоёр талын төвшний нийлбэр. Салбарлалт b, хариу d бол
   нэг талын BFS ≈ b^d төлөв, хоёр талынх ≈ 2·b^(d/2) төлөв нээнэ.
Хамгийн муу үед ч Θ(10⁴) төлөв, Θ(10⁴) санах ой.
"""
from typing import List

POW = (1000, 100, 10, 1)


def neighbours(x: int):
    for p in POW:
        digit = x // p % 10
        yield x + p if digit < 9 else x - 9 * p  # +1 (9 → 0)
        yield x - p if digit > 0 else x + 9 * p  # −1 (0 → 9)


class Solution:
    def __init__(self) -> None:
        self.expanded = 0  # тэлсэн төлөвийн тоо (хэмжилтэд)

    def openLock(self, deadends: List[str], target: str) -> int:
        dead = bytearray(10000)
        for d in deadends:
            dead[int(d)] = 1
        start, goal = 0, int(target)
        if dead[start] or dead[goal]:
            return -1
        if start == goal:
            return 0
        # side[x]: 0 — үзээгүй, 1 — эхлэлээс, 2 — зорилгоос хүрсэн
        side = bytearray(10000)
        side[start], side[goal] = 1, 2
        front = {1: [start], 2: [goal]}
        depth = {1: 0, 2: 0}
        while front[1] and front[2]:
            s = 1 if len(front[1]) <= len(front[2]) else 2  # жижиг хилийг тэлнэ
            other = 3 - s
            depth[s] += 1
            nxt = []
            for x in front[s]:
                self.expanded += 1
                for y in neighbours(x):
                    if dead[y] or side[y] == s:
                        continue
                    if side[y] == other:
                        return depth[1] + depth[2]
                    side[y] = s
                    nxt.append(y)
            front[s] = nxt
        return -1
