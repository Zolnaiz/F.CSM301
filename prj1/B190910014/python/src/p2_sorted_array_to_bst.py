"""LeetCode 108. Convert Sorted Array to Binary Search Tree —
https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/
"""
from typing import List, Optional

try:
    TreeNode  # LeetCode дээр урьдчилан тодорхойлогдсон
except NameError:
    from src.tree_node import TreeNode


class Solution:
    """Дунд гишүүнийг үндэс болгож хоёр талыг дахин дуудна. T(n) = 2T(n/2) + Θ(1) = Θ(n)."""

    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def build(lo: int, hi: int) -> Optional[TreeNode]:  # nums[lo..hi]
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(nums[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(nums) - 1)
