from __future__ import annotations

import statistics
import time

import pytest

from src.ranking_distance import ranking_distance
from tests.tsv import MINE, write_results

SIZES = [100, 1_000, 10_000, 100_000, 1_000_000]
REPEATS = 5


def _load(n: int) -> tuple[list[int], list[int]] | None:
    path = MINE / f"personal_{n}.tsv"
    if not path.exists():
        return None
    a: list[int] = []
    b: list[int] = []
    with path.open(encoding="utf-8") as f:
        next(f)
        for line in f:
            x, y = line.split()
            a.append(int(x))
            b.append(int(y))
    return a, b


def test_benchmark():
    results = []
    for n in SIZES:
        data = _load(n)
        if data is None:
            continue
        a, b = data
        distance = ranking_distance(a, b)
        times = []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            ranking_distance(a, b)
            times.append((time.perf_counter() - t0) * 1000)
        median = statistics.median(times)
        results.append([n, distance, f"{median:.3f}"])
        print(f"  n={n:<9} distance={distance:<14} {median:9.3f} ms")

    if not results:
        pytest.skip(
            "personal_*.tsv олдсонгүй. Эхлээд ажиллуул:\n"
            "  cd lab02/<Student-ID> && python3 ../tools/gen_lab02.py <Student-ID>"
        )
    path = write_results("python", ["n", "distance", "time_ms"], results)
    print(f"\n  -> {path}")
