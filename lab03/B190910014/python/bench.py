"""5-р даалгаврын хэмжилт.

Ажиллуулах (lab03/<Student-ID>/python хавтаснаас):
    python3 ../../tools/gen_lab03.py <Student-ID>   # эхлээд lab03/<Student-ID>-ээс
    python3 bench.py

Үр дүн: ../out/results_python.tsv  (n, algorithm, time_ms, mults)
"""
import statistics
import time
from pathlib import Path

from src.matrix_multiply import matrix_multiply
from src.matrix_multiply_recursive import matrix_multiply_recursive
from src.strassen import strassen

STUDENT_DIR = Path(__file__).resolve().parent.parent
DATA = STUDENT_DIR / "test_data"
OUT = STUDENT_DIR / "out"

LIMIT_MS = 60_000
# n хоёр дахин өсөхөд хугацаа ойролцоогоор хэд дахин өсөх вэ (n³ → 8, n^lg7 → 7).
ALGORITHMS = [
    ("matrix_multiply", matrix_multiply, 8),
    ("matrix_multiply_recursive", matrix_multiply_recursive, 8),
    ("strassen", strassen, 7),
]


def load(n: int):
    lines = (DATA / f"personal_{n}.tsv").read_text(encoding="utf-8").split("\n")
    assert int(lines[0]) == n
    rows = [[int(x) for x in line.split("\t")] for line in lines[1 : 2 * n + 1]]
    return rows[:n], rows[n:]


def measure(fn, a, b, repeats: int):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        c, mults = fn(a, b)
        times.append((time.perf_counter() - t0) * 1000)
    return c, mults, statistics.median(times)


def main() -> None:
    results = []
    last_ms = {name: 0.0 for name, _, _ in ALGORITHMS}
    stopped = set()
    n = 2
    while (DATA / f"personal_{n}.tsv").exists():
        a, b = load(n)
        reference = None
        for name, fn, growth in ALGORITHMS:
            if name in stopped:
                continue
            if last_ms[name] * growth > LIMIT_MS:
                print(f"  n={n:<4} {name:<26} алгассан: ~{last_ms[name] * growth / 1000:.0f} с > 60 с")
                stopped.add(name)
                continue
            repeats = 3 if n <= 128 else 1
            c, mults, ms = measure(fn, a, b, repeats)
            if reference is None:
                reference = c
            assert c == reference, f"{name}: n={n} хариу таарахгүй"
            results.append([n, name, f"{ms:.3f}", mults])
            last_ms[name] = ms
            print(f"  n={n:<4} {name:<26} {ms:12.3f} ms  mults={mults}")
            if ms > LIMIT_MS:
                stopped.add(name)
        n *= 2

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "results_python.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("n\talgorithm\ttime_ms\tmults\n")
        for r in results:
            f.write("\t".join(str(v) for v in r) + "\n")
    print(f"\n  -> {path}")


if __name__ == "__main__":
    main()
