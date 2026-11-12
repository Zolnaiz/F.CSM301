"""Харьцуулах зорилготой онлайн бодлогууд: FIFO ба LRU (ирээдүйг мэдэхгүй).

caching_01.tsv-ийн fifo, lru баганатай тулгаж шалгана. Furthest-in-future нь ирээдүйг мэддэг
(offline) учраас эдгээрээс ямагт цөөн буюу тэнцүү алдаатай байна.
"""
from collections import OrderedDict, deque


def fifo_misses(k: int, requests: list[int]) -> int:
    cache: set[int] = set()
    order: deque[int] = deque()
    misses = 0
    for page in requests:
        if page in cache:
            continue
        misses += 1
        if k == 0:
            continue
        if len(cache) == k:
            cache.remove(order.popleft())
        cache.add(page)
        order.append(page)
    return misses


def lru_misses(k: int, requests: list[int]) -> int:
    cache: OrderedDict[int, None] = OrderedDict()
    misses = 0
    for page in requests:
        if page in cache:
            cache.move_to_end(page)
            continue
        misses += 1
        if k == 0:
            continue
        if len(cache) == k:
            cache.popitem(last=False)
        cache[page] = None
    return misses
