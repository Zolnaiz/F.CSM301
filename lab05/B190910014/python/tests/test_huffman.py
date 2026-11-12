import heapq
from collections import Counter

from src.huffman import huffman_build, huffman_decode, huffman_encode
from tests.tsv import SHARED, ints, rows

CASES = rows("huffman_01.tsv")


def _optimal_bits(freqs: list[int]) -> int:
    if len(freqs) == 1:
        return freqs[0]
    h = list(freqs)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def _check_codes(codes: dict[str, str], symbols, label: str) -> None:
    assert set(codes) == set(symbols), label
    for c in codes.values():
        assert c and set(c) <= {"0", "1"}, (label, c)
    cs = sorted(codes.values())
    for a, b in zip(cs, cs[1:]):
        assert not b.startswith(a), f"{label}: {a!r} нь {b!r}-ийн угтвар"


def test_table_codes_are_optimal_prefix_codes():
    for r in CASES:
        symbols, freqs = r["symbols"].split(","), ints(r["freqs"])
        freq = dict(zip(symbols, freqs))
        codes = huffman_build(freq)
        _check_codes(codes, symbols, r["id"])
        assert sum(freq[s] * len(codes[s]) for s in symbols) == int(r["total_bits"]), r["id"]

        text = "".join(s * f for s, f in freq.items())
        bits = huffman_encode(text, codes)
        assert len(bits) == int(r["total_bits"]), r["id"]
        assert huffman_decode(bits, codes) == text, r["id"]


def test_mongolian_text_round_trip():
    text = (SHARED / "mn_text.txt").read_text(encoding="utf-8")
    freq = dict(Counter(text))
    codes = huffman_build(freq)
    _check_codes(codes, freq.keys(), "mn_text")
    bits = huffman_encode(text, codes)
    assert len(bits) == _optimal_bits(list(freq.values()))
    assert huffman_decode(bits, codes) == text
