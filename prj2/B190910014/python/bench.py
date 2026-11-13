"""Бие даалт 2 — хэмжилт. lab-ын хавтаснаас: cd python && python3 bench.py -> ../out/results_python.tsv

Мөр бүр: problem, variant, case, n, time_ms, peak_kb, extra.
Хугацаа: ≥ 20 ms багцын 3 хэмжилтийн медиан (нэг дуудалт ≥ 5 с бол 1 удаа).
Санах ой: tracemalloc-ийн оргил (KB), оролтыг оролцуулахгүй (оролтыг өмнө нь үүсгэнэ).
"""
import random
import statistics
import time
import tracemalloc
from pathlib import Path

from src.p1_str_str import Solution as Kmp, SolutionNaive as Naive
from src.p2_flood_fill import Solution as FloodBfs
from src.p3_assign_cookies import Solution as Cookies
from src.p4_jump_game import Solution as JumpDp
from src.p4_jump_game_improved import Solution as JumpGreedy
from src.p5_open_lock import Solution as Lock
from src.p5_open_lock_improved import Solution as LockImproved

OUT = Path(__file__).resolve().parent.parent / "out"
ROWS: list[list] = []


def measure(make_args, fn, repeats=3):
    """make_args() нь шинэ оролт буцаана (функц оролтыг өөрчилж болох тул дуудалт бүрд шинээр)."""
    args = make_args()
    t0 = time.perf_counter()
    result = fn(*args)
    first = time.perf_counter() - t0
    times = [first]
    if first < 5:
        iters = max(1, int(0.02 / max(first, 1e-7)))
        for _ in range(repeats):
            batch = [make_args() for _ in range(iters)]
            t0 = time.perf_counter()
            for a in batch:
                fn(*a)
            times.append((time.perf_counter() - t0) / iters)
    args = make_args()
    tracemalloc.start()
    fn(*args)
    peak = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    return result, statistics.median(times) * 1000, peak


def record(problem, variant, case, n, make_args, fn, extra=lambda r: r):
    result, ms, kb = measure(make_args, fn)
    ROWS.append([problem, variant, case, n, f"{ms:.4f}", f"{kb:.1f}", extra(result)])
    print(f"  {problem} {variant:<9} {case:<8} n={n:<9} {ms:12.3f} ms {kb:12.1f} KB  {extra(result)}", flush=True)


def main() -> None:
    rng = random.Random(2026)

    # 1. strStr: муу тохиолдол (a…ab ба a…ab) болон санамсаргүй текст, m = 100
    for n in (10**3, 10**4, 10**5):
        hay, needle = "a" * (n - 1) + "b", "a" * 99 + "b"
        for variant, cls in (("kmp", Kmp), ("naive", Naive)):
            record("p1", variant, "worst", n, lambda: (hay, needle), lambda h, s, c=cls: c().strStr(h, s))
        text = "".join(rng.choice("abcd") for _ in range(n))
        pat = "".join(rng.choice("abcd") for _ in range(100))
        for variant, cls in (("kmp", Kmp), ("naive", Naive)):
            record("p1", variant, "random", n, lambda: (text, pat), lambda h, s, c=cls: c().strStr(h, s))

    # 2. Flood Fill: бүх нүд ижил өнгөтэй R×R зураг (бүх нүдийг будна)
    for side in (50, 200, 1000):
        record("p2", "bfs", "full", side * side, lambda: ([[1] * side for _ in range(side)], 0, 0, 2),
               lambda img, r, c, col: FloodBfs().floodFill(img, r, c, col), extra=lambda r: "")

    # 3. Assign Cookies: n = m санамсаргүй
    for n in (10**4, 10**5, 10**6):
        g = [rng.randint(1, 2**31 - 1) for _ in range(n)]
        s = [rng.randint(1, 2**31 - 1) for _ in range(n)]
        record("p3", "greedy", "random", n, lambda: (g[:], s[:]), lambda a, b: Cookies().findContentChildren(a, b))

    # 4. Jump Game II: nums[i] ∈ [1, 1000] санамсаргүй (LeetCode-ийн хязгаар)
    for n in (10**3, 10**4, 10**5):
        nums = [rng.randint(1, 1000) for _ in range(n)]

        def dp(a):
            s = JumpDp()
            return s.jump(a), s.steps

        if n <= 10**4:
            record("p4", "dp", "random", n, lambda: (nums,), dp, extra=lambda r: f"jumps={r[0]};steps={r[1]}")
        record("p4", "greedy", "random", n, lambda: (nums,), lambda a: JumpGreedy().jump(a),
               extra=lambda r: f"jumps={r}")

    # 5. Open the Lock
    cases = {
        "far": ([], "5555"),  # хамгийн хол (20 эргүүлэлт), түгжээгүй
        "example": (["0201", "0101", "0102", "1212", "2002"], "0202"),
        "random": (sorted({f"{rng.randrange(10000):04d}" for _ in range(500)} - {"0000", "7319"}), "7319"),
        "blocked": (["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888"),
    }
    for case, (dead, target) in cases.items():
        for variant, cls in (("bfs", Lock), ("bidir", LockImproved)):
            def run(d, t, c=cls):
                s = c()
                return s.openLock(d, t), s.expanded

            record("p5", variant, case, len(dead), lambda: (dead, target), run,
                   extra=lambda r: f"answer={r[0]};expanded={r[1]}")

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "results_python.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("problem\tvariant\tcase\tn\ttime_ms\tpeak_kb\textra\n")
        for r in ROWS:
            f.write("\t".join(str(v) for v in r) + "\n")
    print(f"\n  -> {path}")


if __name__ == "__main__":
    main()
