"""Лаб 5 хэмжилт: бодлого бүрийн хугацаа, санах ой ба A төвшний харьцуулалт.

Ажиллуулах (lab05/<Student-ID>/python-оос, эхлээд python3 ../../tools/gen_lab05.py <ID>):
    python3 bench_a.py c          1–3-р бодлого (санамсаргүй, seed 5)  -> ../out/a_c_python.tsv
    python3 bench_a.py huffman    mn_text × 1…16, анхны ба сайжруулсан -> ../out/a_huffman_python.tsv
    python3 bench_a.py caching    personal.tsv, k = 64, анхны ба сайжр. -> ../out/a_caching_python.tsv
Хугацаа: 3 удаагийн медиан (нэг ажиллалт ≥ 5 с бол 1 удаа). Санах ой: tracemalloc-ийн оргил, KB
(анхны кэш нь 5 с-ээс удаан бол санах ойг хэмжихгүй).
"""
import random
import statistics
import sys
import time
import tracemalloc
from collections import Counter
from pathlib import Path

from src.activity import activity_select
from src.caching import cache_misses
from src.caching_fast import cache_misses_fast
from src.change import make_change, min_coins
from src.huffman import huffman_build, huffman_decode, huffman_encode
from src.huffman_fast import huffman_decode_fast
from src.knapsack import fractional_knapsack

STUDENT_DIR = Path(__file__).resolve().parent.parent
LAB_DIR = STUDENT_DIR.parent
OUT = STUDENT_DIR / "out"
TOGROG = [1, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 20000]


def measure(fn, memory: bool = True):
    t0 = time.perf_counter()
    result = fn()
    first = (time.perf_counter() - t0) * 1000
    times = [first]
    if first < 5000:
        for _ in range(2):
            t0 = time.perf_counter()
            fn()
            times.append((time.perf_counter() - t0) * 1000)
    kb = None
    if memory and first < 5000:
        tracemalloc.start()
        fn()
        kb = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()
    return result, statistics.median(times), kb


def save(name, header, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"a_{name}_python.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(str(v) for v in r) + "\n")
    print(f"  -> {path}\n", flush=True)


def fmt(kb):
    return "—" if kb is None else f"{kb:.1f}"


def bench_c():
    rng = random.Random(5)
    rows = []
    for n in (10**4, 10**5, 10**6):
        s = [rng.randint(0, 10 * n) for _ in range(n)]
        f = [si + rng.randint(1, 100) for si in s]
        res, ms, kb = measure(lambda: activity_select(s, f))
        rows.append(["activity_select", n, len(res), f"{ms:.3f}", fmt(kb)])
        w = [rng.randint(1, 100) for _ in range(n)]
        v = [rng.randint(1, 100) for _ in range(n)]
        res, ms, kb = measure(lambda: fractional_knapsack(w, v, 25 * n))
        rows.append(["fractional_knapsack", n, f"{res:.2f}", f"{ms:.3f}", fmt(kb)])
    for x in (3760, 10**6, 10**9):
        res, ms, kb = measure(lambda: make_change(TOGROG, x))
        rows.append(["make_change", x, sum(res), f"{ms:.4f}", fmt(kb)])
    for x in (10**4, 10**5, 10**6):
        res, ms, kb = measure(lambda: min_coins(TOGROG, x))
        rows.append(["min_coins", x, res, f"{ms:.3f}", fmt(kb)])
    for r in rows:
        print("  " + "\t".join(str(v) for v in r), flush=True)
    save("c", ["problem", "n_or_x", "result", "time_ms", "peak_kb"], rows)


def bench_huffman():
    base = (LAB_DIR / "test_data" / "mn_text.txt").read_text(encoding="utf-8")
    rows = []
    for k in (1, 2, 4, 8, 16):
        text = base * k
        codes = huffman_build(dict(Counter(text)))
        bits = huffman_encode(text, codes)
        for variant, decode in (("basic", huffman_decode), ("fast", huffman_decode_fast)):
            def run():
                c = huffman_build(dict(Counter(text)))
                return decode(huffman_encode(text, c), c)

            assert run() == text
            _, total_ms, kb = measure(run)
            _, dec_ms, dec_kb = measure(lambda: decode(bits, codes))
            rows.append([variant, len(text), len(bits), f"{total_ms:.3f}", f"{dec_ms:.3f}", fmt(kb), fmt(dec_kb)])
            print(f"  {variant:<6} chars={len(text):<8} bits={len(bits):<9} build+enc+dec {total_ms:9.1f} ms"
                  f"  decode {dec_ms:9.1f} ms  peak {fmt(kb)} KB", flush=True)
    save("huffman", ["variant", "chars", "bits", "total_ms", "decode_ms", "peak_kb", "decode_peak_kb"], rows)


def bench_caching():
    line = (STUDENT_DIR / "test_data" / "personal.tsv").read_text(encoding="utf-8").split("\n")[1]
    requests = [int(x) for x in line.split("\t")[1].split(",")]
    rows, basic_stopped = [], False
    for n in (1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000, 200_000):
        req = requests[:n]
        fast, fast_ms, fast_kb = measure(lambda: cache_misses_fast(64, req))
        rows.append(["fast", n, 64, fast, f"{fast_ms:.3f}", fmt(fast_kb)])
        print(f"  fast   n={n:<7} misses={fast:<7} {fast_ms:10.1f} ms  peak {fmt(fast_kb)} KB", flush=True)
        if not basic_stopped:
            basic, ms, kb = measure(lambda: cache_misses(64, req))
            assert basic == fast
            rows.append(["basic", n, 64, basic, f"{ms:.3f}", fmt(kb)])
            print(f"  basic  n={n:<7} misses={basic:<7} {ms:10.1f} ms  peak {fmt(kb)} KB", flush=True)
            basic_stopped = ms >= 10_000
    save("caching", ["variant", "n", "k", "misses", "time_ms", "peak_kb"], rows)


SECTIONS = {"c": bench_c, "huffman": bench_huffman, "caching": bench_caching}

if __name__ == "__main__":
    for name in sys.argv[1:] or list(SECTIONS):
        SECTIONS[name]()
