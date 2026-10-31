import pytest

from src.matrix_multiply import matrix_multiply
from tests.tsv import matrix, rows

CASES = rows("matmul_01.tsv")
IDS = [f"n={r['n']}#{i}" for i, r in enumerate(CASES, 1)]


# (a) matmul_01.tsv-ийн хариу
@pytest.mark.parametrize("r", CASES, ids=IDS)
def test_product(r):
    c, _ = matrix_multiply(matrix(r["A"]), matrix(r["B"]))
    assert c == matrix(r["expected"])


# (d) скаляр үржүүлэлтийн тоо яг n³
@pytest.mark.parametrize("r", CASES, ids=IDS)
def test_mults_is_n_cubed(r):
    n = int(r["n"])
    _, mults = matrix_multiply(matrix(r["A"]), matrix(r["B"]))
    assert mults == n ** 3


# (b) C-г тэглэхгүй бол хоёр дахь дуудалтад өмнөх үр дүн нэмэгдэнэ
def test_second_call_gives_same_result():
    a = matrix("1,2;3,4")
    b = matrix("5,6;7,8")
    first, _ = matrix_multiply(a, b)
    second, _ = matrix_multiply(a, b)
    assert first == second == matrix("19,22;43,50")


# (c) хэмжээ таарахгүй
@pytest.mark.parametrize(
    "a,b",
    [
        ("1,2;3,4", "1,2,3;4,5,6;7,8,9"),  # 2×2 ба 3×3
        ("1,2,3;4,5,6", "1,2;3,4"),        # A нь 2×3, дөрвөлжин биш
        ("1,2;3,4", "1,2;3"),              # B-ийн мөр дутуу
    ],
)
def test_size_mismatch_raises(a, b):
    with pytest.raises(ValueError):
        matrix_multiply(matrix(a), matrix(b))
