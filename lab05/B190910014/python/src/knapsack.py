def fractional_knapsack(w: list[int], v: list[int], W: int) -> float:
    """Хэсэгчилж авч болох үүргэвчтэй бодлого — нэгж жингийн үнээр хомхойлох арга.

    Эд зүйлсийг vᵢ/wᵢ-ээр буурахаар эрэмбэлж (Θ(n lg n)), багтаамж дуустал бүтнээр нь,
    сүүлийнхийг хэсэгчилж авна. Хамгийн их нийт үнийг буцаана.
    """
    if len(w) != len(v):
        raise ValueError("w, v ижил урттай байх ёстой")
    if W < 0 or any(x < 0 for x in w) or any(x < 0 for x in v):
        raise ValueError("жин, үнэ, багтаамж сөрөг байж болохгүй")
    # Жин нь 0 эд зүйлс багтаамж эзлэхгүй тул түрүүлж бүгдийг авна.
    total = float(sum(vi for wi, vi in zip(w, v) if wi == 0))
    items = sorted(((vi / wi, wi, vi) for wi, vi in zip(w, v) if wi > 0), reverse=True)
    room = W
    for ratio, wi, vi in items:
        if room == 0:
            break
        if wi <= room:
            total += vi
            room -= wi
        else:
            total += ratio * room
            room = 0
    return total
