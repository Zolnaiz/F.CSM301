def gauss_solve(a: list[list[float]], b: list[float]) -> tuple[list[float], int]:
    """Гауссын арга (мөрийн хувиргалтгүй). Шийд x ба *, /, +, - үйлдлийн тоог буцаана."""
    n = len(a)
    if len(b) != n or any(len(row) != n for row in a):
        raise ValueError("A нь n×n, b нь n урттай байх ёстой")
    m = [[float(v) for v in row] for row in a]  # оролтыг өөрчлөхгүйн тулд хуулна
    v = [float(x) for x in b]
    ops = 0

    # Шууд явц: k-р баганын доорх гишүүдийг тэглэнэ.
    for k in range(n - 1):
        if m[k][k] == 0:
            raise ValueError("хувиргалтын гишүүн тэг боллоо")
        for i in range(k + 1, n):
            factor = m[i][k] / m[k][k]
            ops += 1
            for j in range(k, n):
                m[i][j] = m[i][j] - factor * m[k][j]
                ops += 2
            v[i] = v[i] - factor * v[k]
            ops += 2

    # Буцах орлуулга: доороос дээш x-ийг олно.
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = 0.0
        for j in range(i + 1, n):
            s = s + m[i][j] * x[j]
            ops += 2
        x[i] = (v[i] - s) / m[i][i]
        ops += 2
    return x, ops


def gauss_ops(n: int) -> int:
    """gauss_solve-ийн үйлдлийн тоо: (4n³ + 15n² − 7n) / 6 ≈ ⅔n³."""
    return (4 * n**3 + 15 * n**2 - 7 * n) // 6
