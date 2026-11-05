from src.matrix_multiply import matrix_multiply

MOD = 10**9 + 7
M = [[1, 1], [1, 0]]
IDENTITY = [[1, 0], [0, 1]]


def _mul(x: list[list[int]], y: list[list[int]]) -> tuple[list[list[int]], int]:
    """1-р бодлогын matrix_multiply-аар үржүүлээд mod p авна (тоо хязгаартай хэвээр)."""
    c, mults = matrix_multiply(x, y)
    return [[v % MOD for v in row] for row in c], mults


def fib_matrix(n: int) -> tuple[int, int]:
    """F_n mod (10⁹ + 7) ба скаляр үржүүлэлтийн тоог буцаана.

    Mⁿ = [[F(n+1), F(n)], [F(n), F(n−1)]], M = [[1, 1], [1, 0]]. Зэргийг хэсэгчилнэ:
    Mⁿ = (M^⌊n/2⌋)², сондгой n үед дахин M-ээр үржүүлнэ. T(n) = T(n/2) + Θ(1) = Θ(lg n)
    удаа 2×2 матриц үржүүлнэ (тус бүр 8 скаляр үржүүлэлт).
    """
    if n < 0:
        raise ValueError("n сөрөг байж болохгүй")

    def power(k: int) -> tuple[list[list[int]], int]:
        if k == 0:
            return IDENTITY, 0
        half, mults = power(k // 2)  # дэд бодлогыг ганцхан удаа
        square, m2 = _mul(half, half)
        mults += m2
        if k % 2 == 1:
            square, m3 = _mul(square, M)
            mults += m3
        return square, mults

    mk, mults = power(n)
    return mk[0][1], mults
