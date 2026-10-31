def lcs_length(x: str, y: str) -> int:
    """LCS-Length (CLRS 14.4). c[i][j]: x[:i], y[:j]-ийн хамгийн урт ерөнхий дэд дарааллын урт.

    Хүснэгтийг мөр мөрөөр бөглөдөг ба зөвхөн өмнөх мөр хэрэгтэй тул хоёр мөр хадгална:
    хугацаа Θ(mn), санах ой Θ(n).
    """
    m, n = len(x), len(y)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]
