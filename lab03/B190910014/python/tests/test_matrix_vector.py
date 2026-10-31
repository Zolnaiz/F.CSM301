import pytest

from src.matrix_vector import matrix_vector, vector_hadamard
from tests.tsv import matrix, rows, vector

CASES = rows("matvec_01.tsv")


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_matrix_vector(r):
    y, ops = matrix_vector(matrix(r["A"]), vector(r["x"]))
    assert y == vector(r["expected"])
    assert ops == int(r["ops"]) == 2 * int(r["n"]) ** 2


def test_hadamard():
    w, ops = vector_hadamard([1, -2, 3, 4], [5, 6, -7, 0])
    assert w == [5, -12, -21, 0]
    assert ops == 4


def test_bad_size_raises():
    with pytest.raises(ValueError):
        matrix_vector(matrix("1,2;3,4"), vector("1,2,3"))
    with pytest.raises(ValueError):
        vector_hadamard([1, 2], [1])
