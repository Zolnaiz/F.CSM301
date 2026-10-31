def bottom_up_cut_rod(p: list[int]) -> tuple[int, int]:
    """Bottom-Up-Cut-Rod (CLRS 14.1). p[i-1] нь i урттай хэсгийн үнэ.

    Хамгийн их орлого r[n] болон дотоод давталтын биелэлтийн тоог буцаана.
    j = 1..n бүрд дотоод давталт j удаа эргэх тул нийт n(n+1)/2 = Θ(n²).
    """
    n = len(p)
    r = [0] * (n + 1)  # r[j]: j урттай савааны хамгийн их орлого
    loops = 0
    for j in range(1, n + 1):
        q = float("-inf")
        for i in range(1, j + 1):  # эхний хэсгийн урт i
            q = max(q, p[i - 1] + r[j - i])
            loops += 1
        r[j] = q
    return r[n], loops
