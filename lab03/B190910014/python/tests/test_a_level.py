"""A түвшин: fib_matrix, сайжруулсан Гаусс, Якобийн арга, cutoff-той Штрассен."""
import random

import pytest

from src.fib_matrix import MOD, fib_matrix
from src.gauss import gauss_fast_ops, gauss_ops, gauss_solve, gauss_solve_fast, jacobi_solve
from src.matrix_multiply import matrix_multiply
from src.strassen import strassen
from tests.tsv import matrix, rows, vector


def test_fib_matrix_matches_bottom_up():
    f = [0, 1]
    for _ in range(2, 1001):
        f.append((f[-1] + f[-2]) % MOD)
    for n in range(0, 1001):
        value, mults = fib_matrix(n)
        assert value == f[n], n
        if n >= 1:  # (⌊lg n⌋ + 1) квадрат + (n-ийн 1 битийн тоо) нэмэлт үржвэр, тус бүр 8
            assert mults == 8 * (n.bit_length() + bin(n).count("1")), n


def test_fib_matrix_negative_raises():
    with pytest.raises(ValueError):
        fib_matrix(-1)


@pytest.mark.parametrize("r", rows("gauss_01.tsv"), ids=lambda r: r["id"])
def test_gauss_fast_solution(r):
    a, b = matrix(r["A"]), vector(r["b"])
    x, ops = gauss_solve_fast(a, b)
    assert x == pytest.approx(vector(r["x"]), abs=1e-9)
    n = int(r["n"])
    assert ops == gauss_fast_ops(n) == gauss_ops(n) - n * (n - 1)


def test_gauss_fast_random():
    rng = random.Random(5)
    for n in (1, 3, 20, 100):
        a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] = sum(abs(v) for j, v in enumerate(a[i]) if j != i) + 1
        b = [rng.randint(-50, 50) for _ in range(n)]
        assert gauss_solve_fast(a, b)[0] == pytest.approx(gauss_solve(a, b)[0], abs=1e-9)


@pytest.mark.parametrize("r", rows("gauss_01.tsv"), ids=lambda r: r["id"])
def test_jacobi_solution(r):
    a, b = matrix(r["A"]), vector(r["b"])
    x, ops, iters = jacobi_solve(a, b)
    assert x == pytest.approx(vector(r["x"]), abs=1e-9)
    n = int(r["n"])
    assert 1 <= iters < 1000 and ops == iters * 2 * n * n  # нэг давталт = нэг матриц–вектор


def test_jacobi_random_matches_gauss():
    rng = random.Random(7)
    for n in (1, 3, 20, 100, 200):
        a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] = sum(abs(v) for j, v in enumerate(a[i]) if j != i) + 1
        b = [rng.randint(-50, 50) for _ in range(n)]
        assert jacobi_solve(a, b)[0] == pytest.approx(gauss_solve(a, b)[0], rel=1e-9, abs=1e-9)
    assert jacobi_solve([], []) == ([], 0, 0)


def test_jacobi_requires_diagonal_dominance():
    with pytest.raises(ValueError):
        jacobi_solve([[1, 2], [3, 4]], [1, 2])
    with pytest.raises(ValueError):
        jacobi_solve([[2, 1]], [1])


@pytest.mark.parametrize("cutoff", [2, 8, 32])
def test_strassen_cutoff(cutoff):
    rng = random.Random(cutoff)
    for n in (4, 16, 64):
        a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        b = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        c, mults = strassen(a, b, cutoff)
        assert c == matrix_multiply(a, b)[0]
        base = min(cutoff, n)
        assert mults == 7 ** ((n // base).bit_length() - 1) * base**3
