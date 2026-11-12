def cache_misses(k: int, requests: list[int]) -> int:
    """Оновчтой кэш (B төвшин): furthest-in-future хомхойлох арга.

    Хуудас кэшид байхгүй бол алдаа +1. Кэш дүүрсэн үед кэш дэх хуудас бүрийн дараагийн
    хандалтыг цаашаа шугаман хайлтаар (list.index) олж, хамгийн хойно хандагдах (эсвэл огт
    хандагдахгүй) хуудсыг хасна. Нэг хасалт O(k·n) тул хамгийн муу үед O(n²·k).
    """
    if k < 0:
        raise ValueError("k сөрөг байж болохгүй")
    if k == 0:
        return len(requests)
    cache: set[int] = set()
    misses = 0
    for i, page in enumerate(requests):
        if page in cache:
            continue
        misses += 1
        if len(cache) == k:
            victim, furthest = None, -1
            for q in cache:
                try:
                    nxt = requests.index(q, i + 1)
                except ValueError:  # цаашид огт хандагдахгүй — шууд хасна
                    victim = q
                    break
                if nxt > furthest:
                    victim, furthest = q, nxt
            cache.remove(victim)
        cache.add(page)
    return misses
