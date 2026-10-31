def matrix_chain_order(p: list[int]) -> tuple[int, str]:
    """Matrix-Chain-Order ба Print-Optimal-Parens (CLRS 14.2).

    A_i нь p[i-1] × p[i] хэмжээтэй. m[i][j]: A_i…A_j-г үржүүлэх скаляр үржүүлэлтийн хамгийн бага
    тоо, s[i][j]: хамгийн сүүлд хуваах цэг k. Хугацаа Θ(n³), санах ой Θ(n²).
    """
    n = len(p) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):  # гинжийн урт
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    def parens(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        return "(" + parens(i, s[i][j]) + parens(s[i][j] + 1, j) + ")"

    return m[1][n], parens(1, n)
