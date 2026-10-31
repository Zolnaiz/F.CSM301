from __future__ import annotations

from typing import Optional


class TreeNode:
    """LeetCode-ийн хоёртын модны зангилаа."""

    def __init__(self, val: int = 0, left: Optional[TreeNode] = None,
                 right: Optional[TreeNode] = None):
        self.val = val
        self.left = left
        self.right = right


def inorder(root: Optional[TreeNode]) -> list[int]:
    out, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out


def preorder(root: Optional[TreeNode]) -> list[int]:
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out


def height(root: Optional[TreeNode]) -> int:
    """Модны өндөр (хоосон мод 0). Давталтаар тул гүн модонд ч ажиллана."""
    best, stack = 0, [(root, 1)] if root else []
    while stack:
        node, depth = stack.pop()
        best = max(best, depth)
        for child in (node.left, node.right):
            if child:
                stack.append((child, depth + 1))
    return best


def is_balanced(root: Optional[TreeNode]) -> bool:
    """Зангилаа бүрийн хоёр дэд модны өндрийн зөрүү ≤ 1 эсэх."""
    def check(node: Optional[TreeNode]) -> int:  # өндөр, тэнцвэргүй бол -1
        if node is None:
            return 0
        lh, rh = check(node.left), check(node.right)
        if lh < 0 or rh < 0 or abs(lh - rh) > 1:
            return -1
        return max(lh, rh) + 1

    return check(root) >= 0
