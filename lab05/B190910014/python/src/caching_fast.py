"""Оновчтой кэш — сайжруулсан (A төвшин).

1. next_use[i] — requests[i] хуудасны дараагийн хандалтын байрлал (байхгүй бол ∞).
   Төгсгөлөөс эхэн рүү нэг гүйж толиор Θ(n) хугацаанд олно.
2. Кэш дэх хуудсуудыг дараагийн хандалтаар нь хамгийн их овоо (heap)-д хадгална. Хуудсанд
   дахин хандахад шинэ (next_use, хуудас) оруулж, хуучныг «хуучирсан» гэж үлдээнэ (lazy
   deletion). Хасахдаа хуучирсан оролтыг алгасаж, оройг авна. Овооны хэмжээ 4k + 64-өөс
   хэтэрвэл кэшийн одоогийн k оролтоос шинээр байгуулна (хорогдуулсан O(1)), тиймээс овоо O(k).
Нийт O(n lg k) хугацаа, O(n) санах ой (next_use массив). Анхных O(n²·k) хугацаа, O(k) санах ой.
"""
import heapq


def next_use(requests: list[int]) -> list[int]:
    n = len(requests)
    nxt = [0] * n
    last: dict[int, int] = {}
    for i in range(n - 1, -1, -1):
        nxt[i] = last.get(requests[i], n)  # n нь «∞»
        last[requests[i]] = i
    return nxt


def cache_misses_fast(k: int, requests: list[int]) -> int:
    if k < 0:
        raise ValueError("k сөрөг байж болохгүй")
    if k == 0:
        return len(requests)
    nxt = next_use(requests)
    cache: dict[int, int] = {}  # хуудас → дараагийн хандалт
    heap: list[tuple[int, int]] = []  # (−дараагийн хандалт, хуудас)
    misses = 0
    for i, page in enumerate(requests):
        if page not in cache:
            misses += 1
            if len(cache) == k:
                while True:
                    neg, victim = heapq.heappop(heap)
                    if cache.get(victim) == -neg:  # хуучирсан оролт биш
                        del cache[victim]
                        break
        cache[page] = nxt[i]
        heapq.heappush(heap, (-nxt[i], page))
        if len(heap) > 4 * k + 64:  # хуучирсан оролтыг цэвэрлэж heap-ийг O(k) хэмжээнд барина
            heap = [(-nu, p) for p, nu in cache.items()]
            heapq.heapify(heap)
    return misses
