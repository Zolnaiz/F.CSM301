import math
import pytest

from src.binary_insertion_sort import binary_insertion_sort
from src.insertion_sort import insertion_sort
from tests.tsv import ints, rows

SORT = rows("sort_01.tsv")
SHIFTS = rows("insertion_shifts_01.tsv")


@pytest.mark.parametrize("r", SORT, ids=[r["id"] for r in SORT])
def test_sorts(r):
    got, _, _ = binary_insertion_sort(ints(r["input"]))
    assert got == ints(r["expected"])


@pytest.mark.parametrize("r", SHIFTS, ids=[r["id"] for r in SHIFTS])
def test_shift_count_matches_task_one(r):
    _, _, shifts = binary_insertion_sort(ints(r["input"]))
    assert shifts == int(r["shifts"])


@pytest.mark.parametrize("r", SHIFTS, ids=[r["id"] for r in SHIFTS])
def test_comparison_bound(r):
    n = int(r["n"])
    if n < 2:
        pytest.skip("n < 2")
    _, cmps, _ = binary_insertion_sort(ints(r["input"]))
    assert cmps <= n * math.ceil(math.log2(n))


def test_stable_for_equal_keys():
    _, _, shifts = binary_insertion_sort([5] * 16)
    assert shifts == 0


def test_agrees_with_insertion_sort():
    import random

    rng = random.Random(2)
    for _ in range(20):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        exp, exp_shifts = insertion_sort(list(a))
        got, _, got_shifts = binary_insertion_sort(list(a))
        assert got == exp
        assert got_shifts == exp_shifts
