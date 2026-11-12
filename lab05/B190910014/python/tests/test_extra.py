"""Нэмэлт шалгалт: шууд (brute force) аргатай тулгах, шинжилгээ ба уншлагын дүгнэлт, A төвшний
сайжруулсан хувилбарууд."""
import itertools
import random
from collections import Counter

import pytest

from src.activity import activity_select, shortest_first
from src.caching import cache_misses
from src.caching_fast import cache_misses_fast, next_use
from src.change import first_counterexample, make_change, min_coins, min_coins_table
from src.huffman import huffman_build, huffman_decode, huffman_encode
from src.huffman_fast import huffman_decode_fast
from src.knapsack import fractional_knapsack
from tests.tsv import SHARED, ints, rows

rng = random.Random(5)
TOGROG = [1, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 20000]


# --- 1. Ажиллагаа ---------------------------------------------------------
def _max_compatible(s, f) -> int:
    n = len(s)
    best = 0
    for mask in range(1 << n):
        idx = [i for i in range(n) if mask >> i & 1]
        if all(s[a] >= f[b] or s[b] >= f[a] for a, b in itertools.combinations(idx, 2)):
            best = max(best, len(idx))
    return best


def test_activity_random_against_brute_force():
    for _ in range(300):
        n = rng.randint(0, 10)
        s = [rng.randint(0, 20) for _ in range(n)]
        f = [si + rng.randint(1, 8) for si in s]
        assert len(activity_select(s, f)) == _max_compatible(s, f)


def test_shortest_first_counterexample_and_half_bound():
    # Шинжилгээ (б): [1,4), [3,5), [4,7) — хамгийн богино [3,5) нь нөгөө хоёртой давхцана.
    s, f = [1, 3, 4], [4, 5, 7]
    assert shortest_first(s, f) == [2] and len(activity_select(s, f)) == 2
    # Шинжилгээ (в): хамгийн богиныг сонгох дүрэм оновчтойн дор хаяж хагасыг сонгоно.
    for _ in range(300):
        n = rng.randint(1, 10)
        s = [rng.randint(0, 20) for _ in range(n)]
        f = [si + rng.randint(1, 8) for si in s]
        assert 2 * len(shortest_first(s, f)) >= len(activity_select(s, f))


# --- 2. Үүргэвч ------------------------------------------------------------
def test_knapsack_edge_cases():
    assert fractional_knapsack([], [], 10) == 0
    assert fractional_knapsack([5], [10], 0) == 0
    assert fractional_knapsack([2, 3], [4, 9], 100) == 13  # бүгд багтана
    assert fractional_knapsack([0, 4], [7, 8], 2) == 7 + 4  # жингүй эд зүйл + хагас
    with pytest.raises(ValueError):
        fractional_knapsack([1], [1, 2], 3)


def test_knapsack_not_below_zero_one():
    for r in rows("knapsack_01.tsv"):
        got = fractional_knapsack(ints(r["w"]), ints(r["v"]), int(r["W"]))
        assert got >= int(r["zero_one"]) - 1e-9, r["id"]


# --- 3. Хариулт мөнгө, уншлага ---------------------------------------------
def test_make_change_example_3760():
    assert make_change(TOGROG, 3760) == [0, 0, 1, 0, 1, 2, 1, 3, 0, 0, 0]


def test_kozen_zaks_range():
    assert first_counterexample(TOGROG) is None  # x = 11…29 999 бүгд оновчтой
    assert first_counterexample([1, 5, 10, 20, 25, 50]) == 40  # 25+10+5 ба 20+20
    assert first_counterexample([1, 3, 4]) == 6
    assert first_counterexample([1, 3, 6, 12, 24, 30]) == 48  # Их Британи, 1971 оноос өмнө


def test_doubling_is_not_enough():
    # Уншлага (б): дүн бүр өмнөхөөсөө ≥ 2 дахин их ч хомхойлох арга оновчгүй.
    d = [1, 10, 25]
    assert all(b >= 2 * a for a, b in zip(d, d[1:]))
    assert sum(make_change(d, 30)) == 6 and min_coins(d, 30) == 3


def test_min_coins_table_matches_single():
    d = [1, 5, 10, 20, 25, 50]
    table = min_coins_table(d, 300)
    assert all(table[x] == min_coins(d, x) for x in range(0, 301, 7))


