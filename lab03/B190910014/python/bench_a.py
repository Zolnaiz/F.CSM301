"""A түвшин: B бодлогуудын (Штрассен, Гаусс) өмнөх ба сайжруулсан хувилбарын харьцуулалт.

Хувийн өгөгдөл (gen_lab03.py) дээр хугацаа (ms) ба санах ойн оргилыг (KB, tracemalloc) хэмжинэ.
Гауссын системийг хувийн A матрицаас диагональ давамгай болгож, x = B-ийн эхний багана гэж үүсгэнэ.

Ажиллуулах (lab03/<Student-ID>/python-оос):
    python3 bench_a.py strassen   naive, цэвэр Штрассен, cutoff 32/64 -> ../out/a_strassen_python.tsv
    python3 bench_a.py gauss      gauss_solve, _fast, jacobi_solve -> ../out/a_gauss_python.tsv
    python3 bench_a.py problems   1–5-р бодлого, fib_matrix (n=128) -> ../out/a_problems_python.tsv
Аргументгүй бол гурвууланг нь ажиллуулна.
"""
import gc
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

from src.fib_matrix import fib_matrix
from src.gauss import gauss_solve, gauss_solve_fast, jacobi_solve
from src.matrix_multiply import matrix_multiply
from src.matrix_multiply_recursive import matrix_multiply_recursive
from src.matrix_vector import matrix_vector
from src.strassen import strassen

STUDENT_DIR = Path(__file__).resolve().parent.parent
DATA = STUDENT_DIR / "test_data"
OUT = STUDENT_DIR / "out"


def load(n: int):
    lines = (DATA / f"personal_{n}.tsv").read_text(encoding="utf-8").split("\n")
    rows = [[int(x) for x in line.split("\t")] for line in lines[1: 2 * n + 1]]
    return rows[:n], rows[n:]


def system(n: int):
    """Хувийн A-г диагональ давамгай болгож, x = B-ийн эхний багана байх b = Ax-ийг үүсгэнэ."""
    a, b = load(n)
    for i in range(n):
        a[i][i] = sum(abs(v) for j, v in enumerate(a[i]) if j != i) + 1
    x = [b[i][0] for i in range(n)]
    rhs = [sum(a[i][j] * x[j] for j in range(n)) for i in range(n)]
    return a, rhs


def measure(fn, repeats: int = 5):
    """Хугацаа: ≥ 20 ms багцын медиан (ms). Санах ой: нэг дуудалтын tracemalloc оргил (KB)."""
    gc.collect()
    iters = 1
    while True:
        t0 = time.perf_counter()
        for _ in range(iters):
            fn()
        elapsed = time.perf_counter() - t0
        if elapsed >= 0.02 or iters >= 1 << 12:
            break
        iters *= 2
    times = []
    for _ in range(repeats if elapsed < 5 else 1):
        t0 = time.perf_counter()
        for _ in range(iters):
            fn()
        times.append((time.perf_counter() - t0) * 1000 / iters)
    tracemalloc.start()
    fn()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return statistics.median(times), peak / 1024


def run(section: str, cases) -> None:
    rows = []
    for name, n, fn in cases:
        ms, kb = measure(fn)
        rows.append([name, n, f"{ms:.3f}", f"{kb:.1f}"])
        print(f"  {name:<28} n={n:<4} {ms:12.3f} ms {kb:12.1f} KB", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"a_{section}_python.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("variant\tn\ttime_ms\tpeak_kb\n")
        for r in rows:
            f.write("\t".join(str(v) for v in r) + "\n")
    print(f"  -> {path}\n", flush=True)


def strassen_cases():
    for n in (32, 64, 128, 256):
        a, b = load(n)
        yield "naive", n, lambda: matrix_multiply(a, b)  # харьцуулах суурь (1-р бодлого)
        if n <= 128:  # n = 256 үед цэвэр Штрассен ≈ 15 с × давталт
            yield "pure", n, lambda: strassen(a, b)
        yield "cutoff32", n, lambda: strassen(a, b, 32)
        yield "cutoff64", n, lambda: strassen(a, b, 64)


def gauss_cases():
    for n in (64, 128, 256, 512):
        a, rhs = system(n)
        yield "basic", n, lambda: gauss_solve(a, rhs)
        yield "fast", n, lambda: gauss_solve_fast(a, rhs)
        yield "jacobi", n, lambda: jacobi_solve(a, rhs)


def problem_cases():
    n = 128
    a, b = load(n)
    x = [b[i][0] for i in range(n)]
    ga, rhs = system(n)
    yield "1 matrix_multiply", n, lambda: matrix_multiply(a, b)
    yield "2 matrix_multiply_recursive", n, lambda: matrix_multiply_recursive(a, b)
    yield "3 matrix_vector", n, lambda: matrix_vector(a, x)
    yield "4 strassen", n, lambda: strassen(a, b)
    yield "5 gauss_solve", n, lambda: gauss_solve(ga, rhs)
    yield "fib_matrix", 10**18, lambda: fib_matrix(10**18)


SECTIONS = {"strassen": strassen_cases, "gauss": gauss_cases, "problems": problem_cases}

if __name__ == "__main__":
    for section in sys.argv[1:] or list(SECTIONS):
        run(section, SECTIONS[section]())
