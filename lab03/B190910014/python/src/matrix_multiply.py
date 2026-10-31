from src.matrix import Matrix, check_square, zeros


def matrix_multiply(a: Matrix, b: Matrix) -> tuple[Matrix, int]:
    """Matrix-Multiply(A, B, C, n).

    C = A·B үржвэр болон скаляр үржүүлэлтийн тоог буцаана.
    """
    n = check_square(a, b)
    c = zeros(n)  # 4-р мөр C-д нэмдэг тул эхлээд тэглэнэ: Θ(n²)
    mults = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i][j] = c[i][j] + a[i][k] * b[k][j]
                mults += 1
    return c, mults
