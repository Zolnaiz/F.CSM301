from src.caching import cache_misses
from tests.tsv import ints, rows

CASES = rows("caching_01.tsv")


def test_furthest_in_future_miss_count():
    for r in CASES:
        got = cache_misses(int(r["k"]), ints(r["requests"]))
        assert got == int(r["furthest"]), r["id"]
