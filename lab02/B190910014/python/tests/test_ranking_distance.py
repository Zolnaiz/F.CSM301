import pytest

from src.ranking_distance import ranking_distance
from tests.tsv import ints, rows

CASES = rows("ranking_distance_01.tsv")


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_distance(r):
    assert ranking_distance(ints(r["A"]), ints(r["B"])) == int(r["expected"])


def test_identical_is_zero():
    a = list(range(1, 51))
    assert ranking_distance(a, list(a)) == 0


def test_reversed_is_maximum():
    for n in (2, 5, 10, 50):
        a = list(range(1, n + 1))
        assert ranking_distance(a, a[::-1]) == n * (n - 1) // 2
