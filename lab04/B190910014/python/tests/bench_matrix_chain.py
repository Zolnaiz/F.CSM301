from __future__ import annotations

import statistics
import time

import pytest

from src.matrix_chain import matrix_chain_order
from tests.tsv import MINE, ints, rows, write_results

REPEATS = 5
TIME_LIMIT_MS = 10_000


def test_benchmark():
    if not (MINE / "personal_chain.tsv").exists():
        pytest.skip(
            "personal_chain.tsv олдсонгүй. Эхлээд ажиллуул:\n"
            "  cd lab04/<Student-ID> && python3 ../tools/gen_lab04.py <Student-ID>"
        )

    results = []
    for r in rows("personal_chain.tsv"):
        p = ints(r["p"])
        n = len(p) - 1
        t0 = time.perf_counter()
        min_mults, _ = matrix_chain_order(p)
        first = (time.perf_counter() - t0) * 1000
        times = [first]
        if first < TIME_LIMIT_MS:
            for _ in range(REPEATS - 1):
                t0 = time.perf_counter()
                matrix_chain_order(p)
                times.append((time.perf_counter() - t0) * 1000)
        median = statistics.median(times)
        results.append([n, min_mults, f"{median:.3f}"])
        print(f"  n={n:<6} min_mults={min_mults:<12} {median:9.3f} ms")
        if first >= TIME_LIMIT_MS:
            print("  хугацаа хэтэрсэн тул үлдсэн оролтыг алгаслаа")
            break

    path = write_results("python", ["n", "min_mults", "time_ms"], results, name="chain")
    print(f"\n  -> {path}")
