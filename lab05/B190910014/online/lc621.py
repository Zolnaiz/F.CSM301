"""LeetCode 621 — Task Scheduler. https://leetcode.com/problems/task-scheduler/

Хамгийн олон давтагдсан ажлын тоо f, ийм ажлын төрлийн тоо c бол хариу
max(len(tasks), (f − 1)·(n + 1) + c). Хамгийн олон ажлыг (n + 1) урттай f − 1 «хүрээ» болгон
тавиад, сүүлийн хүрээнд c ажил үлдэнэ. Бусад ажлыг хоосон зайд хомхойлон дүүргэнэ. Зай
хүрэхгүй бол хоосон зай огт хэрэггүй тул хариу нь len(tasks). Θ(N) хугацаа, Θ(1) санах ой.
"""
from collections import Counter
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        counts = Counter(tasks).values()
        f = max(counts)
        c = sum(1 for x in counts if x == f)
        return max(len(tasks), (f - 1) * (n + 1) + c)


class SolutionSimulation:
    """Шалгах зорилготой: алхам бүрд үлдсэн тоо нь хамгийн их, хүлээх шаардлагагүй ажлыг
    хийх хомхойлох симуляц (heap + хүлээлгийн дараалал). O(хариу · lg 26)."""

    def leastInterval(self, tasks: List[str], n: int) -> int:
        import heapq
        from collections import deque

        heap = [-x for x in Counter(tasks).values()]
        heapq.heapify(heap)
        waiting: deque[tuple[int, int]] = deque()  # (үлдсэн тоо, дахин боломжтой болох хугацаа)
        time = 0
        while heap or waiting:
            time += 1
            if heap:
                left = heapq.heappop(heap) + 1
                if left:
                    waiting.append((left, time + n))
            if waiting and waiting[0][1] == time:
                heapq.heappush(heap, waiting.popleft()[0])
        return time
