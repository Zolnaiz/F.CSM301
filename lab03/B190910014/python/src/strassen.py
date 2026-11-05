from src.matrix import Matrix, check_square
from src.matrix_multiply import matrix_multiply


def _add(x: Matrix, y: Matrix) -> Matrix:
    return [[p + q for p, q in zip(rx, ry)] for rx, ry in zip(x, y)]


def _sub(x: Matrix, y: Matrix) -> Matrix:
    return [[p - q for p, q in zip(rx, ry)] for rx, ry in zip(x, y)]


def _split(m: Matrix, h: int) -> tuple[Matrix, Matrix, Matrix, Matrix]:
    """M-г M11, M12, M21, M22 дэд матрицад хуваана."""
    return (
        [row[:h] for row in m[:h]],
        [row[h:] for row in m[:h]],
        [row[:h] for row in m[h:]],
        [row[h:] for row in m[h:]],
    )


def _strassen(a: Matrix, b: Matrix, cutoff: int = 1) -> tuple[Matrix, int]:
    n = len(a)
    if n == 1:
        return [[a[0][0] * b[0][0]]], 1
    if n <= cutoff:  # сайжруулалт: жижиг n дээр давталттай арга
        return matrix_multiply(a, b)

    # 1-р алхам: дэд матрицад хуваах
    h = n // 2
    a11, a12, a21, a22 = _split(a, h)
    b11, b12, b21, b22 = _split(b, h)

    # 2-р алхам: S1, ..., S10
    s1 = _sub(b12, b22)
    s2 = _add(a11, a12)
    s3 = _add(a21, a22)
    s4 = _sub(b21, b11)
    s5 = _add(a11, a22)
    s6 = _add(b11, b22)
    s7 = _sub(a12, a22)
    s8 = _add(b21, b22)
    s9 = _sub(a11, a21)
    s10 = _add(b11, b12)

    # 3-р алхам: P1, ..., P7 — 8 биш 7 дахин дуудалт
    p1, m1 = _strassen(a11, s1, cutoff)
    p2, m2 = _strassen(s2, b22, cutoff)
    p3, m3 = _strassen(s3, b11, cutoff)
    p4, m4 = _strassen(a22, s4, cutoff)
    p5, m5 = _strassen(s5, s6, cutoff)
    p6, m6 = _strassen(s7, s8, cutoff)
    p7, m7 = _strassen(s9, s10, cutoff)

    # 4-р алхам: C11, C12, C21, C22
    c11 = _add(_sub(_add(p5, p4), p2), p6)
    c12 = _add(p1, p2)
    c21 = _add(p3, p4)
    c22 = _sub(_sub(_add(p5, p1), p3), p7)

    c = [r1 + r2 for r1, r2 in zip(c11, c12)] + [r1 + r2 for r1, r2 in zip(c21, c22)]
    return c, m1 + m2 + m3 + m4 + m5 + m6 + m7


def strassen(a: Matrix, b: Matrix, cutoff: int = 1) -> tuple[Matrix, int]:
    """Штрассены алгоритм. C = A·B ба скаляр үржүүлэлтийн тоог буцаана.

    cutoff = 1 бол лекцийн цэвэр Штрассен; n ≤ cutoff үед давталттай арга руу шилжинэ (сайжруулалт).
    """
    n = check_square(a, b)
    if n == 0 or n & (n - 1):
        raise ValueError("n нь 2-ын зэрэг байх ёстой")
    if cutoff < 1:
        raise ValueError("cutoff ≥ 1 байх ёстой")
    return _strassen(a, b, cutoff)
