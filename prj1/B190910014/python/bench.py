"""Бие даалт 1-ийн хэмжилт: хугацаа (ms) ба санах ойн оргил (KB, tracemalloc).

Ажиллуулах (prj1/B190910014/python хавтаснаас): python3 bench.py
Үр дүн: ../out/results_python.tsv
"""
import random
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

from src.p1_majority_element import Solution as Majority
from src.p2_sorted_array_to_bst import Solution as SortedToBst
from src.p3_longest_nice_substring import Solution as Nice
from src.p4_different_ways import Solution as Ways
from src.p4_different_ways_improved import Solution as WaysImproved
from src.p5_build_tree import Solution as BuildTree
from src.p5_build_tree_improved import Solution as BuildTreeImproved
from src.tree_node import TreeNode, inorder, preorder

sys.setrecursionlimit(20000)
OUT = Path(__file__).resolve().parent.parent / "out"
rng = random.Random(14)


def measure(fn, repeats: int = 3) -> tuple[float, float]:
    """(хугацааны медиан ms, санах ойн оргил KB). Санах ойг тусад нь хэмжинэ."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter() - t0) * 1000)
    tracemalloc.start()
    fn()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return statistics.median(times), peak / 1024


# --- оролт үүсгэгчид -------------------------------------------------------
def majority_input(n: int) -> list[int]:
    k = n // 2 + 1
    nums = [7] * k + [rng.randint(-10**6, 10**6) for _ in range(n - k)]
    rng.shuffle(nums)
    return nums


def nice_input(n: int) -> str:
    return "".join(rng.choice("abcdeABCDE") for _ in range(n))


def expression(k: int) -> str:
    parts = [str(rng.randint(1, 99))]
    for _ in range(k):
        parts += [rng.choice("+-*"), str(rng.randint(1, 99))]
    return "".join(parts)


def random_tree(n: int) -> TreeNode | None:
    values = rng.sample(range(-10**6, 10**6), n)

    def make(vals):
        if not vals:
            return None
        k = rng.randrange(len(vals))
        return TreeNode(vals[k], make(vals[:k]), make(vals[k + 1:]))

    return make(values)


def chain(n: int) -> TreeNode | None:
    root = None
    for v in range(n):
        root = TreeNode(v, root, None)
    return root


def main() -> None:
    rows = []

    def record(problem, variant, case, n, fn, extra=""):
        ms, kb = measure(fn)
        rows.append([problem, variant, case, n, f"{ms:.3f}", f"{kb:.1f}", extra])
        print(f"  {problem} {variant:<9} {case:<7} n={n:<8} {ms:10.3f} ms {kb:10.1f} KB {extra}")

    for n in (10**3, 10**4, 10**5, 10**6):
        nums = majority_input(n)
        record("p1", "dc", "random", n, lambda: Majority().majorityElement(nums))

    for n in (10**3, 10**4, 10**5, 10**6):
        nums = list(range(n))
        record("p2", "basic", "sorted", n, lambda: SortedToBst().sortedArrayToBST(nums))

    for n in (10**2, 10**3, 10**4, 10**5):
        s = nice_input(n)
        record("p3", "dc", "random", n, lambda: Nice().longestNiceSubstring(s))

    for k in range(2, 11):
        expr = expression(k)
        for variant, cls in (("basic", Ways), ("improved", WaysImproved)):
            solver = cls()
            solver.diffWaysToCompute(expr)
            calls = solver.calls
            record("p4", variant, "random", k, lambda: cls().diffWaysToCompute(expr), f"calls={calls}")

    for n in (500, 1000, 2000, 4000):
        for case, tree in (("random", random_tree(n)), ("chain", chain(n))):
            pre, ino = preorder(tree), inorder(tree)
            for variant, cls in (("basic", BuildTree), ("improved", BuildTreeImproved)):
                record("p5", variant, case, n, lambda: cls().buildTree(pre, ino))

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "results_python.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("problem\tvariant\tcase\tn\ttime_ms\tpeak_kb\textra\n")
        for r in rows:
            f.write("\t".join(str(v) for v in r) + "\n")
    print(f"\n  -> {path}")


if __name__ == "__main__":
    main()
