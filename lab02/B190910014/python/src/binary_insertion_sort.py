def binary_insertion_sort(a: list[int]) -> tuple[list[int], int, int]:
    """Өсөхөөр эрэмбэлнэ.

    Эрэмбэлэгдсэн жагсаалт, хайлтын харьцуулалтын тоо болон зөөлтийн тоог
    буцаана. A[i]-тэй тэнцүү гишүүд байвал A[i]-г тэдгээрийн ард оруулна.
    """
    a = list(a)
    comparisons = 0
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        # A[0..i-1]-ээс key-ээс их эхний гишүүний байрлалыг хайна.
        lo, hi = 0, i
        while lo < hi:
            mid = (lo + hi) // 2
            comparisons += 1
            if a[mid] <= key:
                lo = mid + 1
            else:
                hi = mid
        for j in range(i - 1, lo - 1, -1):
            a[j + 1] = a[j]
            shifts += 1
        a[lo] = key
    return a, comparisons, shifts
