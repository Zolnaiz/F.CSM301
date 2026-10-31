import math
import random

import pytest

from src.matrix_multiply import matrix_multiply
from src.strassen import strassen
from tests.tsv import matrix, rows

CASES = rows("matmul_01.tsv")
COUNTS = rows("strassen_counts_01.tsv")

# Python дээр n = 128-аас дээш нь удаан тул тоог бодитоор ажиллуулж шалгахгүй.
RUN_LIMIT = 64


# (a) хариу 2, 3-р даалгавартай ижил
@pytest.mark.parametrize("r", CASES, ids=[f"n={r['n']}#{i}" for i, r in enumerate(CASES, 1)])
def test_product(r):
    c, _ = strassen(matrix(r["A"]), matrix(r["B"]))
    assert c == matrix(r["expected"])


def test_random_matches_iterative():
    rng = random.Random(7)
    for n in (16, 32):
        a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        b = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        assert strassen(a, b)[0] == matrix_multiply(a, b)[0]


# (b) үржүүлэлтийн тоо яг 7^lg n = n^lg 7
@pytest.mark.parametrize("r", COUNTS, ids=[f"n={r['n']}" for r in COUNTS])
def test_mult_count(r):
    n = int(r["n"])
    expected = int(r["strassen_mults"])
    assert expected == 7 ** int(math.log2(n))
    assert int(r["naive_mults"]) == n ** 3
    if n > RUN_LIMIT:
        pytest.skip(f"n={n}: Python дээр удаан, тоог зөвхөн томьёогоор шалгав")
    zero = [[0] * n for _ in range(n)]
    _, mults = strassen(zero, zero)
    assert mults == expected


def test_bad_size_raises():
    with pytest.raises(ValueError):
        strassen(matrix("1,2,3;4,5,6;7,8,9"), matrix("1,2,3;4,5,6;7,8,9"))
