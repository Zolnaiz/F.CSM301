def _merge(a: list[int], p: int, q: int, r: int) -> int:
    """A[p..q], A[q+1..r] хоёр эрэмбэлэгдсэн хэсгийг нэгтгэнэ.

    A[k] = ... хэлбэрийн утга олгосон тоог буцаана.
    """
    left = a[p : q + 1]
    right = a[q + 1 : r + 1]
    n_left, n_right = len(left), len(right)
    i = j = 0
    k = p
    writes = 0
    while i < n_left and j < n_right:
        if left[i] <= right[j]:
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        k += 1
        writes += 1
    while i < n_left:
        a[k] = left[i]
        i += 1
        k += 1
        writes += 1
    while j < n_right:
        a[k] = right[j]
        j += 1
        k += 1
        writes += 1
    return writes


def _merge_sort(a: list[int], p: int, r: int) -> int:
    if p >= r:
        return 0
    q = (p + r) // 2
    writes = _merge_sort(a, p, q)
    writes += _merge_sort(a, q + 1, r)
    return writes + _merge(a, p, q, r)


def merge_sort(a: list[int]) -> tuple[list[int], int]:
    """Өсөхөөр эрэмбэлнэ.

    Эрэмбэлэгдсэн жагсаалт болон Merge доторх бичилтийн нийт тоог буцаана.
    """
    a = list(a)
    writes = _merge_sort(a, 0, len(a) - 1)
    return a, writes
