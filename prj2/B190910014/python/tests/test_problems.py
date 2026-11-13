"""Бие даалт 2-ын шалгалт: LeetCode-ийн жишээ + шууд (brute force) аргатай санамсаргүй тулгалт."""
import random
from collections import deque

import pytest

from src.p1_str_str import Solution as StrStr, SolutionNaive as StrStrNaive
from src.p2_flood_fill import Solution as FloodBfs, SolutionDfs as FloodDfs
from src.p3_assign_cookies import Solution as Cookies
from src.p4_jump_game import Solution as Jump
from src.p4_jump_game_improved import Solution as JumpImproved
from src.p5_open_lock import Solution as Lock
from src.p5_open_lock_improved import Solution as LockImproved, neighbours

rng = random.Random(13)


# --- 1. strStr --------------------------------------------------------------
@pytest.mark.parametrize("solution", [StrStr, StrStrNaive])
@pytest.mark.parametrize("h,n,expected", [("sadbutsad", "sad", 0), ("leetcode", "leeto", -1),
                                          ("hello", "ll", 2), ("aaaaab", "aab", 3), ("a", "a", 0),
                                          ("abc", "abcd", -1), ("mississippi", "issip", 4)])
def test_p1_examples(solution, h, n, expected):
    assert solution().strStr(h, n) == expected


def test_p1_random_against_find():
    for _ in range(3000):
        h = "".join(rng.choice("ab") for _ in range(rng.randint(1, 30)))
        n = "".join(rng.choice("ab") for _ in range(rng.randint(1, 6)))
        expected = h.find(n)  # зөвхөн тест дээр шалгах зорилгоор
        assert StrStr().strStr(h, n) == expected, (h, n)
        assert StrStrNaive().strStr(h, n) == expected, (h, n)


# --- 2. Flood Fill ------------------------------------------------------------
def flood_reference(image, sr, sc, color):
    """Тогтмол цэг хүртэл давтах энгийн арга."""
    img = [row[:] for row in image]
    old = img[sr][sc]
    if old == color:
        return img
    region = {(sr, sc)}
    changed = True
    while changed:
        changed = False
        for r in range(len(img)):
            for c in range(len(img[0])):
                if (r, c) not in region and img[r][c] == old and any(
                        (r + dr, c + dc) in region for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    region.add((r, c))
                    changed = True
    for r, c in region:
        img[r][c] = color
    return img


@pytest.mark.parametrize("solution", [FloodBfs, FloodDfs])
def test_p2_examples_and_random(solution):
    assert solution().floodFill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    assert solution().floodFill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == [[0, 0, 0], [0, 0, 0]]
    for _ in range(300):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        image = [[rng.randint(0, 2) for _ in range(cols)] for _ in range(rows)]
        sr, sc, color = rng.randrange(rows), rng.randrange(cols), rng.randint(0, 2)
        expected = flood_reference(image, sr, sc, color)
        assert solution().floodFill([row[:] for row in image], sr, sc, color) == expected


def test_p2_large_image_no_recursion_limit():
    image = [[1] * 300 for _ in range(300)]
    out = FloodDfs().floodFill(image, 0, 0, 5)
    assert all(v == 5 for row in out for v in row)


# --- 3. Assign Cookies --------------------------------------------------------
def cookies_brute(g, s):
    """Хоёр талт графын хамгийн их хослол (Кун) — жижиг оролтод."""
    match = [-1] * len(s)

    def try_child(i, seen):
        for j in range(len(s)):
            if s[j] >= g[i] and not seen[j]:
                seen[j] = True
                if match[j] == -1 or try_child(match[j], seen):
                    match[j] = i
                    return True
        return False

    return sum(try_child(i, [False] * len(s)) for i in range(len(g)))


def test_p3():
    assert Cookies().findContentChildren([1, 2, 3], [1, 1]) == 1
    assert Cookies().findContentChildren([1, 2], [1, 2, 3]) == 2
    assert Cookies().findContentChildren([], [1]) == 0
    for _ in range(500):
        g = [rng.randint(1, 9) for _ in range(rng.randint(0, 8))]
        s = [rng.randint(1, 9) for _ in range(rng.randint(0, 8))]
        assert Cookies().findContentChildren(g[:], s[:]) == cookies_brute(g, s)


# --- 4. Jump Game II ----------------------------------------------------------
def jump_bfs(nums):
    n = len(nums)
    dist = [-1] * n
    dist[0] = 0
    q = deque([0])
    while q:
        i = q.popleft()
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if dist[j] == -1:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist[-1]


def reachable_array(n, max_jump):
    nums = [rng.randint(0, max_jump) for _ in range(n)]
    reach = 0  # бодлогын нөхцөл: n − 1-д заавал хүрэх боломжтой
    for i in range(n - 1):
        if reach <= i and nums[i] == 0:
            nums[i] = 1
        reach = max(reach, i + nums[i])
    return nums


@pytest.mark.parametrize("solution", [Jump, JumpImproved])
def test_p4(solution):
    assert solution().jump([2, 3, 1, 1, 4]) == 2
    assert solution().jump([2, 3, 0, 1, 4]) == 2
    assert solution().jump([0]) == 0
    assert solution().jump([1, 2]) == 1
    for _ in range(500):
        nums = reachable_array(rng.randint(1, 40), rng.randint(1, 6))
        assert solution().jump(nums) == jump_bfs(nums), nums


def test_p4_dp_work_is_quadratic_on_large_jumps():
    n = 300
    basic = Jump()
    assert basic.jump([n] * n) == 1
    assert basic.steps == (n - 1) * n // 2  # i бүрд n − 1 − i шинэчлэл


# --- 5. Open the Lock -------------------------------------------------------------
@pytest.mark.parametrize("solution", [Lock, LockImproved])
def test_p5_examples(solution):
    assert solution().openLock(["0201", "0101", "0102", "1212", "2002"], "0202") == 6
    assert solution().openLock(["8888"], "0009") == 1
    assert solution().openLock(["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888") == -1
    assert solution().openLock(["0000"], "8888") == -1
    assert solution().openLock([], "0000") == 0


def test_p5_improved_matches_basic_random():
    for _ in range(300):
        dead = {f"{rng.randrange(10000):04d}" for _ in range(rng.randint(0, 400))}
        target = f"{rng.randrange(10000):04d}"
        assert LockImproved().openLock(list(dead), target) == Lock().openLock(list(dead), target), target


def test_p5_neighbours():
    assert sorted(neighbours(0)) == sorted([1000, 9000, 100, 900, 10, 90, 1, 9])
    assert sorted(neighbours(9999)) == sorted([999, 9099, 9909, 9990, 8999, 9899, 9989, 9998])
    assert all(len(set(neighbours(x))) == 8 for x in range(0, 10000, 37))


@pytest.mark.parametrize("solution", [Lock, LockImproved])
def test_p5_target_is_deadend(solution):
    assert solution().openLock(["0001"], "0001") == -1
