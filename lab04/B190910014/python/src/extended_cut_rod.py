def extended_bottom_up_cut_rod(p: list[int]) -> tuple[int, list[int]]:
    """Extended-Bottom-Up-Cut-Rod (CLRS 14.1) ба Print-Cut-Rod-Solution.

    s[j]: j урттай саваанаас эхлээд огтлох хэсгийн оновчтой урт. Хамгийн их орлого болон
    хэсгүүдийн уртын жагсаалтыг буцаана.
    """
    n = len(p)
    r = [0] * (n + 1)
    s = [0] * (n + 1)
    for j in range(1, n + 1):
        q = float("-inf")
        for i in range(1, j + 1):
            if p[i - 1] + r[j - i] > q:
                q = p[i - 1] + r[j - i]
                s[j] = i
        r[j] = q

    cuts = []
    while n > 0:  # s-ийг дагаж хэсгүүдийг сэргээнэ
        cuts.append(s[n])
        n -= s[n]
    return r[len(p)], cuts
