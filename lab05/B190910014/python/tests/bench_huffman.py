from __future__ import annotations

import statistics
import time
from collections import Counter

import pytest

from src.huffman import huffman_build, huffman_decode, huffman_encode
from tests.tsv import MINE, SHARED, write_results

REPEATS = 3
FACTORS = [1, 2, 4, 8, 16]


def test_benchmark():
    if not (MINE / "personal.tsv").exists():
        pytest.skip(
            "personal.tsv олдсонгүй. Эхлээд ажиллуул:\n"
            "  cd lab05/<Student-ID> && python3 ../tools/gen_lab05.py <Student-ID>"
        )
    base = (SHARED / "mn_text.txt").read_text(encoding="utf-8")
    results = []
    for k in FACTORS:
        text = base * k
        times = []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            codes = huffman_build(dict(Counter(text)))
            bits = huffman_encode(text, codes)
            huffman_decode(bits, codes)
            times.append((time.perf_counter() - t0) * 1000)
        median = statistics.median(times)
        results.append([len(text), len(bits), f"{median:.3f}"])
        print(f"  chars={len(text):<9} bits={len(bits):<10} {median:10.3f} ms")

    path = write_results(
        "python", ["chars", "bits", "time_ms"], results, name="huffman"
    )
    print(f"\n  -> {path}")
