def lcs_diff(a: list[str], b: list[str]) -> list[str]:
    """Хоёр файлын мөрийн ялгааг LCS-ээр гаргана (diff).

    Хамгийн урт ерөнхий дэд дарааллын мөрүүд « » тэмдэгтэй хэвээр үлдэж, бусад нь A-аас «-»
    (устгасан), B-д «+» (нэмсэн) болно. Ингэснээр өөрчлөлтийн тоо хамгийн бага байна.

    c[i][j] нь a[i:], b[j:] сүүлүүдийн LCS-ийн урт. Сүүлээр тодорхойлсон тул ялгааг эхнээс нь
    дарааллаар нь уншиж болно. Хугацаа, санах ой Θ(mn).
    """
    m, n = len(a), len(b)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                c[i][j] = c[i + 1][j + 1] + 1
            else:
                c[i][j] = max(c[i + 1][j], c[i][j + 1])

    out = []
    i = j = 0
    while i < m and j < n:
        if a[i] == b[j]:
            out.append(" " + a[i])
            i += 1
            j += 1
        elif c[i + 1][j] >= c[i][j + 1]:  # a[i]-г хасахад LCS буурахгүй
            out.append("-" + a[i])
            i += 1
        else:
            out.append("+" + b[j])
            j += 1
    out.extend("-" + line for line in a[i:])
    out.extend("+" + line for line in b[j:])
    return out
