from __future__ import annotations

import statistics
import time

import pytest

from src.lcs_diff import lcs_diff
from tests.tsv import MINE, rows, strs, write_results

REPEATS = 3
TIME_LIMIT_MS = 10_000


def test_benchmark():
    if not (MINE / "personal_diff.tsv").exists():
        pytest.skip(
            "personal_diff.tsv олдсонгүй. Эхлээд ажиллуул:\n"
            "  cd lab04/<Student-ID> && python3 ../tools/gen_lab04.py <Student-ID>"
        )

    results = []
    for r in rows("personal_diff.tsv"):
        a, b = strs(r["A"]), strs(r["B"])
        t0 = time.perf_counter()
        out = lcs_diff(a, b)
        first = (time.perf_counter() - t0) * 1000
        common = sum(1 for line in out if line.startswith(" "))
        times = [first]
        if first < TIME_LIMIT_MS:
            for _ in range(REPEATS - 1):
                t0 = time.perf_counter()
                lcs_diff(a, b)
                times.append((time.perf_counter() - t0) * 1000)
        median = statistics.median(times)
        results.append([len(a), len(b), common, f"{median:.3f}"])
        print(f"  |A|={len(a):<6} |B|={len(b):<6} common={common:<6} {median:9.3f} ms")
        if first >= TIME_LIMIT_MS:
            print("  хугацаа хэтэрсэн тул үлдсэн оролтыг алгаслаа")
            break

    path = write_results(
        "python", ["m", "n", "common", "time_ms"], results, name="diff"
    )
    print(f"\n  -> {path}")
