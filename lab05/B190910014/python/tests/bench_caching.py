from __future__ import annotations

import time

import pytest

from src.caching import cache_misses
from tests.tsv import MINE, ints, rows, write_results

K = 64
SIZES = [1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000, 200_000]
TIME_LIMIT_MS = 10_000


def test_benchmark():
    if not (MINE / "personal.tsv").exists():
        pytest.skip(
            "personal.tsv олдсонгүй. Эхлээд ажиллуул:\n"
            "  cd lab05/<Student-ID> && python3 ../tools/gen_lab05.py <Student-ID>"
        )

    requests = ints(rows("personal.tsv")[0]["requests"])
    results = []
    for n in SIZES:
        if n > len(requests):
            break
        t0 = time.perf_counter()
        misses = cache_misses(K, requests[:n])
        ms = (time.perf_counter() - t0) * 1000
        results.append([n, K, misses, f"{ms:.3f}"])
        print(f"  n={n:<8} k={K} misses={misses:<8} {ms:10.3f} ms")
        if ms >= TIME_LIMIT_MS:
            print("  хугацаа хэтэрсэн тул үлдсэн оролтыг алгаслаа")
            break

    path = write_results(
        "python", ["n", "k", "misses", "time_ms"], results, name="caching"
    )
    print(f"\n  -> {path}")
