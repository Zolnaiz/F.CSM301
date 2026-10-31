import pytest

from src.insertion_sort import insertion_sort
from tests.tsv import ints, rows

CASES = rows("insertion_shifts_01.tsv")
SORT = rows("sort_01.tsv")


@pytest.mark.parametrize("r", SORT, ids=[r["id"] for r in SORT])
def test_sorts(r):
    a = ints(r["input"])
    got, _ = insertion_sort(list(a))
    assert got == ints(r["expected"])


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_shift_count(r):
    _, shifts = insertion_sort(ints(r["input"]))
    assert shifts == int(r["shifts"])


def test_reverse_sorted_is_n_choose_2():
    for n in (4, 8, 16, 64):
        _, shifts = insertion_sort(list(range(n, 0, -1)))
        assert shifts == n * (n - 1) // 2


def test_already_sorted_needs_no_shift():
    _, shifts = insertion_sort(list(range(1, 33)))
    assert shifts == 0
