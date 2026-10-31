import random

import pytest

from src.matrix_multiply import matrix_multiply
from src.matrix_multiply_recursive import matrix_multiply_recursive
from tests.tsv import matrix, rows

CASES = rows("matmul_01.tsv")
IDS = [f"n={r['n']}#{i}" for i, r in enumerate(CASES, 1)]


# (a) хариу болон үржүүлэлтийн тоо 2-р даалгавартай яг ижил
@pytest.mark.parametrize("r", CASES, ids=IDS)
def test_same_as_iterative(r):
    a, b = matrix(r["A"]), matrix(r["B"])
    c, mults = matrix_multiply_recursive(a, b)
    assert c == matrix(r["expected"])
    assert (c, mults) == matrix_multiply(a, b)


def test_random_16x16_and_32x32():
    rng = random.Random(3)
    for n in (16, 32):
        a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        b = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        assert matrix_multiply_recursive(a, b) == matrix_multiply(a, b)


@pytest.mark.parametrize("a,b", [("1,2;3,4", "1,2,3;4,5,6;7,8,9"), ("1,2,3;4,5,6;7,8,9", "1,2,3;4,5,6;7,8,9")])
def test_bad_size_raises(a, b):
    """Хэмжээ таарахгүй эсвэл n нь 2-ын зэрэг биш (3×3)."""
    with pytest.raises(ValueError):
        matrix_multiply_recursive(matrix(a), matrix(b))
