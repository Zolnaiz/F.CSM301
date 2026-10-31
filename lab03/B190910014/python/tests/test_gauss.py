import random

import pytest

from src.gauss import gauss_ops, gauss_solve
from tests.tsv import matrix, rows, vector

CASES = rows("gauss_01.tsv")


def diagonally_dominant(n: int, seed: int) -> list[list[int]]:
    """Мөр бүрийн диагоналийн гишүүн бусдын үнэмлэхүй нийлбэрээс их матриц."""
    rng = random.Random(seed)
    a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        a[i][i] = sum(abs(v) for j, v in enumerate(a[i]) if j != i) + rng.randint(1, 9)
    return a


# (b) gauss_01.tsv: шийд ба үйлдлийн тоо
@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_solution(r):
    x, _ = gauss_solve(matrix(r["A"]), vector(r["b"]))
    assert x == pytest.approx(vector(r["x"]), abs=1e-9)


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_ops(r):
    _, ops = gauss_solve(matrix(r["A"]), vector(r["b"]))
    assert ops == int(r["ops"]) == gauss_ops(int(r["n"]))


# (b) n = 10, 50, 100, 200 үед үйлдлийн тоо ⅔n³ уруу дөхнө
def test_ops_approach_two_thirds_n_cubed():
    ratios = []
    for n in (10, 50, 100, 200):
        a = diagonally_dominant(n, n)
        x_true = [random.Random(n + 1).randint(-5, 5) for _ in range(n)]
        b = [sum(a[i][j] * x_true[j] for j in range(n)) for i in range(n)]
        x, ops = gauss_solve(a, b)
        assert x == pytest.approx(x_true, abs=1e-6)
        assert ops == gauss_ops(n)
        ratios.append(ops / (2 * n**3 / 3))
    assert ratios == sorted(ratios, reverse=True)  # 1 уруу буурна
    assert ratios[-1] < 1.02


def test_bad_size_raises():
    with pytest.raises(ValueError):
        gauss_solve(matrix("1,2;3,4"), vector("1,2,3"))
