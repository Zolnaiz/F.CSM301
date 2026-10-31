from __future__ import annotations

import statistics
import time

import pytest

from src.cut_rod import bottom_up_cut_rod
from tests.tsv import MINE, ints, rows, write_results

REPEATS = 5


def test_benchmark():
    if not (MINE / "personal.tsv").exists():
        pytest.skip(
            "personal.tsv олдсонгүй. Эхлээд ажиллуул:\n"
            "  cd lab04/<Student-ID> && python3 ../tools/gen_lab04.py <Student-ID>"
        )

    results = []
    for r in rows("personal.tsv"):
        p = ints(r["p"])
        n = len(p)
        revenue, loop_count = bottom_up_cut_rod(p)
        times = []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            bottom_up_cut_rod(p)
            times.append((time.perf_counter() - t0) * 1000)
        median = statistics.median(times)
        results.append([n, revenue, loop_count, f"{median:.3f}"])
        print(f"  n={n:<6} revenue={revenue:<10} loops={loop_count:<10} {median:9.3f} ms")

    path = write_results("python", ["n", "revenue", "loop_count", "time_ms"], results)
    print(f"\n  -> {path}")
