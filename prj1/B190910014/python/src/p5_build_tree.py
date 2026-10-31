"""LeetCode 105. Construct Binary Tree from Preorder and Inorder Traversal (B түвшин) —
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
"""
import sys
from typing import List, Optional

try:
    TreeNode  # LeetCode дээр урьдчилан тодорхойлогдсон
except NameError:
    from src.tree_node import TreeNode

sys.setrecursionlimit(20000)


class Solution:
    """preorder[0] нь үндэс. Түүнийг inorder-оос шугаман хайлтаар олж, жагсаалтыг хуулж хуваана.

    Хамгийн муу (нэг талдаа тулсан мод): T(n) = T(n−1) + Θ(n) = Θ(n²) хугацаа, санах ой.
    """

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None
        root = TreeNode(preorder[0])
        k = inorder.index(preorder[0])  # Θ(n) хайлт
        root.left = self.buildTree(preorder[1:k + 1], inorder[:k])
        root.right = self.buildTree(preorder[k + 1:], inorder[k + 1:])
        return root