def test_one_five_ten_twenty_fifty_bounds():
    # Уншлага (в): оновчтой шийдэд 1 ≤ 4, 5 ≤ 1, 10 ≤ 1, 20 ≤ 2 ширхэг, 20×2 ба 10 хамт байхгүй.
    d = [1, 5, 10, 20, 50]
    for x in range(0, 500):
        c = make_change(d, x)
        assert sum(c) == min_coins(d, x)
        assert c[0] <= 4 and c[1] <= 1 and c[2] <= 1 and c[3] <= 2
        assert not (c[3] == 2 and c[2] == 1)


# --- 4. Хаффман -------------------------------------------------------------
def test_huffman_single_and_skewed():
    codes = huffman_build({"x": 5})
    assert codes == {"x": "0"}
    assert huffman_decode(huffman_encode("xxxxx", codes), codes) == "xxxxx"
    assert huffman_decode_fast(huffman_encode("xxxxx", codes), codes) == "xxxxx"
    # Фибоначчийн давтамж — модны гүн σ − 1 (код 20+ бит урт)
    fib = [1, 1]
    while len(fib) < 25:
        fib.append(fib[-1] + fib[-2])
    freq = {chr(65 + i): f for i, f in enumerate(fib)}
    codes = huffman_build(freq)
    assert max(len(c) for c in codes.values()) == len(freq) - 1
    text = "".join(rng.choice(list(freq)) for _ in range(3000))
    bits = huffman_encode(text, codes)
    assert huffman_decode_fast(bits, codes) == huffman_decode(bits, codes) == text


def test_huffman_fast_decode_random_and_text():
    for _ in range(100):
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяөү ."[: rng.randint(2, 37)]
        text = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 400)))
        codes = huffman_build(dict(Counter(text)))
        bits = huffman_encode(text, codes)
        assert huffman_decode_fast(bits, codes) == text
    text = (SHARED / "mn_text.txt").read_text(encoding="utf-8")
    codes = huffman_build(dict(Counter(text)))
    assert huffman_decode_fast(huffman_encode(text, codes), codes) == text


def test_huffman_rejects_bad_bits():
    codes = {"a": "0", "b": "10", "c": "11"}
    for bad in ("1", "0101"):
        with pytest.raises(ValueError):
            huffman_decode(bad, codes)
        with pytest.raises(ValueError):
            huffman_decode_fast(bad, codes)


# --- 5. Кэш ----------------------------------------------------------------
def _optimal_misses(k, req) -> int:
    """Бүх хасах сонголтыг шалгах (жижиг оролтод)."""
    best = None

    def go(i, cache, misses):
        nonlocal best
        if best is not None and misses >= best:
            return
        if i == len(req):
            best = misses
            return
        p = req[i]
        if p in cache:
            go(i + 1, cache, misses)
        elif len(cache) < k:
            go(i + 1, cache | {p}, misses + 1)
        else:
            for q in cache:
                go(i + 1, (cache - {q}) | {p}, misses + 1)

    go(0, frozenset(), 0)
    return best


def test_furthest_in_future_is_optimal_on_small_inputs():
    for _ in range(150):
        k = rng.randint(1, 3)
        req = [rng.randint(1, 5) for _ in range(rng.randint(0, 11))]
        expected = _optimal_misses(k, req)
        assert cache_misses(k, req) == expected
        assert cache_misses_fast(k, req) == expected


def test_fast_matches_basic():
    for r in rows("caching_01.tsv"):
        assert cache_misses_fast(int(r["k"]), ints(r["requests"])) == int(r["furthest"]), r["id"]
    for _ in range(200):
        k = rng.randint(0, 8)
        req = [rng.randint(1, 15) for _ in range(rng.randint(0, 300))]
        assert cache_misses_fast(k, req) == cache_misses(k, req)


def test_next_use():
    assert next_use([1, 2, 1, 3, 2]) == [2, 4, 5, 5, 5]


def test_fifo_lru_columns_and_offline_optimality():
    from src.caching_policies import fifo_misses, lru_misses

    for r in rows("caching_01.tsv"):
        k, req = int(r["k"]), ints(r["requests"])
        assert fifo_misses(k, req) == int(r["fifo"]), r["id"]
        assert lru_misses(k, req) == int(r["lru"]), r["id"]
    for _ in range(200):
        k = rng.randint(1, 6)
        req = [rng.randint(1, 12) for _ in range(rng.randint(0, 200))]
        best = cache_misses_fast(k, req)
        assert best <= fifo_misses(k, req) and best <= lru_misses(k, req)
