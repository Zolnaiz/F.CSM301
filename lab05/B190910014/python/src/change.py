def make_change(d: list[int], x: int) -> list[int]:
    """Хариулт мөнгө — кассчны (хомхойлох) арга: хамгийн их дүнгээс эхлэн аль болох олныг авна.

    d нь өсөх дараалалтай, d[0] = 1. Нэрлэсэн дүн бүрээс авсан тоог d-ийн дарааллаар буцаана.
    Хугацаа Θ(m). Каноник системд (жишээ нь төгрөг) хамгийн цөөн дэвсгэрт өгнө.
    """
    if not d or d[0] != 1 or any(a >= b for a, b in zip(d, d[1:])):
        raise ValueError("d нь 1-ээс эхэлсэн өсөх дараалал байх ёстой")
    if x < 0:
        raise ValueError("x сөрөг байж болохгүй")
    counts = [0] * len(d)
    for j in range(len(d) - 1, -1, -1):
        counts[j], x = divmod(x, d[j])
    return counts


def min_coins(d: list[int], x: int) -> int:
    """Уншлага (а): хамгийн цөөн дэвсгэртийн тоо — динамик программчлал.

    best[y] = 1 + min(best[y − dⱼ]), dⱼ ≤ y. Хугацаа Θ(m·x), санах ой Θ(x).
    """
    if x < 0:
        raise ValueError("x сөрөг байж болохгүй")
    inf = x + 1
    best = [0] + [inf] * x
    coins = sorted(d)
    for y in range(1, x + 1):
        b = inf
        for c in coins:
            if c > y:
                break
            if best[y - c] + 1 < b:
                b = best[y - c] + 1
        best[y] = b
    if best[x] == inf:
        raise ValueError(f"{x}-ийг {d} дүнгүүдээр бүрдүүлэх боломжгүй")
    return best[x]


def min_coins_table(d: list[int], limit: int) -> list[int]:
    """0…limit бүх дүнгийн хамгийн цөөн тоо (Козен–Заксын мужийг нэг дор шалгахад)."""
    inf = limit + 1
    best = [0] + [inf] * limit
    for y in range(1, limit + 1):
        best[y] = 1 + min(best[y - c] for c in d if c <= y)
    return best


def first_counterexample(d: list[int]) -> int | None:
    """Козен–Заксын теорем: c₃ < x < c_(m−1) + c_m мужид хомхойлох арга оновчгүй хамгийн бага x."""
    if len(d) < 3:
        return None
    hi = d[-2] + d[-1]
    best = min_coins_table(d, hi)
    for x in range(d[2] + 1, hi):
        if sum(make_change(d, x)) != best[x]:
            return x
    return None
