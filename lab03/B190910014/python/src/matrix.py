"""Матрицын туслах функцүүд."""

Matrix = list[list[int]]


def check_square(a: Matrix, b: Matrix) -> int:
    """A, B хоёулаа ижил n×n хэмжээтэй эсэхийг шалгаж, n-г буцаана."""
    n = len(a)
    if len(b) != n or any(len(row) != n for row in a) or any(len(row) != n for row in b):
        raise ValueError("A ба B ижил n×n хэмжээтэй байх ёстой")
    return n


def zeros(n: int) -> Matrix:
    return [[0] * n for _ in range(n)]
