def _search(a: list[int], x: int, p: int, r: int) -> tuple[int, int]:
    """Recursive-Binary-Search(A, x, p, r). (товъёг, дуудалтын тоо)-г буцаана."""
    if p > r:
        return -1, 1
    q = (p + r) // 2
    if a[q] == x:
        return q, 1
    if a[q] < x:
        index, calls = _search(a, x, q + 1, r)
    else:
        index, calls = _search(a, x, p, q - 1)
    return index, calls + 1


def binary_search(a: list[int], x: int) -> tuple[int, int]:
    """Эрэмбэлэгдсэн, давхардалгүй жагсаалтаас хайх.

    Олдсон товъёг (0-ээс эхэлсэн, олдохгүй бол -1) болон эхний дуудалтыг
    оролцуулсан нийт дуудалтын тоог буцаана.
    """
    return _search(a, x, 0, len(a) - 1)
