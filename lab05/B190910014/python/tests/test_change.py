from src.change import make_change, min_coins
from tests.tsv import ints, rows

CASES = rows("change_01.tsv")


def test_make_change_uses_fewest_notes():
    for r in CASES:
        d, x = ints(r["d"]), int(r["x"])
        counts = make_change(d, x)
        assert len(counts) == len(d), r["id"]
        assert all(c >= 0 for c in counts), r["id"]
        assert sum(c * di for c, di in zip(counts, d)) == x, r["id"]
        assert sum(counts) == int(r["total"]), r["id"]


def test_min_coins_matches_greedy_on_canonical_systems():
    for r in CASES:
        assert min_coins(ints(r["d"]), int(r["x"])) == int(r["total"]), r["id"]


def test_min_coins_on_non_canonical_system():
    assert min_coins([1, 3, 4], 6) == 2
    assert min_coins([1, 5, 10, 20, 25, 50], 40) == 2
