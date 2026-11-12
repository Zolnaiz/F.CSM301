"""LeetCode 105 — сайжруулсан (A төвшин).

1. inorder-ийн утга → товъёгийг тольд (dict) нэг удаа хадгална: хайлт Θ(1).
2. Жагсаалт хуулахгүй, зөвхөн товъёгоор дамжуулна; preorder-ийг нэг заагчаар уншина.
Хугацаа ба санах ой Θ(n) (дахин дуудалтын стек модны өндөр h ≤ n).
"""
import sys
from typing import List, Optional

try:
    TreeNode  # LeetCode дээр урьдчилан тодорхойлогдсон
except NameError:
    from src.tree_node import TreeNode

sys.setrecursionlimit(20000)


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        position = {value: i for i, value in enumerate(inorder)}
        next_root = 0  # preorder-оос дараагийн үндсийг уншина

        def build(lo: int, hi: int) -> Optional[TreeNode]:  # inorder[lo..hi]
            nonlocal next_root
            if lo > hi:
                return None
            value = preorder[next_root]
            next_root += 1
            k = position[value]
            root = TreeNode(value)
            root.left = build(lo, k - 1)  # preorder-т зүүн дэд мод түрүүлж ирдэг
            root.right = build(k + 1, hi)
            return root

        return build(0, len(inorder) - 1)
