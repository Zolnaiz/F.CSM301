import random
from collections import Counter
from itertools import product

import pytest

from src.p1_majority_element import Solution as Majority
from src.p2_sorted_array_to_bst import Solution as SortedToBst
from src.p3_longest_nice_substring import Solution as Nice
from src.p4_different_ways import Solution as Ways
from src.p4_different_ways_improved import Solution as WaysImproved
from src.p5_build_tree import Solution as BuildTree
from src.p5_build_tree_improved import Solution as BuildTreeImproved
from src.tree_node import TreeNode, height, inorder, is_balanced, preorder

rng = random.Random(2026)


# --- 1. Majority Element -------------------------------------------------
@pytest.mark.parametrize("nums,expected", [([3, 2, 3], 3), ([2, 2, 1, 1, 1, 2, 2], 2), ([7], 7)])
def test_p1_examples(nums, expected):
    assert Majority().majorityElement(nums) == expected


def test_p1_random_against_counter():
    for _ in range(300):
        n = rng.randint(1, 60)
        major = rng.randint(-5, 5)
        k = n // 2 + 1 + rng.randint(0, n - n // 2 - 1)
        nums = [major] * k + [rng.randint(-5, 5) for _ in range(n - k)]
        rng.shuffle(nums)
        assert Majority().majorityElement(nums) == Counter(nums).most_common(1)[0][0]


# --- 2. Sorted Array to BST ----------------------------------------------
@pytest.mark.parametrize("n", [0, 1, 2, 3, 7, 8, 100, 1000])
def test_p2_is_balanced_bst(n):
    nums = sorted(rng.sample(range(-10_000, 10_000), n))
    root = SortedToBst().sortedArrayToBST(nums)
    assert inorder(root) == nums          # хайлтын мод: inorder нь эрэмбэлэгдсэн
    assert is_balanced(root)
    assert height(root) == n.bit_length()  # хамгийн бага өндөр ⌈lg(n+1)⌉


# --- 3. Longest Nice Substring -------------------------------------------
def nice_brute(s: str) -> str:
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]
            if len(t) > len(best) and all(c.swapcase() in t for c in t):
                best = t
    return best


@pytest.mark.parametrize("s,expected", [("YazaAay", "aAa"), ("Bb", "Bb"), ("c", ""), ("dDzeE", "dD")])
def test_p3_examples(s, expected):
    assert Nice().longestNiceSubstring(s) == expected


def test_p3_random_against_brute():
    for _ in range(2000):
        s = "".join(rng.choice("aAbBcC") for _ in range(rng.randint(0, 14)))
        assert Nice().longestNiceSubstring(s) == nice_brute(s), s


# --- 4. Different Ways to Add Parentheses --------------------------------
def random_expression(k: int) -> str:
    parts = [str(rng.randint(0, 99))]
    for _ in range(k):
        parts += [rng.choice("+-*"), str(rng.randint(0, 99))]
    return "".join(parts)


@pytest.mark.parametrize("solution", [Ways, WaysImproved])
@pytest.mark.parametrize(
    "expr,expected",
    [("2-1-1", [0, 2]), ("2*3-4*5", [-34, -14, -10, -10, 10]), ("11", [11])],
)
def test_p4_examples(solution, expr, expected):
    assert sorted(solution().diffWaysToCompute(expr)) == expected


CATALAN = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]


def test_p4_improved_matches_basic():
    for k in range(0, 9):
        for _ in range(5):
            expr = random_expression(k)
            basic, improved = Ways(), WaysImproved()
            a = basic.diffWaysToCompute(expr)
            b = improved.diffWaysToCompute(expr)
            assert sorted(a) == sorted(b)
            assert len(b) == CATALAN[k]  # хаалт тавих аргын тоо = Каталаны тоо
            assert basic.calls == 3 ** k  # C(k) = 1 + 2·ΣC(j) = 3^k
            assert improved.calls == (k + 1) * (k + 2) // 2  # дэд бодлого бүрийг 1 удаа


# --- 5. Construct Binary Tree --------------------------------------------
def random_tree(n: int) -> TreeNode | None:
    """Ялгаатай утгатай санамсаргүй хэлбэрийн мод."""
    values = rng.sample(range(-3000, 3001), n)

    def make(vals):
        if not vals:
            return None
        k = rng.randrange(len(vals))
        return TreeNode(vals[k], make(vals[:k]), make(vals[k + 1:]))

    return make(values)


def chain(n: int) -> TreeNode | None:
    """Зөвхөн зүүн хүүхэдтэй (нэг талдаа тулсан) мод — хамгийн муу тохиолдол."""
    root = None
    for v in range(n):
        root = TreeNode(v, root, None)
    return root


@pytest.mark.parametrize("solution", [BuildTree, BuildTreeImproved])
def test_p5_example(solution):
    root = solution().buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    assert preorder(root) == [3, 9, 20, 15, 7]
    assert inorder(root) == [9, 3, 15, 20, 7]


@pytest.mark.parametrize("solution", [BuildTree, BuildTreeImproved])
def test_p5_random_and_chain(solution):
    trees = [random_tree(rng.randint(0, 60)) for _ in range(200)] + [chain(2000)]
    for tree in trees:
        pre, ino = preorder(tree), inorder(tree)
        root = solution().buildTree(pre, ino)
        assert preorder(root) == pre and inorder(root) == ino
