"""Тайлангийн 4(b), 4(c) хүснэгтийг гаргах туршилт.

Ажиллуулах: cd lab02/<Student-ID>/python && .venv/bin/python experiments.py
"""
import math
import random
import time

from src.binary_insertion_sort import binary_insertion_sort
from src.insertion_sort import insertion_sort


def inputs(n: int) -> dict[str, list[int]]:
    rng = random.Random(n)
    shuffled = list(range(1, n + 1))
    rng.shuffle(shuffled)
    return {
        "урвуу": list(range(n, 0, -1)),
        "өсөх": list(range(1, n + 1)),
        "санамсаргүй": shuffled,
    }


def counts_table() -> None:
    print("## 4(b) харьцуулалт ба зөөлт")
    print("| n | оролт | харьцуулалт | n⌈lg n⌉ | зөөлт | n(n-1)/2 |")
    print("| -: | --- | ---: | ---: | ---: | ---: |")
    for n in (100, 1000, 10000):
        for name, a in inputs(n).items():
            _, cmps, shifts = binary_insertion_sort(a)
            bound = n * math.ceil(math.log2(n))
            print(f"| {n} | {name} | {cmps} | {bound} | {shifts} | {n * (n - 1) // 2} |")


def timing_table() -> None:
    print("\n## 4(c) санамсаргүй оролт дээрх хугацаа")
    print("| n | харьцуулалт | зөөлт | binary_insertion_sort, ms | insertion_sort, ms |")
    print("| -: | ---: | ---: | ---: | ---: |")
    for n in (1000, 2000, 4000, 8000, 16000):
        a = inputs(n)["санамсаргүй"]
        t0 = time.perf_counter()
        _, cmps, shifts = binary_insertion_sort(a)
        t1 = time.perf_counter()
        insertion_sort(a)
        t2 = time.perf_counter()
        print(
            f"| {n} | {cmps} | {shifts} | {(t1 - t0) * 1000:.1f} | {(t2 - t1) * 1000:.1f} |"
        )


if __name__ == "__main__":
    counts_table()
    timing_table()
