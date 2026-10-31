import pytest

from src.merge_sort import merge_sort
from tests.tsv import ints, rows

CASES = rows("merge_writes_01.tsv")
SORT = rows("sort_01.tsv")


@pytest.mark.parametrize("r", SORT, ids=[r["id"] for r in SORT])
def test_sorts(r):
    got, _ = merge_sort(ints(r["input"]))
    assert got == ints(r["expected"])


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_write_count(r):
    _, writes = merge_sort(ints(r["input"]))
    assert writes == int(r["writes"])


def test_power_of_two_is_n_lg_n():
    for k in range(1, 11):
        n = 1 << k
        _, writes = merge_sort(list(range(n, 0, -1)))
        assert writes == n * k


def test_write_count_independent_of_content():
    """Ижил урттай өөр агуулга -> бичилтийн тоо ижил."""
    counts = {
        merge_sort(a)[1]
        for a in (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [8, 7, 6, 5, 4, 3, 2, 1],
            [3, 1, 4, 1, 5, 9, 2, 6],
        )
    }
    assert len(counts) == 1
