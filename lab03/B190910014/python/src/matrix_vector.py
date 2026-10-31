def matrix_vector(a: list[list[int]], x: list[int]) -> tuple[list[int], int]:
    """y = A·x. Мөр бүрд n үржүүлэх + n нэмэх тул нийт 2n² үйлдэл."""
    n = len(a)
    if len(x) != n or any(len(row) != n for row in a):
        raise ValueError("A нь n×n, x нь n урттай байх ёстой")
    y = [0] * n
    ops = 0
    for i in range(n):
        for j in range(n):
            y[i] = y[i] + a[i][j] * x[j]
            ops += 2
    return y, ops


def vector_hadamard(u: list[int], v: list[int]) -> tuple[list[int], int]:
    """w_i = u_i · v_i. n үржүүлэх үйлдэл."""
    if len(u) != len(v):
        raise ValueError("векторууд ижил урттай байх ёстой")
    return [p * q for p, q in zip(u, v)], len(u)
