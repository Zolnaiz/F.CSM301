"""Codeforces 559B — Equivalent Strings — https://codeforces.com/problemset/problem/559/B

Хоёр мөр тэнцүү урттай a, b. Тэд ижил, эсвэл тэгш урттай бөгөөд хагаслан хуваахад
(a1≡b1 ба a2≡b2) эсвэл (a1≡b2 ба a2≡b1) бол эквивалент.
"""
import sys


def canonical(s: str) -> str:
    """Эквивалент мөрүүдэд ижил гарах «хамгийн бага» хэлбэр.

    Тэгш урттай бол хоёр хагасын хэлбэрийг гаргаад, бага нь эхэнд орно.
    T(n) = 2T(n/2) + Θ(n) = Θ(n lg n).
    """
    if len(s) % 2 == 1:
        return s
    h = len(s) // 2
    x, y = canonical(s[:h]), canonical(s[h:])
    return x + y if x < y else y + x


def equivalent(a: str, b: str) -> bool:
    return canonical(a) == canonical(b)


def main() -> None:
    a, b = sys.stdin.read().split()
    print("YES" if equivalent(a, b) else "NO")


if __name__ == "__main__":
    main()
