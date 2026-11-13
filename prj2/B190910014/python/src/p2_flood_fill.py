"""LeetCode 733. Flood Fill — https://leetcode.com/problems/flood-fill/"""
from collections import deque
from typing import List


class Solution:
    """Гүехэн хайлт (BFS): эхлэх нүднээс ижил өнгөтэй 4 хөршөөр тархана.

    Нүд бүр дараалалд нэг л удаа орно: өнгийг дараалалд оруулах үед нь сольдог тул дахин
    орохгүй. Θ(R·C) хугацаа, дараалал хамгийн ихдээ Θ(R·C) санах ой. Шинэ өнгө хуучинтайгаа
    ижил бол юу ч хийхгүй (эс бөгөөс зогсохгүй давтагдана).
    """

    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        old = image[sr][sc]
        if old == color:
            return image
        rows, cols = len(image), len(image[0])
        image[sr][sc] = color
        queue = deque([(sr, sc)])
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == old:
                    image[nr][nc] = color
                    queue.append((nr, nc))
        return image


class SolutionDfs:
    """Гүн хайлт (DFS) — дахин дуудалтын оронд тодорхой стек (Python-ы стекийн хязгаараас сэргийлнэ)."""

    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        old = image[sr][sc]
        if old == color:
            return image
        rows, cols = len(image), len(image[0])
        image[sr][sc] = color
        stack = [(sr, sc)]
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == old:
                    image[nr][nc] = color
                    stack.append((nr, nc))
        return image
