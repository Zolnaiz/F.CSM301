"""A түвшин: өмнөх ба сайжруулсан шийдлийн хугацаа (ms), санах ойн оргил (KB, tracemalloc).

Ажиллуулах (lab04/<Student-ID>/python хавтаснаас, эхлээд gen_lab04.py-ээр өгөгдөл үүсгэнэ):
    python3 bench_improved.py
Үр дүн: ../out/improved_python.tsv
"""
import gc
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

from src.lcs_diff import lcs_diff
from src.lcs_diff_myers import lcs_diff_myers
from src.matrix_chain import matrix_chain_order
from src.matrix_chain_recursive import recursive_matrix_chain

STUDENT_DIR = Path(__file__).resolve().parent.parent
DATA = STUDENT_DIR / "test_data"
OUT = STUDENT_DIR / "out"
sys.setrecursionlimit(10_000)


def rows(name: str) -> list[list[str]]:
    lines = (DATA / name).read_text(encoding="utf-8").splitlines()
    return [line.split("\t") for line in lines[1:] if line]


def measure(fn, repeats: int = 3) -> tuple[float, float]:
    gc.collect()
    iters = 1
    while True:  # нэг багц ≥ 20 ms
        t0 = time.perf_counter()
        for _ in range(iters):
            fn()
        if time.perf_counter() - t0 >= 0.02 or iters >= 1 << 14:
            break
        iters *= 2
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        for _ in range(iters):
            fn()
        times.append((time.perf_counter() - t0) * 1000 / iters)
    tracemalloc.start()
    fn()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return statistics.median(times), peak / 1024


def main() -> None:
    out = []

    def record(task, variant, n, fn, extra=""):
        ms, kb = measure(fn)
        out.append([task, variant, n, f"{ms:.3f}", f"{kb:.1f}", extra])
        print(f"  {task:<5} {variant:<9} n={n:<6} {ms:11.3f} ms {kb:11.1f} KB {extra}")

    for m, a_str, b_str in rows("personal_diff.tsv"):
        a, b = a_str.split(","), b_str.split(",")
        d = len(a) + len(b) - 2 * sum(1 for line in lcs_diff_myers(a, b) if line[0] == " ")
        record("diff", "dp", len(a), lambda: lcs_diff(a, b), f"D={d}")
        record("diff", "myers", len(a), lambda: lcs_diff_myers(a, b), f"D={d}")

    p_all = [int(x) for x in rows("personal_chain.tsv")[-1][1].split(",")]
    for n in (4, 6, 8, 10, 12, 14):
        p = p_all[: n + 1]
        _, calls = recursive_matrix_chain(p)
        record("chain", "recursive", n, lambda: recursive_matrix_chain(p), f"calls={calls}")
        record("chain", "dp", n, lambda: matrix_chain_order(p), f"calls={n * (n + 1) // 2}")

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "improved_python.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("task\tvariant\tn\ttime_ms\tpeak_kb\textra\n")
        for r in out:
            f.write("\t".join(str(v) for v in r) + "\n")
    print(f"\n  -> {path}")


if __name__ == "__main__":
    main()
