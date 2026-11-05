def recursive_matrix_chain(p: list[int]) -> tuple[int, int]:
    """Энгийн шийдэл: Recursive-Matrix-Chain (CLRS 14.3), хүснэгтгүй дахин дуудалт.

    m(i, j) = min_{i≤k<j} m(i, k) + m(k+1, j) + p[i−1]·p[k]·p[j]-г шууд дахин дуудна. Ижил
    (i, j) дэд бодлогыг олон дахин бодох тул T(n) = Ω(2ⁿ) (дуудалт яг 3^(n−1)).
    Хамгийн бага өртөг болон дуудалтын тоог буцаана.
    """
    calls = 0

    def m(i: int, j: int) -> int:
        nonlocal calls
        calls += 1
        if i == j:
            return 0
        best = None
        for k in range(i, j):
            q = m(i, k) + m(k + 1, j) + p[i - 1] * p[k] * p[j]
            if best is None or q < best:
                best = q
        return best

    cost = m(1, len(p) - 1)
    return cost, calls
