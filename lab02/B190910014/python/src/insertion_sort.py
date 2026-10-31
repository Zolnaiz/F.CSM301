def insertion_sort(a: list[int]) -> tuple[list[int], int]:
    """Өсөхөөр эрэмбэлнэ.

    Эрэмбэлэгдсэн жагсаалт болон A[j + 1] = A[j] мөр биелэгдсэн тоог буцаана.
    """
    a = list(a)
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = key
    return a, shifts
