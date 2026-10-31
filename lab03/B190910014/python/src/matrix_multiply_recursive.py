from src.matrix import Matrix, check_square, zeros


def _recurse(a: Matrix, b: Matrix, c: Matrix, i: int, j: int, k: int, n: int) -> int:
    """C[i.., j..] += A[i.., k..] · B[k.., j..] (n×n дэд матрицууд).

    Дэд матрицыг хуулахгүй, зүүн дээд булангийн товъёгоор (i, j, k) дамжуулна.
    Скаляр үржүүлэлтийн тоог буцаана.
    """
    if n == 1:
        c[i][j] = c[i][j] + a[i][k] * b[k][j]
        return 1
    h = n // 2
    mults = 0
    mults += _recurse(a, b, c, i,     j,     k,     h)  # C11 += A11·B11
    mults += _recurse(a, b, c, i,     j + h, k,     h)  # C12 += A11·B12
    mults += _recurse(a, b, c, i + h, j,     k,     h)  # C21 += A21·B11
    mults += _recurse(a, b, c, i + h, j + h, k,     h)  # C22 += A21·B12
    mults += _recurse(a, b, c, i,     j,     k + h, h)  # C11 += A12·B21
    mults += _recurse(a, b, c, i,     j + h, k + h, h)  # C12 += A12·B22
    mults += _recurse(a, b, c, i + h, j,     k + h, h)  # C21 += A22·B21
    mults += _recurse(a, b, c, i + h, j + h, k + h, h)  # C22 += A22·B22
    return mults


def matrix_multiply_recursive(a: Matrix, b: Matrix) -> tuple[Matrix, int]:
    """Matrix-Multiply-Recursive(A, B, C, n). n нь 2-ын зэрэг байна."""
    n = check_square(a, b)
    if n == 0 or n & (n - 1):
        raise ValueError("n нь 2-ын зэрэг байх ёстой")
    c = zeros(n)
    mults = _recurse(a, b, c, 0, 0, 0, n)
    return c, mults
