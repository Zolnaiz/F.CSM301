"""Онлайн бодлогуудын шалгалт: python3 -m pytest online/test_online.py (lab05/<ID>-оос)."""
import itertools
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cf158b import taxis  # noqa: E402
from lc435 import Solution as Lc435  # noqa: E402
from lc621 import Solution as Lc621, SolutionSimulation  # noqa: E402

rng = random.Random(7)


def taxis_brute(groups):
    """First-fit decreasing бүх дарааллаар — жижиг оролтод хамгийн цөөн такси."""
    best = len(groups)
    for perm in set(itertools.permutations(groups)):
        cars = []
        for g in perm:
            for i, free in enumerate(cars):
                if free >= g:
                    cars[i] -= g
                    break
            else:
                cars.append(4 - g)
        best = min(best, len(cars))
    return best


def test_cf158b():
    assert taxis([1, 2, 4, 3, 3]) == 4
    assert taxis([2, 3, 4, 4, 2, 1, 3, 1]) == 5
    for _ in range(300):
        groups = [rng.randint(1, 4) for _ in range(rng.randint(1, 7))]
        assert taxis(groups) == taxis_brute(groups), groups


def test_lc435():
    assert Lc435().eraseOverlapIntervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert Lc435().eraseOverlapIntervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert Lc435().eraseOverlapIntervals([[1, 2], [2, 3]]) == 0
    for _ in range(300):
        iv = [[s, s + rng.randint(1, 6)] for s in (rng.randint(0, 15) for _ in range(rng.randint(1, 9)))]
        best = 0
        for mask in range(1 << len(iv)):
            idx = [i for i in range(len(iv)) if mask >> i & 1]
            if all(iv[a][1] <= iv[b][0] or iv[b][1] <= iv[a][0] for a, b in itertools.combinations(idx, 2)):
                best = max(best, len(idx))
        assert Lc435().eraseOverlapIntervals([x[:] for x in iv]) == len(iv) - best


def test_lc621():
    assert Lc621().leastInterval(list("AAABBB"), 2) == 8
    assert Lc621().leastInterval(list("ACABDB"), 1) == 6
    assert Lc621().leastInterval(list("AAABBB"), 3) == 10
    for _ in range(300):
        tasks = [rng.choice("ABCDE") for _ in range(rng.randint(1, 30))]
        n = rng.randint(0, 5)
        assert Lc621().leastInterval(tasks, n) == SolutionSimulation().leastInterval(tasks, n)
