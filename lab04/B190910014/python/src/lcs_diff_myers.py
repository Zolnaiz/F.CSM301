def lcs_diff_myers(a: list[str], b: list[str]) -> list[str]:
    """Сайжруулсан diff: Myers-ийн O((N+M)·D) алгоритм (git diff-ийн үндсэн арга).

    Засварын граф дээр (0,0)-оос (N,M) хүртэлх замд «баруун» = A-аас хасах, «доош» = B-д нэмэх,
    «диагональ» = ижил мөр (үнэгүй). D = хасах + нэмэх алхмын хамгийн бага тоо бөгөөд
    D = N + M − 2·LCS тул ижил мөрийн тоо LCS-тэй тэнцүү, хариу нь lcs_diff-тэй ижил оновчтой.

    v[k]: d алхмаар k = x − y диагональ дээр хүрч болох хамгийн хол x. Хугацаа O((N+M)·D),
    санах ой O(D²) (буцаж замаа сэргээхийн тулд d бүрийн v-г хадгална). Файлууд бага зэрэг
    ялгаатай (D ≪ N) үед хүснэгтийн Θ(NM)-ээс хамаагүй хурдан.
    """
    n, m = len(a), len(b)
    v = {1: 0}
    trace = []
    found = False
    for d in range(n + m + 1):
        trace.append(dict(v))  # d алхмын өмнөх төлөв
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v[k - 1] < v[k + 1]):
                x = v[k + 1]  # доош: B-ээс нэмнэ
            else:
                x = v[k - 1] + 1  # баруун: A-аас хасна
            y = x - k
            while x < n and y < m and a[x] == b[y]:  # диагональ «могой»
                x += 1
                y += 1
            v[k] = x
            if x >= n and y >= m:
                found = True
                break
        if found:
            break

    # (n, m)-ээс буцаж замыг сэргээнэ.
    out = []
    x, y = n, m
    for d in range(len(trace) - 1, -1, -1):
        vd = trace[d]
        k = x - y
        if k == -d or (k != d and vd[k - 1] < vd[k + 1]):
            prev_k = k + 1
        else:
            prev_k = k - 1
        prev_x = vd[prev_k] if d > 0 else 0
        prev_y = prev_x - prev_k if d > 0 else 0
        while x > prev_x and y > prev_y:  # диагональ: ижил мөр
            x -= 1
            y -= 1
            out.append(" " + a[x])
        if d > 0:
            if x == prev_x:
                out.append("+" + b[prev_y])  # доош
            else:
                out.append("-" + a[prev_x])  # баруун
        x, y = prev_x, prev_y
    out.reverse()
    return out
