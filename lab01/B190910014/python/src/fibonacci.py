def fibonacci_recursive(n: int) -> int:
    """(a) алхам: тодорхойлолтоор шууд бичсэн хувилбар.

    Дуудалт бүр дахиад хоёр дуудалт үүсгэдэг тул ажиллах хугацаа нь
    экспоненциал, n = 30 орчмоос эхлэн шалгалтын 5 секундэд багтахгүй.
    """
    if n < 0:
        raise ValueError(f"n сөрөг байж болохгүй: {n}")
    if n < 2:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci(n: int) -> int:
    """F(0) = 0, F(1) = 1 дарааллын n-р гишүүнийг Θ(n) хугацаанд буцаана."""
    if n < 0:
        raise ValueError(f"n сөрөг байж болохгүй: {n}")
    prev, curr = 0, 1
    for _ in range(n):
        prev, curr = curr, prev + curr
    return prev
